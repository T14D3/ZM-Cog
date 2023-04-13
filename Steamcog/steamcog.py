import discord
from discord.ext import commands

import os


class SteamCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def check_role(self, member, roles):
        """
        Check if a member has at least one of the roles provided.
        """
        member_roles = [role.id for role in member.roles]
        return bool(set(member_roles).intersection(set(roles)))

    @commands.command(name="mysteamid")
    async def mysteamid(self, ctx, steam_id: str):
        steam_id = steam_id.strip()
        if steam_id:
            # check if the discord ID already exists in the file
            discord_id = str(ctx.author.id)
            with open("steam_ids.txt", "r") as f:
                for line in f:
                    if discord_id in line:
                        await ctx.send(f"{ctx.author.mention}, your Steam ID has been updated.")
                        break
                else:
                    await ctx.send(f"{ctx.author.mention}, your Steam ID has been saved.")
            # add the discord ID - steam ID pair to the file
            with open("steam_ids.txt", "a") as f:
                f.write(f"{discord_id}-{steam_id}\n")
        else:
            await ctx.send(f"{ctx.author.mention}, you need to provide a Steam ID.")

    @commands.command(name="cleanlist")
    async def cleanlist(self, ctx, *roles: discord.Role):
        # get the IDs of the roles provided
        role_ids = [role.id for role in roles]

        # read the file and remove the entries that don't have at least one of the roles provided
        with open("steam_ids.txt", "r") as f:
            lines = f.readlines()
        with open("steam_ids.txt", "w") as f:
            cleaned = 0
            for line in lines:
                discord_id, steam_id = line.strip().split("-")
                member = ctx.guild.get_member(int(discord_id))
                if member and await self.check_role(member, role_ids):
                    f.write(f"{discord_id}-{steam_id}\n")
                else:
                    cleaned += 1
            await ctx.send(f"{ctx.author.mention}, cleaned {cleaned} entries from the list.")

    @commands.command(name="fetchsteamids")
    async def fetchsteamids(self, ctx):
        # read the file and extract the steam IDs
        steam_ids = []
        with open("steam_ids.txt", "r") as f:
            for line in f:
                _, steam_id = line.strip().split("-")
                steam_ids.append(steam_id)

        # create a file and attach it to the bot's response
        with open("ids.txt", "w") as f:
            f.write("\n".join(steam_ids))
        with open("ids.txt", "rb") as f:
            await ctx.send(file=discord.File(f, "ids.txt"))

def setup(bot):
    bot.add_cog(SteamCog(bot))
