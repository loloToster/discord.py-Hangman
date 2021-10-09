from discord.ext import commands
import os
import json

root = os.path.dirname(os.path.abspath(__file__)).replace("\\", "/") + "/.."


class Settings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        await ctx.send("Pong")

    @commands.has_permissions(administrator=True)
    @commands.command()
    async def prefix(self, ctx, newPrefix: str):
        with open(f"{root}/files/data.json", "r+") as f:
            dataJSON = json.load(f)
            dataJSON["prefix"] = newPrefix
            f.seek(0)
            json.dump(dataJSON, f, indent=2)
            f.truncate()
        await ctx.send(f"Changing prefix to `{newPrefix}`")

    @commands.command()
    async def help(self, ctx):
        pass


def setup(bot):
    bot.add_cog(Settings(bot))
