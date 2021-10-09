from discord import Embed
from discord import TextChannel
from discord.ext import commands

import os
import json
import random

from PIL import Image

acceptedLetters = [
    "A",
    "B",
    "C",
    "D",
    "E",
    "F",
    "G",
    "H",
    "I",
    "J",
    "K",
    "L",
    "M",
    "N",
    "O",
    "P",
    "R",
    "S",
    "T",
    "U",
    "W",
    "Y",
    "Z",
    "X",
    "Q",
    "V",
]

root = os.path.dirname(os.path.abspath(__file__)).replace("\\", "/") + "/.."


class Hangman(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        with open(f"{root}/files/data.json") as f:
            self.channel = json.load(f)["channel"]
        self.setDefault()

    def setDefault(self):
        self.currentWord = ""
        self.attempts = 9
        self.guessedLetters = []
        self.wrongLetters = []

    def createHangmanGraphic(self):
        im = Image.open(f"{root}/files/hangman-stages/{self.attempts}.png")
        pix = im.load()
        string = ""

        for y in range(14):
            string += "\n"
            for x in range(10):
                if pix[x, y] == (255, 255, 255):  # (255,255,255,255)
                    string += "\u2b1c"
                else:
                    string += "\u2b1b"

        return string

    def createEmbed(self):
        embed = Embed(color=65480)
        encodedWord = ""
        for letter in self.currentWord:
            encodedWord += (
                letter
                if letter in self.guessedLetters or not letter in acceptedLetters
                else "#"
            )
        embed.add_field(name="Hangman:", value=encodedWord, inline=False)
        if self.wrongLetters:
            embed.add_field(
                name="\u200b",
                value=f"Wrong letters: {', '.join(self.wrongLetters)}",
                inline=False,
            )
        if 0 <= self.attempts <= 8:
            embed.add_field(
                name="\u200b",
                value=self.createHangmanGraphic(),
                inline=False,
            )
        embed.set_footer(text=f"Attempts left: {self.attempts}")
        return embed

    def allGuessed(self):
        allGuessed = True
        for letter in self.currentWord:
            if letter in self.guessedLetters or not letter in acceptedLetters:
                continue
            allGuessed = False
            break
        return allGuessed

    async def checkForLoss(self, ctx):
        if self.attempts <= 0:
            await ctx.send(embed=self.createEmbed())
            await ctx.send(f"The word was **{self.currentWord}**")
            self.setDefault()
            return True
        return False

    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    @commands.command()
    async def setChannel(self, ctx: commands.Context, channel: TextChannel = None):
        if not channel:
            channel = ctx.channel
        with open(f"{root}/files/data.json", "r+") as f:
            dataJSON = json.load(f)
            dataJSON["channel"] = channel.id
            f.seek(0)
            json.dump(dataJSON, f, indent=2)
            f.truncate()
        self.channel = channel.id
        await ctx.send(f"{channel.mention} set as hangman channel")

    @commands.has_permissions(administrator=True)
    @commands.command()
    async def unsetChannel(self, ctx: commands.Context):
        with open(f"{root}/files/data.json", "r+") as f:
            dataJSON = json.load(f)
            dataJSON["channel"] = None
            f.seek(0)
            json.dump(dataJSON, f, indent=2)
            f.truncate()
        channel = self.bot.get_channel(self.channel)
        self.channel = None
        await ctx.send(f"{channel.mention} is no longer the hangman channel")

    @commands.has_permissions(administrator=True)
    @commands.command()
    async def clearUsedWords(self, ctx: commands.Context):
        with open(f"{root}/files/usedwords.json", "w") as f:
            f.write("[]")
        await ctx.send("Cleared used words")

    @commands.command(aliases=["w"])
    async def word(self, ctx: commands.Context, *, word: str = None):
        targetChannel = (
            self.bot.get_channel(self.channel) if self.channel else ctx.channel
        )
        if ctx.guild is None:
            if not self.channel:
                return await ctx.send(
                    "please specify hangman channel to send words in dms"
                )
        elif self.channel:
            if ctx.channel.id != self.channel:
                return await ctx.send(
                    "this command can only be used on hangman channel or in dms"
                )
        if word:
            await ctx.message.delete()
        self.setDefault()
        if word:
            if len(word) < 2:
                return await targetChannel.send(
                    "Word need to have at least two letters"
                )
            word = word.upper()
        else:
            with open(f"{root}/files/words.json") as f:
                words = json.load(f)
            with open(f"{root}/files/usedwords.json") as f:
                usedWords = json.load(f)
            words = [word for word in words if not word in usedWords and len(word) > 1]
            word = random.choice(words).upper()
            usedWords.append(word)
            with open(f"{root}/files/usedwords.json", "w") as f:
                json.dump(usedWords, f, indent=2)
        self.currentWord = word
        print(word)
        await targetChannel.send(embed=self.createEmbed())

    @commands.guild_only()
    @commands.command(aliases=["g"])
    async def guess(self, ctx: commands.Context, *, guess: str = None):
        targetChannel = (
            self.bot.get_channel(self.channel) if self.channel else ctx.channel
        )
        if self.channel and self.channel != ctx.channel.id:
            return await ctx.send("this command can only be used on hangman channel")
        if not guess:
            return await targetChannel.send(
                "guess is a required argument that is missing"
            )
        if not self.currentWord:
            return await targetChannel.send("please set the word")
        guess = guess.upper()
        if len(guess) < 2:
            if not guess in acceptedLetters:
                return await targetChannel.send(f"**{guess}** is not a letter")
            if guess in self.guessedLetters:
                return await targetChannel.send(f"**{guess}** was already guessed")
            self.guessedLetters.append(guess)
            if self.allGuessed():
                await targetChannel.send(
                    f"Congratulations {ctx.author.mention}! The word was **{self.currentWord}**"
                )
                self.setDefault()
                return
            if not guess in self.currentWord:
                self.wrongLetters.append(guess)
                self.attempts -= 1
                if await self.checkForLoss(ctx):
                    return
        else:
            if guess != self.currentWord:
                await targetChannel.send(f"**{guess}** is not the word")
                self.attempts -= 1
                if await self.checkForLoss(ctx):
                    return
            else:
                await targetChannel.send(
                    f"Congratulations {ctx.author.mention}! The word was **{self.currentWord}**"
                )
                self.setDefault()
                return
        await targetChannel.send(embed=self.createEmbed())


def setup(bot):
    bot.add_cog(Hangman(bot))
