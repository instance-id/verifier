from .actions import Actions


def setup(bot):
    bot.add_cog(Actions(bot))
