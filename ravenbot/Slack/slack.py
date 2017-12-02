import os
from slackclient import SlackClient
from functools import partial
import threading
import time
import urllib.request
import json
import re
import pdb
import inspect
import logging


class SlackCommand:
    """Decorate a function as a new command

    Keyword arguments:
    name -- the name of the command (default None)
    """
    commands = {}

    def __init__(self, name=None):
        self.name = name

    def __call__(self, f):
        if self.name is None:
            self.name = f.__name__  # Get the name of the decorated function
            self.commands[self.name] = f
        return f


class Context:
    """Get the context of a command

    Arguments:
    bot -- the slack bot
    command -- the command invoked
    """
    def __init__(self, bot, command):
        self.bot = bot
        self.command = command
        self.command_name = None
        self.callback = None

    def send(self, content):
        self.bot.send_message(channel=self.command.get("channel"), content=content)


class SlackBot(SlackClient):
    """Initialize a slack bot

    Arguments:
    key -- the bot's token

    Keyword Arguments:
    prefix -- the bot command prefix (default ?)
    """
    def __init__(self, key, prefix="?"):
        super().__init__(key)  # Initialize the bot with the token
        self.prefix = prefix
        self.read_incomming_thread = threading.Thread(target=self.read_messages)
        self.read_incomming_thread.start()  # Start reading all incoming messages
        self.events = {"channel_archive": self.on_channel_archive,  # All the events which can happen
                       "channel_created": self.on_channel_create,
                       "channel_deleted": self.on_channel_delete,
                       "channel_joined": self.on_channel_join,
                       "channel_left": self.on_channel_leave,
                       "channel_marked": self.on_channel_marked,
                       "channel_rename": self.on_channel_rename,
                       "commands_changed": self.on_commands_change,
                       "emoji_changed": self.on_emoji_change,
                       "file_created": self.on_file_create,
                       "file_deleted": self.on_file_delete,
                       "group_joined": self.on_group_join,
                       "group_left": self.on_group_leave,
                       "group_marked": self.on_group_marked,
                       "group_rename": self.on_group_rename,
                       "member_joined_channel": self.on_member_join_channel,
                       "member_left_channel": self.on_member_leave_channel,
                       "message": self.on_message,
                       "team_join": self.on_member_join_team,
                       "hello": self.on_ready}
        self.__logger = logging.getLogger(__name__)

    def send_message(self, channel, content):
        """Send a message to a channel

        Arguments:
        channel -- the slack channel ID
        content -- the message text to send
        """
        self.rtm_send_message(channel, content)
        self.__logger.debug("Sent a message to {}: {}".format(channel, content))

    def parse_output(self, output_list):
        """Parse the output of a self.rtm_read() method

        Arguments:
        output_list -- the response from self.rtm_read()
        """
        if output_list:
            for output in output_list:
                event_function = self.events.get(output.get("type"))
                if event_function:
                    event_function(**output)
                self.__logger.debug(output)

    def get_command(self, command_name):
        c = {"name": command_name, "callback": SlackCommand.commands.get(command_name)}
        return c

    def read_messages(self):
        """Continuously recieve new messages"""
        if self.rtm_connect():
            while True:
                self.parse_output(self.rtm_read())  # Get message from output
                time.sleep(0.1)  # 0.2 Second interval between checking messages

    def get_usage(self, command):
        args_spec = inspect.getargspec(command.get("callback"))  # Get arguments of command
        args_info = []
        [args_info.append("".join(["<", arg, ">"])) for arg in args_spec.args[1:]]  # List arguments
        if args_spec.defaults is not None:
            for index, default in enumerate(args_spec.defaults):  # Modify <> to [] for optional arguments
                default_arg = list(args_info[-(index + 1)])
                default_arg[0] = "["
                default_arg[-1] = "]"
                args_info[-(index + 1)] = "".join(default_arg)
        if args_spec.varargs:  # Compensate for *args
            args_info.append("<" + args_spec.varargs + ">")
        args_info.insert(0, self.prefix + command.get("name"))  # Add command name to the front
        return " ".join(args_info)  # Return args

    def on_message(self, **message):
        """This method is ran every time a message is sent"""
        user = self.api_call("users.info", user=message.get("user"))
        channel = self.api_call("channels.info", channel=message.get("channel"))
        if user and channel and message.get("text"):
            self.__logger.info("({}) {}: {}".format(channel.get("channel").get("name"),
                                                    user.get("profile").get("display_name"),
                                                    message.get("text")))
        if message.get("text").startswith(self.prefix):
            message["args"] = message.get("text").split()
            self.on_command(message)

    def on_ready(self, **output):
        """This method is when the bot is ready and reading messages"""
        print(output.get("type"))

    def on_command(self, command):
        """This method is ran every time a command is sent"""
        cmd = command.get("args")[0][len(self.prefix):]  # Get the command w/o prefix
        args = command.get("args")[1:]
        if cmd in SlackCommand.commands:  # If the command is an actual command
            ctx = Context(self, command)  # Get the context of the command
            cmd_function = SlackCommand.commands.get(cmd)
            ctx.command["callback"] = cmd_function
            ctx.command["name"] = cmd
            ctx.command_name = cmd
            try:
                cmd_function(ctx, *args)  # Invoke the command
            except TypeError:
                ctx.send("Invalid Syntax: `" + self.get_usage(ctx.command) + "`")

    def on_channel_archive(self, **output):
        """A channel was archived"""
        pass

    def on_channel_create(self, **output):
        """A channel was created"""
        pass

    def on_channel_delete(self, **output):
        """A channel was deleted"""
        pass

    def on_channel_join(self, **output):
        """You joined a channel"""
        pass

    def on_channel_leave(self, **output):
        """You left a channel"""
        pass

    def on_channel_marked(self, **output):
        """Your channel read marker was updated"""
        pass

    def on_channel_rename(self, **output):
        """A channel was renamed"""
        pass

    def on_commands_change(self, **output):
        """A slash command has been added or changed"""
        pass

    def on_emoji_change(self, **output):
        """A custom emoji has been added or changed"""
        pass

    def on_file_create(self, **output):
        """A file was created"""
        pass

    def on_file_delete(self, **output):
        """A file was deleted"""
        pass

    def on_group_join(self, **output):
        """You joined a private channel"""
        pass

    def on_group_leave(self, **output):
        """You left a private channel"""
        pass

    def on_group_marked(self, **output):
        """A private channel read marker was updated"""
        pass

    def on_group_rename(self, **output):
        """A private channel was renamed"""
        pass

    def on_member_join_channel(self, **output):
        """A user joined a public or private channel"""
        pass

    def on_member_leave_channel(self, **output):
        """A user left a public or private channel"""
        pass

    def on_member_join_team(self, **output):
        """A new member has joined"""
        pass
