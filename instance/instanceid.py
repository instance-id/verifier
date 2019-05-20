import discord
from discord.ext import commands
import instance.database as data
from instance.database import *
import sys
import traceback
import jsoncfg


COMMAND_PREFIX = '!cmd'
DESCRIPTION = """ instance.Id Discord Assistant """
MODULES = [
    "instance.modules.actions.actions", "instance.modules.validate.validate"
]

config = jsoncfg.load_config('instance/config/config.json')
chars = "\\`*_<>#@:~"


# http://stackoverflow.com/questions/3411771/multiple-character-replace-with-python
def escape_name(name):
    name = str(name)
    for c in chars:
        if c in name:
            name = name.replace(c, "\\" + c)
    return name.replace("@", "@\instance.id")  # prevent mentions


bot = commands.Bot(command_prefix=COMMAND_PREFIX, description=DESCRIPTION, pm_help=None, escape_name=escape_name)
bot.escape_name = escape_name


# ---------------------------------------- Main functionality -------------------------------------
@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    print(discord.utils.oauth_url(bot.user.id))
    info = await bot.application_info()


class InstanceId:
    """instance.id Verification Module"""
    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    def start():
        token = config.token()
        if token:
            for module in MODULES:
                try:
                    bot.load_extension(module)
                except Exception as e:
                    print(f'Bot could not load: {module}', file=sys.stderr)
                    traceback.print_exc()
            data.main()
            bot.run(token)
        else:
            print("Missing Discord token in config.json")
