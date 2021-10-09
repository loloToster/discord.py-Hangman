from discord.ext import commands
import os
import json

root = os.path.dirname(os.path.abspath(__file__)).replace("\\", "/")


class Settings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def prefix(self, ctx, newPrefix):
        with open("") as f:
            data = json.load(f)
        data["prefix"] = newPrefix
        with open(f"{root}/files/data.json", "w") as f:
            json.dump(data, f, indent=2)
        await ctx.send(f"Changing prefix to `{newPrefix}`")

    @commands.command()
    async def help(self, ctx):
        pass


def setup(bot):
    bot.add_cog(Settings(bot))
