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


class slackcommand:
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
        self.commands = {}
        self.prefix = prefix
        self.read_incomming_thread = threading.Thread(target=self.read_messages)
        self.read_incomming_thread.start()  # Start reading all incoming messages

    def send_message(self, channel, content):
        """Send a message to a channel

        Arguments:
        channel -- the slack channel ID
        content -- the message text to send
        """
        self.api_call("chat.postMessage", channel=channel, text=content, as_user=True)

    def on_message(self, message):
        """This method is ran every time a message is sent"""
        pass

    def on_ready(self):
        """This method is when the bot is ready and reading messages"""
        pass

    def on_command(self, command):
        """This method is ran every time a command is sent"""
        cmd = command.get("args")[0][len(self.prefix):]  # Get the command w/o prefix
        args = command.get("args")[1:]
        if cmd in slackcommand.commands:  # If the command is an actual command
            ctx = Context(self, command)  # Get the context of the command
            cmd_function = slackcommand.commands.get(cmd)
            ctx.callback = cmd_function
            ctx.command["callback"] = cmd_function
            ctx.command["name"] = cmd
            ctx.command_name = cmd
            try:
                cmd_function(ctx, *args)  # Invoke the command
            except TypeError:
                ctx.send("Invalid Syntax: `" + self.get_usage(ctx.command) + "`")

    def parse_output(self, output_list):
        """Parse the output of a self.rtm_read() method

        Arguments:
        output_list -- the response from self.rtm_read()
        """
        if output_list:
            for output in output_list:
                if output.get("type") == "message":
                    content = output.get("text")
                    channel = output.get("channel")
                    author = output.get("user")
                    timestamp = output.get("ts")
                    return {"content": content, "channel": channel, "author": author, "ts": timestamp}
        return None  # If there is no messages

    def get_command(self, command_name):
        d = {"name": command_name, "callback": slackcommand.commands.get(command_name)}
        return d

    def read_messages(self):
        """Continuously recieve new messages"""
        if self.rtm_connect():
            self.on_ready()
            while True:
                msg = self.parse_output(self.rtm_read())  # Get message from output
                if msg:
                    if msg.get("content").startswith(self.prefix):  # If message starts with prefix
                        msg["args"] = msg.get("content").split()
                        self.on_command(msg)
                    self.on_message(msg)
                time.sleep(0.2)  # 0.2 Second interval between checking messages

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
        if args_spec.varargs:
            args_info.append("<" + args_spec.varargs + ">")
        args_info.insert(0, self.prefix + command.get("name")) # Add command name to the front
        return " ".join(args_info) # Return args
