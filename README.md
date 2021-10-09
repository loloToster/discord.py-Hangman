# discord.py Hangman Bot 🤖

This is my custom discord bot which you can play hangman with! 

## Instalation
1. Clone this repo
2. Go [here](https://discord.com/developers/applications)
3. Click on `Create New application` and give it a name
4. Go to the `Bot` tab and then click `Add Bot`
5. Copy and paste your token to `files/token.txt`
6. Go to the `OAuth2` tab. Select `bot` in scopes and `Administrator` in bot permissions
7. Click on the link that is in scopes and add bot to your server
8. Download necessary python libraries:
    * discordpy
    * Pillow
    * On Raspberry pi you will need to install some additional system libraries for image processing more info [here](https://raspberrypi.stackexchange.com/questions/104591/what-system-libraries-are-required-to-support-pillow-on-raspbian-buster-lite)
9. Run `main.py` and enjoy playing Hangman!

## Notes
* This bot is meant for **one** guild. It will not work on multiple guilds/servers
* Default prefix is `.`
* If you want to add more words to list of random words just add them to `files/words.json` file
