import os
import discord
import asyncio
import threading

TOKEN = os.environ["BOT_TOKEN"]
client = discord.Client()


def print_guilds():
    print("\nCurrent servers:")
    print("----------------")
    for guild in client.guilds:
        print(f"    {guild}")
    print("")


def print_help():
    print("\nCommands:")
    print("----------------")
    print("     help        - show this message")
    print("     exit        - close the connection")
    print("     guilds      - list all servers")
    print("")


commands = dict(guilds=print_guilds, help=print_help,)


def do_action(cmd: str):
    if cmd in commands:
        commands[cmd]()
    else:
        print("Invalid command. Use 'help' for a list of available commands")


async def start():
    await client.start(TOKEN)


def run_it_forever(loop):
    loop.run_forever()


def init():
    print("Connecting to bot...")

    loop = asyncio.get_event_loop()
    loop.create_task(start())

    thread = threading.Thread(target=run_it_forever, args=(loop,))
    thread.start()

    while not client.is_ready():
        pass

    print(f"🤖 Connected to {client.user.name}")

    command = ""

    while command != "exit":
        print(f"{client.user.name} $ ", end="")
        command = input()
        if command != "exit":
            do_action(command)

    print("Closing connection...")
    loop.stop()
    thread.join()
    print("❌ Disconnected")


init()
