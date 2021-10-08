from discord import Embed
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
        embed = Embed()
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

    @commands.command(aliases=["w"])
    async def word(self, ctx: commands.Context, *, word: str = None):
        if word:
            word = word.upper()
        else:
            with open(f"{root}/files/words.json") as f:
                words = json.load(f)
            with open(f"{root}/files/usedwords.json") as f:
                usedWords = json.load(f)
            words = [word for word in words if not word in usedWords]
            word = random.choice(words).upper()
            usedWords.append(word)
            with open(f"{root}/files/usedwords.json", "w") as f:
                json.dump(usedWords, f, indent=2)
        self.currentWord = word
        print(word)
        await ctx.send("", embed=self.createEmbed())

    @commands.command(aliases=["g"])
    async def guess(self, ctx: commands.Context, guess: str):
        guess = guess.upper()
        if len(guess) < 2:
            self.guessedLetters.append(guess)
            if not guess in self.currentWord:
                self.wrongLetters.append(guess)
                self.attempts -= 1
        else:
            if guess != self.currentWord:
                return await ctx.send("That's not the word")
            await ctx.send(f"Congratulations! The words was {self.currentWord}")
            self.setDefault()
            return
        await ctx.send("", embed=self.createEmbed())


def setup(bot):
    bot.add_cog(Hangman(bot))
