# R2D2
R2D2 is a [Discord](https://discord.com/) bot.

## Usage

### Add to your server
Add [R2D2](https://discord.com/api/oauth2/authorize?client_id=751926044960882829&permissions=8&scope=bot) to your server.

### Commands

All commands are prefixed with a dot "." <br />
```
Basic: 
        .help   shows all commands  
Misc: 
       .8ball   ask a question
        .ping   get the bot latency
Roles: 
       .roles   list, add or remove roles
```

## Deploy your own

Create a discord [application](https://discordpy.readthedocs.io/en/latest/discord.html). <br />
Create a [heroku](https://heroku.com) account. <br />

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/dferndz/r2d2)

## Run locally

Clone the repo. <br />
Install requirements.txt ```pip install -r requirements.txt``` <br /><br />
Add env variables:
```
export BOT_TOKEN=your_discord_bot_token
```
Run ```python main.py```
