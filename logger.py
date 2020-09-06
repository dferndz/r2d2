import datetime


def log(msg):
    print(f"[{datetime.datetime.now()}] {msg}")


def log_ctx(ctx):
    log(f"{ctx.author} sent '{ctx.message.content}'")


def log_msg(message):
    log(f"{message.author} sent '{message.content}'")
