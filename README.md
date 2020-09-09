# R2D2
![img](https://img.shields.io/badge/discord-bot-blueviolet?style=for-the-badge&logo=discord)
![img](https://img.shields.io/badge/code-python-blue?style=for-the-badge&logo=python)
![img](https://img.shields.io/badge/code_style-black-black?style=for-the-badge)
<br /><br />
R2D2 is a general purpose [Discord](https://discord.com/) bot. It can manage roles, members, 
lookup and play youtube music, and more!

## Usage

### Add to your server
Add [R2D2](https://discord.com/api/oauth2/authorize?client_id=751926044960882829&permissions=8&scope=bot) to your server.

### Commands

All commands are prefixed with a dot "." <br />
```
Basic:
        help   display this help message
        r2d2   share r2d2 to a server
      invite   invite url for this server
         all   mention @everyone

Misc:
       8ball   ask a question, get a prediction
        ping   get the bot latency
        rand   mention a random member

Roles:
       roles   list, add or remove roles

Music:
        play   look up and play music
       pause   pause music
        stop   stop music
  disconnect   disconnect from voice channel

Members (admin only):
         ban   ban member
       unban   unban user
 create_role   create a role
```

## Deploy your own

Create a discord [application](https://discordpy.readthedocs.io/en/latest/discord.html). <br />
Create a [heroku](https://heroku.com) account. <br />

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/dferndz/r2d2)

#### Dependencies

This bot uses ffmpeg and opus library. Both must be install for the Music Cog to work. <br />
Using the Deploy to Heroku button will automatically install both requirements to heroku. <br /><br />
If necessary, the buildpacks to install such requirements are: <br />
```
# ffmpeg
https://github.com/jonathanong/heroku-buildpack-ffmpeg-latest.git

# opus
https://github.com/xrisk/heroku-opus.git
```

## Run locally

Clone the repo. <br />
Install requirements.txt ```pip install -r requirements.txt``` <br /><br />
Add env variables:
```
export BOT_TOKEN=your_discord_bot_token
export CLIENT_ID=your_discord_app_client_id
```
Run ```python main.py```
