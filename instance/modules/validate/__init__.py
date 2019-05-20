from .validate import Validate


def setup(bot):
    bot.add_cog(Validate(bot))
