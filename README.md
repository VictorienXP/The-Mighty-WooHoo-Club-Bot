# The Mighty WooHoo Club Bot

This bot is custom made for The Mighty WooHoo Club Discord server.

## Setup

Dependencies are [discord.py](https://pypi.org/project/discord.py/), [discord-py-slash-command](https://pypi.org/project/discord-py-slash-command/) and [webcolors](https://pypi.org/project/webcolors/).

```sh
pip3 install discord.py
pip3 install discord-py-slash-command
pip3 install webcolors
```

This bot uses [Discord slash commands](https://discord.com/developers/docs/interactions/slash-commands).
And will obviously require the permission to manage roles on the Discord server.

Create a `config.json` based on `config-example.json` and fill in the details.

Invite the bot on your server of choice with that invite link for example:
`https://discord.com/oauth2/authorize?client_id=YOUR_CLIENT_ID_HERE&permissions=2617557056&scope=bot%20applications.commands`

You can start the bot with `python3 main.py`.
