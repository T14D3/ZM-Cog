import discord
from redbot.core import commands

class Steamcog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="mysteamid")
    async def mysteamid(self, ctx, steam_id: str):
        steam_id = steam_id.strip()
        if steam_id:
            with open("steam_ids.txt", "r+") as file:
                lines = file.readlines()
                file.seek(0)
                for line in lines:
                    if str(ctx.author.id) not in line:
                        file.write(line)
                file.truncate()
                file.write(f"{ctx.author.id}-{steam_id}\n")
            await ctx.send(f"{ctx.author.mention}, your Steam ID has been saved.")
        else:
            await ctx.send(f"{ctx.author.mention}, you need to provide a Steam ID.")

    @commands.command(name="cleansteamids")
    async def cleanlist(self, ctx, *roles: discord.Role):
        role_ids = [role.id for role in roles]  # convert role IDs to int
        with open("steam_ids.txt", "r+") as file:
            lines = file.readlines()
            file.seek(0)
            count = 0
            for line in lines:
                discord_id, steam_id = line.strip().split("-")
                member = ctx.guild.get_member(int(discord_id))
                if not member or any(role_id in member._roles for role_id in role_ids):
                    file.write(line)
                else:
                    count += 1
            file.truncate()
        await ctx.send(f"Cleaned {count} steam IDs from the file.")


    @commands.command(name="fetchsteamids")
    async def fetchsteamids(self, ctx):
        with open("steam_ids.txt", "r") as file:
            steam_ids = [line.strip().split("-")[1] for line in file.readlines()]
        ids_str = "\n".join(steam_ids)
        await ctx.send(content=ids_str, file=discord.File(filename="ids.txt"))



def setup(bot):
    bot.add_cog(Steamcog(bot)) 
