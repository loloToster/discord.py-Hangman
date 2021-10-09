from discord import Embed
from discord import Color
from discord.ext import commands
import os
import json

root = os.path.dirname(os.path.abspath(__file__)).replace("\\", "/") + "/.."


class Managment(commands.Cog):
    """Category that has every commands not related to hangman game"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(brief="command for checking if bot is running")
    async def ping(self, ctx):
        await ctx.send("Pong")

    @commands.has_permissions(administrator=True)
    @commands.command(brief="changes prefix")
    async def prefix(self, ctx, newPrefix: str):
        with open(f"{root}/files/data.json", "r+") as f:
            dataJSON = json.load(f)
            dataJSON["prefix"] = newPrefix
            f.seek(0)
            json.dump(dataJSON, f, indent=2)
            f.truncate()
        await ctx.send(f"Changing prefix to `{newPrefix}`")

    @commands.command(aliases=["h"], brief="help command")
    async def help(self, ctx, query: str = None):
        prefix = self.bot.command_prefix(self.bot, ctx.message)
        if query:
            for cog in self.bot.cogs:
                if cog.lower() == query.lower():
                    embed = Embed(
                        title=f"Categories / {cog}:",
                        color=Color.green(),
                    )
                    embed.add_field(
                        name=f"Description:",
                        value=self.bot.get_cog(cog).description
                        if self.bot.get_cog(cog).description
                        else "This category does not have a description",
                        inline=False,
                    )
                    commandsDisp = ""
                    for command in self.bot.get_cog(cog).get_commands():
                        try:
                            if await command.can_run(ctx):
                                commandsDisp += f"**\u2022 `{command.name}` :**\n└ {command.brief if command.brief != None else 'This command does not have a description'}\n"
                        except:
                            pass
                    embed.add_field(
                        name=f"Commands:",
                        value=commandsDisp,
                        inline=False,
                    )
                    embed.set_footer(
                        text=f'Use "{prefix}help <Command>" to get more info'
                    )
                    break
            else:
                for command in self.bot.walk_commands():
                    try:
                        canrun = await command.can_run(ctx)
                    except:
                        canrun = False
                    if (
                        command.name.lower() == query.lower()
                        or query.lower() in [alias.lower() for alias in command.aliases]
                    ) and canrun:
                        embed = Embed(
                            title=f"Categories / {command.cog_name} / {command.name}:",
                            color=Color.green(),
                        )
                        description = (
                            command.description
                            if command.description
                            else command.brief
                            if command.brief
                            else "This command does not have a description"
                        )
                        embed.add_field(
                            name="Description:",
                            value=description,
                            inline=False,
                        )
                        callStatements = f"\u2022 `{prefix}{command.name}`\n"
                        for alias in command.aliases:
                            callStatements += f"\u2022 `{prefix}{alias}`\n"
                        embed.add_field(
                            name=f"Invoking:",
                            value=callStatements,
                            inline=False,
                        )
                        usage = f"```\n{prefix}{command.name} "
                        for param in list(command.clean_params.items()):
                            usage += f"{param[0]} "
                        usage += "```"
                        embed.add_field(
                            name=f"Usage:",
                            value=usage,
                            inline=False,
                        )
                        break
                else:
                    return await ctx.send(
                        f"I couldn't find any category or command that you can run named *{query}*"
                    )
        else:
            embed = Embed(color=Color.blue())
            cogsDisp = ""
            for cog in self.bot.cogs:
                canRunAnyCommand = False
                for command in self.bot.get_cog(cog).get_commands():
                    try:
                        if await command.can_run(ctx):
                            canRunAnyCommand = True
                    except:
                        pass
                if canRunAnyCommand:
                    cogsDisp += f"\u2022 {cog}\n"
            embed.add_field(name=f"Categories:", value=cogsDisp, inline=False)
            embed.set_footer(text=f'Use "{prefix}help <Category>" to get more info')
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Managment(bot))
