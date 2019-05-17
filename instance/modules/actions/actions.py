# ------------------------------------------- #
# Verifier - Discord/Unity Asset Verification #
# Created by isntance.id - http://instance.id #
# github.com/instance-id - system@instance.id #
# ------------------------------------------- #
#                                             #

import discord
from discord.ext import commands
from datetime import datetime, timedelta
import traceback
import asyncio
import jsoncfg
import logging
import sys

log = logging.getLogger(__name__)


# These are some general loading / unloading and maintenance actions. Maybe more if I don't plan properly
class Actions:
    """instance.id Actions Module"""

    def __init__(self, bot):
        self.bot = bot

    #  ------------------------ Load and unload extension modules -------------------------------
    @commands.command()
    @commands.is_owner()
    async def load(self, ctx, module):  # If I make a new module and I want to install it, this will hot-load it.
        try:
            self.bot.load_extension("instance." + "modules." + module + '.' + module)
            complete = True
        except Exception as e:
            print(f'Bot could not load: {module}.', file=sys.stderr)
            traceback.print_exc()
            complete = False

        if complete:
            result = 'Load of ' + module + ' complete.'
        else:
            result = 'Load of ' + module + ' failed.'
        await ctx.author.send(result)

    @commands.command()
    @commands.is_owner()
    async def reload(self, ctx, module):  # Hot-reload of a module if I am actively making changes to it
        try:
            self.bot.unload_extension("modules." + module + '.' + module)
            self.bot.load_extension("modules." + module + '.' + module)
            complete = True
        except Exception as e:
            print(f'Bot could not load: {module}.', file=sys.stderr)
            traceback.print_exc()
            complete = False

        if complete:
            result = 'Reload of ' + module + ' complete.'
        else:
            result = 'Reload of ' + module + ' failed.'
        await ctx.author.send(result)

    @commands.command()
    @commands.is_owner()
    async def unload(self, ctx, module):  # Hot-reload of a module if I am actively making changes to it
        try:
            self.bot.unload_extension("modules." + module + '.' + module)
            complete = True
        except Exception as e:
            print(f'Bot could not load: {module}.', file=sys.stderr)
            traceback.print_exc()
            complete = False

        if complete:
            result = 'Unload of ' + module + ' complete.'
        else:
            result = 'Unload of ' + module + ' failed.'
        await ctx.author.send(result)

    @commands.command()
    @commands.is_owner()
    @asyncio.coroutine
    def purge_all(self, ctx, limit: int = 100):
        """Delete all messages in the channel"""
        if ctx.invoked_subcommand is None:
            date_limit = datetime.today() - timedelta(days=12)
            yield from ctx.message.channel.purge(after=date_limit, bulk=True)
            yield from ctx.author.send('Purge Complete')


def setup(bot):
    bot.add_cog(Actions(bot))
