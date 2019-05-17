#---------------------------------------------#
# Verifier - Discord/Unity Asset Verification #
# Created by isntance.id - http://instance.id #
# github.com/instance-id - system@instance.id #
#---------------------------------------------#
#                                             #

from tinydb import TinyDB, where
from datetime import datetime
from instance.wpoauth2 import Oauth2
import discord
from discord.ext import commands
import traceback
import logging
import jsoncfg
import re

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

# db = TinyDB('../instance/db/sessions.json', default_table='site_sessions')
# config = jsoncfg.load_config('../config/wordpress.json')

db = TinyDB('instance/db/sessions.json', default_table='site_sessions')
config = jsoncfg.load_config('config/wordpress.json')


class WPConnect:
    def __init__(self):
        self.ctx = None
        self.bot = None
        self.session = Oauth2()

    async def wordpress_setup(self, ctx, bot):
        def check(m): return m.author == ctx.message.author
        self.ctx = ctx
        self.bot = bot

        tmpsession = db.get(where('sitename') == config.siteconnection())
        if tmpsession:
            self.session.delete_wpsession(tmpsession)
        request = self.session.oauth_request()
        await ctx.author.send(config.text.connectlink())
        await ctx.author.send(request)
        await ctx.author.send(config.text.enterid())
        code = await self.bot.wait_for('message', check=check)

        authorize = self.session.oauth_authorize(code.content)
        access_token = self.session.oauth_access(authorize)
        if access_token:
            return config.text.connsuccess()
        else:
            config.text.connfail()

    def query(self, wptype, query, *payload):
        if wptype is 'post':
            response = self.session.oauth_post(query, *payload)
            return response
        if wptype is 'get':
            response = self.session.oauth_query(query, payload)
            return response
