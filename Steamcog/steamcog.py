import discord
from discord.ext import commands

class SteamCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.file_path = "steamids.txt"

    @commands.command(name='mysteamid')
    async def save_steam_id(self, ctx, steam_id: str):
        with open(self.file_path, 'a') as f:
            f.write(f"{ctx.author.id}-{steam_id}\n")
        await ctx.send(f"Your steam ID ({steam_id}) has been saved.")

    @commands.command(name='cleanlist')
    async def cleanlist(self, ctx, *role_ids: int):
        guild = ctx.guild
        roles_to_check = [discord.utils.get(guild.roles, id=r) for r in role_ids]
        if None in roles_to_check:
            await ctx.send("One or more of the specified roles do not exist.")
            return

        with open(self.file_path, 'r') as f:
            lines = f.readlines()

        kept_lines = []
        for line in lines:
            user_id, steam_id = line.strip().split('-')
            member = guild.get_member(int(user_id))
            if not member:
                continue
            if any(role in member.roles for role in roles_to_check):
                kept_lines.append(line)

        with open(self.file_path, 'w') as f:
            f.writelines(kept_lines)

        await ctx.send("The Steam ID list has been cleaned.")

def setup(bot):
    bot.add_cog(SteamCog(bot))
