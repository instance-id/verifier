#!/usr/bin/env python3.6
#---------------------------------------------#
# Verifier - Discord/Unity Asset Verification #
# Created by isntance.id - http://instance.id #
# github.com/instance-id - system@instance.id #
#---------------------------------------------#
#                                             #

import discord
from discord.ext import commands
from discord.ext.commands import  has_permissions, MissingPermissions
import instance.database as data
from instance.database import *
from .wpconnect import WPConnect
import sys
import traceback
import jsoncfg
from datetime import datetime
from jsoncfg.value_mappers import require_string
import logging
import asyncio
import requests

text = jsoncfg.load_config('config/text.json')
config = jsoncfg.load_config('config/config.json')
wpsettings = jsoncfg.load_config('config/wordpress.json')

# <editor-fold desc="Logging definitions">
from colorlog import ColoredFormatter

log = logging.getLogger(__name__)
LOG_LEVEL = logging.DEBUG
LOGFORMAT = "  %(log_color)s%(levelname)-8s%(reset)s | %(log_color)s%(message)s%(reset)s"
logging.root.setLevel(LOG_LEVEL)
formatter = ColoredFormatter(LOGFORMAT)
stream = logging.StreamHandler()
stream.setLevel(LOG_LEVEL)
stream.setFormatter(formatter)
log.setLevel(LOG_LEVEL)
log.addHandler(stream)
# </editor-fold>

colorlight=0x2d35a3


COMMAND_PREFIX = '!cmd'
DESCRIPTION = """ instance.Id Discord Assistant """
MODULES = [
    'instance.modules.actions.actions'
]
chars = "\\`*_<>#@:~"
guildId = config.discordIds['guild']()
botusers = config.discordIds['botusers']()
verifyId = config.roles['Verified']()



# http://stackoverflow.com/questions/3411771/multiple-character-replace-with-python
def escape_name(name):
    name = str(name)
    for c in chars:
        if c in name:
            name = name.replace(c, "\\" + c)
    return name.replace("@", "@\instance.id")  # prevent mentions

bot = commands.Bot(command_prefix=COMMAND_PREFIX, description=DESCRIPTION, pm_help=None, escape_name=escape_name)
bot.escape_name = escape_name


#  ------------------------ Conversion determination -------------------------------
# Checks if the purchase date it after the date in which the asset became ex. v2. If so, v2 will be verified.
def asset_compare(date):
    getdate = config.comparedate(require_string)
    comparedate = datetime.strptime(getdate, '%Y-%m-%d')
    purchasedate = datetime.strptime(date, '%Y-%m-%d')
    return purchasedate > comparedate


def iterate(response, verification):
    if response:
        try:
            for invoice in response['invoices']:
                if verification in invoice['package']:
                    data = invoice
                    cont = True
                    return data, cont
                else:
                    pass

        except Exception as e:
            print(f'No invoice found, please ensure you used the correct shortcode for the product.')
            traceback.print_exc()
    else:
        return 'Invalid response from server.'


def determine_apikey(pkg):
    api = config.apiKey[pkg]()
    return api


def determine_asset(asset):
    package = config.package[asset]()
    return package


def check_valid(pkg, upkg):
    if pkg == upkg:
        return True
    else:
        return False


async def wp_email_check(self, ctx):
    def check(m):
        return m.author == ctx.message.author
    # Ugly, but necessary for now to convert all text to lowercase so there is no discrepancy from input vs expected
    await ctx.send(text.email_capture_during_verification())
    email = await self.bot.wait_for('message', check=check)
    tmp = wpsettings.applyrole()
    apply = tmp.lower()
    if apply == "yes":
        email_check = await self.wordpress_email_verify(ctx, email.content)
        data = jsoncfg.loads(email_check)
        if data['id'] is not 'null' and data['email'] == email.content:
            return email.content
        else:
            addy = config.miscsettings.webaddress()
            await ctx.send('No account for email: ' + email.content + ' at ' +
                           addy + '. Please ensure you have an account created, if not, '
                                                              'create one and then verify your invoice again'
                                                              ' using the email address used for account creation.')
            email = ''
            return email
    else:
        email = email.content
        return email


