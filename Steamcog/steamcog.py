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
    async def cleanlist(self, ctx):
        # Get the guild and role IDs from the cog settings
        guild_id = self.settings.guild_id
        role_ids = self.settings.role_ids

        # Get the guild object
        guild = self.bot.get_guild(guild_id)

        # Get the role objects by their IDs
        roles_to_check = [guild.get_role(r) for r in role_ids]

        if not roles_to_check:
            await ctx.send("No roles to check")
            return

        # Open the file and read the contents
        with open(STEAMID_FILE, 'r') as f:
            steamids = f.read().splitlines()

        # Loop through the steam IDs and check if the users have the required roles
        new_steamids = []
        for line in steamids:
            # Split the line into discord ID and steam ID
            discord_id, steam_id = line.split("-")

            # Get the member object from the discord ID
            member = guild.get_member(int(discord_id))

            # Check if the member has any of the required roles
            if any(role in member.roles for role in roles_to_check):
                new_steamids.append(line)

        # Rewrite the file with the new steam IDs
        with open(STEAMID_FILE, 'w') as f:
            f.write('\n'.join(new_steamids))
    
        await ctx.send("Cleaned the list.")




def setup(bot):
    bot.add_cog(SteamCog(bot))
