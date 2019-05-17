#---------------------------------------------#
# Verifier - Discord/Unity Asset Verification #
# Created by isntance.id - http://instance.id #
# github.com/instance-id - system@instance.id #
#---------------------------------------------#
#                                             # 
from .actions import Actions


def setup(bot):
    bot.add_cog(Actions(bot))
