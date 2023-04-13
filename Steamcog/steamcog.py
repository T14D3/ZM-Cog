from redbot.core import commands, checks, Config
import discord

class SteamCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=1234567890)
        default_global = {
            "steam_ids": {}
        }
        self.config.register_global(**default_global)
        
    @commands.command(name="mysteamid")
    async def mysteamid(self, ctx, steam_id: str):
        steam_id = steam_id.strip()
        if steam_id:
            async with self.config.steam_ids() as steam_ids:
                steam_ids[str(ctx.author.id)] = steam_id
            await ctx.send(f"{ctx.author.mention}, your Steam ID has been saved.")
        else:
            await ctx.send(f"{ctx.author.mention}, you need to provide a Steam ID.")
            
    @commands.command(name="cleanlist")
    async def cleanlist(self, ctx, *role_ids: int):
        role_names = []
        guild = ctx.guild
        for role_id in role_ids:
            role = guild.get_role(role_id)
            if role:
                role_names.append(role.name)
        if not role_names:
            await ctx.send(f"{ctx.author.mention}, please provide at least one valid role.")
            return
        
        async with self.config.steam_ids() as steam_ids:
            id_list = list(steam_ids.keys())
            roles_to_check = [discord.utils.get(guild.roles, name=r) for r in role_names]
            for user_id in id_list:
                member = guild.get_member(int(user_id))
                if member:
                    member_roles = member.roles
                    if not any(role in member_roles for role in roles_to_check):
                        del steam_ids[user_id]
        await ctx.send("The list has been cleaned.")


def setup(bot):
    bot.add_cog(SteamCog(bot))
