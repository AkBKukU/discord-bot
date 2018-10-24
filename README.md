# AkBKukU Discord Bot

A management bot for the AkBKukU Discord Guild

Note: This bot has been specifically built for use in the AkBKukU Discord guild, while it should work in other - there's no guarantee.

Pull requests are open so if you find a bug or have an idea for a new feature, feel free to open one.

---- 

### Setup (standalone):

> Requires more manual intervention.

- Install PostgreSQL & create the akbkuku_discord_bot + scehma (ours are called staging & production)
- Create the tables based on the layout in TABLES.md
- Use `pip install -r requirements.txt` to install the required modules.
- Copy bot.ini.template to bot.ini and populate the options
- Use Python3.6+ to launch the bot & wait.

### Setup (Docker):
