# Tech Tangents Discord Bot

A management & verification bot for the Tech Tangents Discord Server.
By [Ave](https://gitlab.com/a) & [Nev](https://github.com/nevexo)


This bot is mainly used for user-verification on the Tech Tangents Discord. It includes some
other moderation commands, such as a prune command. 

The bot also contains a word filter, that can be disabled by removing the regex field
from `config.py`.

---- 

### Configuration

The config.py.template file contains all the required elements for the bot to operate.

Copy this file to `config.py`, and modify the following:

- Prefix: Set your own prefix that isn't used by any other bots
- Enter your bot's token
- Add your guild ID to the whitelist array
- Add your verification channel to `clean_channels` if you wish to use the verification system.
- Set specific commands allowed in your verification channel with `allowed_clean_commands`
- Set your regexs for filtering.
- Add the ID of any administrative roles in your server.
- Set various other verification flags at the bottom.


### Setup - Docker

This is the easiest way to get the bot working, if you have compose simply run:

`docker-compose up -d`

The bot will be built & start running in the background.

Without docker-compose, you can run the following commands to build & deploy the bot;

```
docker build -t akbk-bot .
docker run -d --name "akbkuku-discord-bot" -v $(pwd)/config.py:/bot/config.py akbk-bot
``` 

This will create the Docker image from the repo and then start a new container named
"akbkuku-discord-bot" with the config.py file mapped through (meaning you can modify
the config and simply restart the container to reload it)

### Setup - Manual

If you'd rather install the bot without Docker, you can use the following commands;

```
pip3 install -r requirements.txt
python3 AkBBot.py
```

You'll probably want to find a daemon to use, such as Systemd to ensure the bot
starts at boot time & recovers from any crashes.