class Validate:
    """instance.id Verification Module"""
    def __init__(self, bot):
        self.wordpress = False
        self.wp = None
        w = config.features.wordpress()
        self.word = w.lower()
        if self.word == 'yes':
            self.wordpress = True
            self.wp = WPConnect()
        self.bot = bot

    @commands.command()
    async def verify(self, ctx):
        verifyText = open("config/verify_text.txt", "r").read()
        await ctx.author.send(verifyText)

    @commands.command()
    async def validate(self, ctx, pkg, invoice, user: discord.Member = None):
        """ Performs asset validation process """
        email = ''
        #  This gets the guild(server) id and 'Verified' roles from the config.json file
        role = ctx.bot.get_guild(guildId).get_role(verifyId)
        discriminator = ctx.bot.get_guild(guildId).get_member(ctx.author.id).discriminator
        user = ctx.bot.get_guild(guildId).get_member(ctx.author.id).name
        userid = user + '#' + discriminator

        inuse = find_invoice(invoice)
        if inuse is False:
            pass
        else:
            await ctx.send(text.invoice_in_use())
            return
        em = config.miscsettings.requireemail()
        ema = em.lower()
        if ema == 'yes':
            while True:
                check = await wp_email_check(self, ctx)
                if check is not '':
                    email = check
                    break
                else:
                    await ctx.send('Could not verify email address. Please try again. '
                                   'If problem persists please contact support')
                    return

        pkg = str(pkg)
        apikey = determine_apikey(pkg)
        verification = determine_asset(pkg)
        #  Takes the user input of asset package and invoice number and sends it to the asset store verification api
        payload = {'key': {apikey}, 'invoice': {invoice}}
        r = requests.get('https://api.assetstore.unity3d.com/publisher/v1/invoice/verify.json', params=payload)
        response = r.json()
        if len(response['invoices']) <= 0:
            await ctx.send(text.no_invoice_found())
        rdata, token = iterate(response, verification)
        presponse = rdata['package']
        #  If verification is successful add appropriate roles to the user and create database entry used to check
        #  if an invoice has already been claimed
        if token is True:
            valid = check_valid(rdata['package'], verification)
            if valid:
                cmpr = config.datecompare()
                compare = cmpr.lower()
                if compare == 'yes':
                    asset1 = config.compareasset1()
                    asset2 = config.compareasset2()
                    if pkg == asset1 or pkg == asset2:
                        datetest = asset_compare(rdata['date'])
                        if datetest:
                            presponse = asset2
                        else:
                            await ctx.send(text.legacy_assets())
                            return
                    else:
                        pass
                else:
                    pass
                if self.wordpress:
                    tmp2 = wpsettings.applyrole()
                    apply = tmp2.lower()
                    if apply == "yes":
                        wpreply = await self.wordpress_chg(ctx, email, pkg.lower())
                        if wpreply is not str:
                            if wpreply.status_code is 200:
                                await ctx.send('Permission has been applied to ' + config.miscsettings.webaddress() + '.')
                            else:
                                await ctx.send('Unable to automatically apply account changes for: ' + email + ' at ' +
                                               config.miscsettings.webaddress() + '. Please ensure you have an account created, if not, '
                                                                     'create one and then verify your invoice again'
                                                                     ' using the email address used for account creation.')
                                return
                        else:
                            await ctx.send(wpreply)
                            return
                    else:
                        pass
                else:
                    pass
                try:
                    add_invoice(userid, invoice, pkg, rdata['date'], email)
                except Exception as e:
                    print(e)
                    traceback.print_exc()
                    await ctx.send('Invoice verification has not completed. Please try again. If the issue '
                                   'persists, please contact a member for support.')
                    return
                roleId = ctx.bot.get_guild(guildId).get_role(config.roles[pkg]())
                await self.bot.get_guild(guildId).get_member(ctx.author.id).add_roles(role, roleId)
                await ctx.send('Response: ' + presponse + ' ' + 'Verified')

    @validate.error
    async def validate_on_error(self, ctx, error):
        return await ctx.send('Both product shortcode as well as an invoice number '
                              'are needed to verify an invoice. Please type !cmdverify'
                              ' to see validation help information')

    #  ------------------------ Database maintenance commands -------------------------------
    @commands.command()
    @commands.has_permissions(manage_roles=True)
    # Search by invoice number to see what account it is currently tied to. It will show other invoices for that user
    async def searchinvoice(self, ctx, invoice):
        name, inv = search_invoice(invoice)
        if not inv:
            result = text.search_no_invoice()
            await ctx.author.send(result)
        else:
            embed = discord.Embed(title=f'Invoice viewer :     ', description=f'```md\n\nUser details                          \n'
                                                                          f'Name    | {name}\n'
                                                                          f'package | {inv["package"]}\n'
                                                                          f'Invoice | {inv["invoice"]}\n'
                                                                          f'Purchase| {inv["purdate"]}\n'
                                                                          f'Verified| {inv["verifydate"]}\n'
                                                                          f'\n*----------------------*```', color=colorlight)
            await ctx.author.send('', embed=embed)

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    # Search for a specific user and receive back all invoices assigned to their account
    async def searchuser(self, ctx, user):
        results = search_user(user)
        if type(results) == str:
            await ctx.author.send(results)
        else:
            try:
                for package in results:
                    for pack in package['packages']:
                        embed = discord.Embed(title=f'Invoice viewer :     ', description=f'```md\n\nUser details                          \n'
                                                                                           f'Name    | {package["username"]}\n'
                                                                                           f'package | {pack["package"]}\n'
                                                                                           f'Invoice | {pack["invoice"]}\n'
                                                                                           f'Purchase| {pack["purdate"]}\n'
                                                                                           f'Verified| {pack["verifydate"]}\n'
                                                                                          f'\n*----------------------*```', color=colorlight)
                        await ctx.author.send('', embed=embed)
            except Exception as e:
                await ctx.author.send('Problem encountered.')
                traceback.print_exc()

    @commands.command()
    @commands.is_owner()
    # Delete an individual invoice entry from a user account
    async def deleteinvoice(self, ctx, message):
        def check(m): return m.author == ctx.message.author
        inv = message
        # await ctx.author.send('Are you sure you want to delete ' + inv + ' ? Reply yes/no.')
        embed = discord.Embed(title=f'Invoice Management : Delete', description=f'```md\n\nAre you sure you would like to Delete {inv}?\n'
                                                                                              f'[1] | Delete Invoice\n'
                                                                                              f'[2] | Cancel Deleting\n'
                                                                                              f'[3] | Exit this menu\n\n*This Menu will timeout in 30s*```', color=colorlight)
        mainmsg = await ctx.message.channel.send('', embed=embed)
        confirm = await self.bot.wait_for('message', timeout=15, check=check)

        embed.add_field(name=u'\u274C', value='Menu timed out')
        await mainmsg.edit(embed=embed)
        timeout = 1

        if confirm.content.lower().strip() == '1':
            results = delete_invoice(inv)
        else:
            results = 'Canceling operation'
        await ctx.author.send(results)

    @commands.command(name='dbsetup')
    @commands.is_owner()
    # Command to setup database tables
    async def db_setup(self, ctx):
        result = db_setup()
        await ctx.author.send(result)

    # ---------------------------------------------------------------- WordPress

    @commands.command(name='wpsetup')
    @commands.is_owner()
    # Command to begin WordPress Oauth2 integration
    async def wp_setup(self, ctx):
        if self.wordpress:
            word = await self.wp.wordpress_setup(ctx, bot)
            if word is not str:
                await ctx.author.send('Connection successfully created.')
            else:
                await ctx.author.send(word)
        else:
            await ctx.author.send('WordPress module is not enabled.')
            return 'WordPress module is not enabled.'


    # Wordpress email lookup
    async def wordpress_email_verify(self, ctx, email):
        if self.wordpress:
            wptype ='get'
            query = 'wp-json/instance/v1/email/%s'
            r = self.wp.query(wptype, query, email)
            return r
        else:
            await ctx.author.send('WordPress module is not enabled.')
            return 'WordPress module is not enabled.'

    @commands.command(name='wpemail')
    @commands.is_owner()
    # Test to check email
    async def wordpress_email(self, ctx, email):
        if self.wordpress:
            wptype ='get'
            query = 'wp-json/instance/v1/email/%s'
            r = self.wp.query(wptype, query, email)
            this = jsoncfg.loads(r)
        else:
            await ctx.author.send('WordPress module is not enabled.')
            return 'WordPress module is not enabled.'

    @commands.command(name='wpid')
    @commands.is_owner()
    # Get WordPress ID for user
    async def wordpress_id(self, ctx, payload):
        if self.wordpress:
            wptype = 'get'
            query = 'wp-json/wp/v2/users/%s?context=view'
            r = self.wp.query(wptype, query,  payload)
        else:
            await ctx.author.send('WordPress module is not enabled.')
            return 'WordPress module is not enabled.'

    @commands.command(name='wpchange')
    @commands.is_owner()
    # Database wipe command to be used for testing purposes only during development
    async def wordpress_change(self, ctx, email, role):
        if self.wordpress:
            payload = [email, role]
            wptype = 'post'
            query = 'wp-json/wp/v2/users/%s'
            r = self.wp.query(wptype, query,  *payload)
            return r
        else:
            await ctx.author.send('WordPress module is not enabled.')
            return 'WordPress module is not enabled.'

    # Called to change users role within WordPress to apply role for a given asset
    async def wordpress_chg(self, ctx, email, role):
        if self.wordpress:
            payload = [email, role]
            wptype = 'post'
            query = 'wp-json/wp/v2/users/%s'
            r = self.wp.query(wptype, query,  *payload)
            return r
        else:
            await ctx.author.send('WordPress module is not enabled.')
            return 'WordPress module is not enabled.'

# ---------------------------------------- Main functionality -------------------------------------
@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    print(discord.utils.oauth_url(bot.user.id))
    info = await bot.application_info()

for module in MODULES:
    try:
        bot.load_extension(module)
    except Exception as e:
        print(f'Bot could not load: {module}', file=sys.stderr)
        traceback.print_exc()


class InstanceId:
    """instance.id Verification Module"""
    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    def start():
        token = config.token()
        if token:
            bot.add_cog(Validate(bot))
            data.main()
            bot.run(token)
        else:
            print("Missing Discord token in config.json")
