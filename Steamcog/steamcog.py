from redbot.core import commands
import discord
import os


class SteamCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "steam_id.txt")
        self.load_steam_ids()

    def load_steam_ids(self):
        self.steam_ids = {}
        try:
            with open(self.file_path) as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    discord_id, steam_id = line.split("-")
                    self.steam_ids[discord_id] = steam_id
        except FileNotFoundError:
            pass

    def save_steam_ids(self):
        with open(self.file_path, "w") as f:
            for discord_id, steam_id in self.steam_ids.items():
                f.write(f"{discord_id}-{steam_id}\n")

    @commands.command()
    async def mysteamid(self, ctx, steamid):
        discord_id = str(ctx.author.id)
        self.steam_ids[discord_id] = steamid
        self.save_steam_ids()
        await ctx.send(f"Your steam ID ({steamid}) has been saved.")

    @commands.command()
    async def cleanlist(self, ctx, *role_names):
        guild = ctx.guild
        if not role_names:
            await ctx.send("Please provide at least one role name to clean the list.")
            return

        roles_to_check = [discord.utils.get(guild.roles, name=r) for r in role_names]
        if None in roles_to_check:
            await ctx.send("One or more of the specified roles do not exist.")
            return

        new_steam_ids = {}
        for discord_id, steam_id in self.steam_ids.items():
            member = guild.get_member(int(discord_id))
            if member is not None and any(role in member.roles for role in roles_to_check):
                new_steam_ids[discord_id] = steam_id
        self.steam_ids = new_steam_ids
        self.save_steam_ids()

        steam_ids_str = "\n".join(f"{discord_id}: {steam_id}" for discord_id, steam_id in self.steam_ids.items())
        await ctx.send(f"Remaining Steam IDs:\n{steam_ids_str}")


def setup(bot):
    bot.add_cog(SteamCog(bot))
