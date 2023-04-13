from .steamcog import SteamCog


def setup(bot):
    bot.add_cog(SteamCog(bot))
