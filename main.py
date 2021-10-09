from discord.ext import commands
import os
import json

root = os.path.dirname(os.path.abspath(__file__)).replace("\\", "/")


def createIfNotExist(file, value):
    if not os.path.isfile(file):
        with open(file, "x") as f:
            f.write(json.dumps(value, indent=2))


dataJSON = f"{root}/files/data.json"
usedwordsJSON = f"{root}/files/usedwords.json"
createIfNotExist(dataJSON, {"prefix": "."})
createIfNotExist(usedwordsJSON, [])


def prefixGenerator(bot, msg):
    with open(dataJSON) as f:
        prefix = json.load(f)["prefix"]
    return prefix


bot = commands.Bot(command_prefix=prefixGenerator, help_command=None)

for file in os.listdir(f"{root}/cogs"):
    if file.endswith(".py") and file != "__init__.py":
        bot.load_extension(f"cogs.{file[:-3]}")


@bot.event
async def on_ready():
    print("Ready")


@bot.event
async def on_command_error(ctx, err):
    print(err)


tokenFile = f"{root}/files/token.txt"
if os.path.isfile(tokenFile):
    with open(tokenFile) as f:
        TOKEN = f.readline()
    if TOKEN:
        bot.run(TOKEN)
    else:
        print("Please specify token in files/token.txt")
else:
    with open(tokenFile, "x"):
        pass
    print("Please specify token in files/token.txt")
