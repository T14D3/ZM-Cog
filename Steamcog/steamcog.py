from redbot.core import commands
from typing import Dict, Union

class SteamCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="mysteamid")
    async def mysteamid(self, ctx, steam_id: str):
        steam_id = steam_id.strip()
        if steam_id:
            with open("steam_ids.txt", "a") as f:
                f.write(f"{ctx.author.id}:{steam_id}\n")
            await ctx.send(f"{ctx.author.mention}, your Steam ID has been saved.")
        else:
            await ctx.send(f"{ctx.author.mention}, you need to provide a Steam ID.")

    @commands.command(name="cleanlist")
    async def cleanlist(self, ctx, *role_ids: Union[int]):
        with open("steam_ids.txt", "r") as f:
            steam_ids = f.read().strip().split("\n")
        new_steam_ids = []
        for steam_id in steam_ids:
            discord_id, steam_id = steam_id.split(":")
            member = ctx.guild.get_member(int(discord_id))
            if member:
                roles = [role.id for role in member.roles]
                if any(role_id in roles for role_id in role_ids):
                    new_steam_ids.append(f"{discord_id}:{steam_id}")
        with open("steam_ids.txt", "w") as f:
            f.write("\n".join(new_steam_ids))
        await ctx.send(f"{len(steam_ids) - len(new_steam_ids)} Steam IDs have been removed.")

        
def setup(bot):
    bot.add_cog(SteamCog(bot))
