from discord.ext.commands import CommandError


COMMAND_NOT_FOUND_RESPONSE = (
    "Hmm, I don't know what that means. Type '.help' to get a list of commands."
)
INTERNAL_ERROR_RESPONSE = "Something went wrong."


class BaseUserError(CommandError):
    def __init__(self, message="Sorry, something went wrong!", private=False):
        self.message = message
        self.private = private
        super().__init__(self.message)


class OutOfServer(BaseUserError):
    def __init__(self, message="You must call this command from a server!", **kwargs):
        self.message = message
        super().__init__(self.message, **kwargs)


class InvalidArgs(BaseUserError):
    def __init__(self, message="Missing arguments.", **kwargs):
        self.message = message
        super().__init__(self.message, **kwargs)


class PermissionDenied(BaseUserError):
    def __init__(self, message="Permission denied.", **kwargs):
        self.message = message
        super().__init__(self.message, **kwargs)


class OutOfVoiceChannel(BaseUserError):
    def __init__(self, message="You must be in a voice channel.", **kwargs):
        self.message = message
        super().__init__(self.message, **kwargs)
