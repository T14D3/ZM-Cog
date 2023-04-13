from discord.ext import commands
import discord

class SteamCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="mysteamid")
    async def mysteamid(self, ctx, steam_id: str):
        steam_id = steam_id.strip()
        if steam_id:
            with open("steam_ids.txt", "r") as f:
                steam_ids = f.readlines()
            steam_ids = [line.strip() for line in steam_ids]
            for i in range(len(steam_ids)):
                if steam_ids[i].startswith(f"{ctx.author.id}-"):
                    steam_ids.pop(i)
                    break
            steam_ids.append(f"{ctx.author.id}-{steam_id}")
            with open("steam_ids.txt", "w") as f:
                f.write("\n".join(steam_ids))
            await ctx.send(f"{ctx.author.mention}, your Steam ID has been saved.")
        else:
            await ctx.send(f"{ctx.author.mention}, you need to provide a Steam ID.")

    @commands.command(name="cleansteamids")
    async def cleansteamids(self, ctx, *role_ids: int):
        with open("steam_ids.txt", "r") as f:
            steam_ids = f.readlines()
        steam_ids = [line.strip() for line in steam_ids]
        cleaned_count = 0
        for i in range(len(steam_ids)):
            discord_id = steam_ids[i].split("-")[0]
            member = ctx.guild.get_member(int(discord_id))
            if member:
                has_role = False
                for role in member.roles:
                    if role.id in role_ids:
                        has_role = True
                        break
                if not has_role:
                    steam_ids.pop(i)
                    cleaned_count += 1
            else:
                steam_ids.pop(i)
                cleaned_count += 1
        with open("steam_ids.txt", "w") as f:
            f.write("\n".join(steam_ids))
        await ctx.send(f"Cleaned {cleaned_count} entries from steam_ids.txt")

    @commands.command(name="fetchsteamids")
    async def fetchsteamids(self, ctx):
        with open("steam_ids.txt", "r") as f:
            steam_ids = f.readlines()
        steam_ids = [line.split("-")[1].strip() for line in steam_ids]
        ids_str = "\n".join(steam_ids)
        file = discord.File(filename="ids.txt", fp=io.StringIO(ids_str))
        await ctx.send(file=file)

def setup(bot):
    bot.add_cog(SteamCog(bot))
