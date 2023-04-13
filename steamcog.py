import discord
from discord.ext import commands

class SteamCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Command to register user's steam ID
    @commands.command()
    async def register(self, ctx, steam_id: int):
        with open("steamids.txt", "a") as file:
            file.write(f"{ctx.author.id}-{steam_id}\n")
        await ctx.send("Steam ID registered!")

    # Command to check for steam IDs associated with specific roles
    @commands.command()
    async def check(self, ctx, *roles: discord.Role):
        # Get list of user IDs with specified roles
        role_ids = [member.id for member in ctx.guild.members if any(role in member.roles for role in roles)]
        # Read file to get all steam IDs
        with open("steamids.txt", "r") as file:
            steam_ids = file.readlines()
        # Filter steam IDs for those associated with role IDs
        steam_ids = [line.split("-")[1].strip() for line in steam_ids if int(line.split("-")[0]) in role_ids]
        # Output remaining steam IDs
        await ctx.send("Remaining Steam IDs: \n" + "\n".join(steam_ids))
