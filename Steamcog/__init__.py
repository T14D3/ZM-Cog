from .steamcog import Steamcog


def setup(bot):
    bot.add_cog(Steamcog(bot))
