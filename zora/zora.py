import os
import time
from slackclient import SlackClient
from collections import defaultdict
import pdb

# starterbot's ID as an environment variable
BOT_ID = os.environ.get("BOT_ID")
SLACK_TOKEN = os.environ.get("SLACK_TOKEN")
AT_BOT = "<@" + BOT_ID + ">"

# instantiate Slack
slack_client = SlackClient(SLACK_TOKEN)


def ditto_cmd(cmd):
    return " ".join(cmd.split()[1:])


def startproject_cmd(cmd):
    project_os = cmd.split()[1]
    if project_os == "windows":
        response = "These are the commands to start a new Windows Project"
    elif project_os == "mac":
        response = "Different start project commands for mac"
    elif project_os == "linux":
        response = "Linux commands for new project"
    else:
        response = "Sorry, I only know Mac, Linux and Windows I don't know what {} is".format(project_os)
    return response


def help_cmd(cmd):
    split = cmd.split()
    if len(split) == 1:
        lines = ["{}: {}".format(cmd.name, cmd.help_text) for cmd in Command.get.values()]
    elif split[1] in Command.get:
        lines = ["{}: {}".format(Command.get[split[1]].name, Command.get[split[1]].help_text)]
    else:
        lines = ["Sorry, this command is not found."]
    return "\n".join(lines)


class Command:
    get = defaultdict(lambda: None)

    def __init__(self, func, name, help_text):
        self.func = func
        self.name = name
        self.help_text = help_text
        Command.get[name] = self

    def execute(self, message):
        return self.func(message)


def handle_command(text, channel):
    """
        Receives commands directed at the bot and determines if they
        are valid commands. If so, then acts on the commands. If not,
        returns back what it needs for clarification.
    """

    cmd_name = text.split()[0]

    cmd = Command.get[cmd_name]

    if cmd:
        response = cmd.execute(text)
    else:
        response = "Sorry, I have not been trained to do that yet."

    slack_client.api_call("chat.postMessage", channel=channel,
                          text=response, as_user=True)


def parse_slack_output(slack_rtm_output):
    """
        The Slack Real Time Messaging API is an events firehose.
        this parsing function returns None unless a message is
        directed at the Bot, based on its ID.
    """
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            if output and 'text' in output and AT_BOT in output['text']:
                # return text after the @ mention, whitespace removed
                command = output['text'].split(AT_BOT)[1].strip().lower()
                channel = output['channel']
                return command, channel

            print(output)
    return None, None


def define_commands():
    Command(ditto_cmd,
            "ditto",
            "Repeats said text")
    Command(startproject_cmd,
            "startproject",
            "How to start a project on different OS's")
    Command(help_cmd,
            "help",
            "Displays help for given command or all if none given.")


if __name__ == "__main__":
    define_commands()

    READ_WEBSOCKET_DELAY = 1  # 1 second delay between reading from firehose
    if slack_client.rtm_connect():
        print("StarterBot connected and running!")
        while True:
            command, channel = parse_slack_output(slack_client.rtm_read())
            if command and channel:
                handle_command(command, channel)
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed. Invalid Slack token or bot ID?")

# ----vv---- used for local testing

# if __name__ == "__main__":
#     define_commands()
#
#     def a(x, **kwargs):
#         print(kwargs["text"])
#
#     slack_client.api_call = a
#
#     while True:
#         handle_command(input("Enter the command:  "), "a")

