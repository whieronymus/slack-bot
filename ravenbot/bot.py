from ravenbot.Slack.slack import SlackBot, SlackCommand
import requests
import json


class Bot(SlackBot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.welcome_channel = "#greeters"

    @SlackCommand()
    def ping(ctx):
        """Pong!"""
        ctx.send(":table_tennis_paddle_and_ball: Pong!")

    @SlackCommand()
    def help(ctx, command=None):
        """Get a list of commands or extra information"""
        if command in SlackCommand.commands:  # If command specified exists
            cmd = ctx.bot.get_command(command)  # Get the command
            help_info = "*Description:* " + cmd.get("callback").__doc__  # Description is docstring
            help_info += "\n*Usage:* `" + ctx.bot.get_usage(cmd) + "`"  # Get usage
        else:
            help_info = "*--------------------- Help Commands ---------------------*"
            for cmd in SlackCommand.commands:
                help_info += "\n• `" + cmd + "`"  # List commands
            help_info += "\n\n Type `help <command>` for more info on that command"
        ctx.send(help_info)

    @SlackCommand()
    def joke(ctx):
        """Tell me a joke!"""
        response = requests.get("https://icanhazdadjoke.com/", headers={"Access: ": "application/json"})
        json_load = json.loads(response.text)
        if json_load.get("status") == 200:
            ctx.send(json_load.get("joke"))

    def on_member_join_team(self, **output):
        user = output.get("user").get("profile")
        self.send_message(self.welcome_channel, "{} has joined ClubPython @here".format(user.get("display_name")))
