from redbot.core import commands, checks, Config
import discord
from discord.ext import commands

class SteamCog(commands.Cog, name="SteamCog"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="mysteamid")
    async def mysteamid(self, ctx, steam_id: str):
        steam_id = steam_id.strip()
        if steam_id:
            with open("steam_ids.txt", "a") as f:
                f.write(f"{ctx.author.id}-{steam_id}\n")
            await ctx.send(f"{ctx.author.mention}, your Steam ID has been saved.")
        else:
            await ctx.send(f"{ctx.author.mention}, you need to provide a Steam ID.")

    @commands.command(name="cleanlist")
    async def cleanlist(self, ctx, *role_ids: int):
        if not role_ids:
            await ctx.send("Please provide at least one role ID.")
            return

        with open("steam_ids.txt", "r") as f:
            steam_id_lines = f.readlines()

        new_steam_id_lines = []
        for line in steam_id_lines:
            discord_id, steam_id = line.strip().split("-")
            member = ctx.guild.get_member(int(discord_id))
            if member:
                member_role_ids = [role.id for role in member.roles]
                if any(role_id in member_role_ids for role_id in role_ids):
                    new_steam_id_lines.append(line)
            else:
                new_steam_id_lines.append(line)

        with open("steam_ids.txt", "w") as f:
            f.writelines(new_steam_id_lines)

        await ctx.send(f"{ctx.author.mention}, the Steam ID list has been cleaned.")



def setup(bot):
    bot.add_cog(SteamCog(bot))
