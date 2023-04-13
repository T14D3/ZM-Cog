from discord.ext import commands

class SteamCog(commands.Cog):
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
    @commands.has_permissions(administrator=True)
    async def cleanlist(self, ctx, *role_ids):
        role_ids = [int(r) for r in role_ids if r.isdigit()]
        if not role_ids:
            return await ctx.send("Please provide at least one valid role ID.")

        lines_to_keep = []
        with open("steam_ids.txt", "r") as f:
            for line in f:
                discord_id, steam_id = line.strip().split("-")
                member = await ctx.guild.fetch_member(discord_id)
                if not member:
                    continue
                member_role_ids = [r.id for r in member.roles]
                if any(r_id in member_role_ids for r_id in role_ids):
                    lines_to_keep.append(line)

        with open("steam_ids.txt", "w") as f:
            f.writelines(lines_to_keep)

        await ctx.send("Done. The Steam ID list has been cleaned.")
        
def setup(bot):
    bot.add_cog(SteamCog(bot))
