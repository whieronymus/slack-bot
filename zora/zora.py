import os
import time
from slackclient import SlackClient
import pdb


# starterbot's ID as an environment variable
BOT_ID = os.environ.get("BOT_ID")
SLACK_TOKEN = os.environ.get("SLACK_TOKEN")
AT_BOT = "<@" + BOT_ID + ">"
EXAMPLE_COMMAND = "do"

# instantiate Slack
slack_client = SlackClient()


def handle_command(command, channel):
    """
        Receives commands directed at the bot and determines if they
        are valid commands. If so, then acts on the commands. If not,
        returns back what it needs for clarification.
    """
    response = "Not sure what you mean. Use the *" + EXAMPLE_COMMAND + \
               "* command with numbers, delimited by spaces."
    if command.startswith(EXAMPLE_COMMAND):
        response = "Sure...write some more code then I can do that!"

    if command.startswith("ditto"):
        response = command.replace("ditto", "")

    if command.startswith("startproject"):
        project_os = command.split()[1]
        if project_os == "windows":
            response = "These are the commands to start a new Windows Project"
        elif project_os == "mac":
            response = "Different start project commands for mac"
        elif project_os == "linux":
            response = "Linux commands for new project"
        else:
            response = "Sorry, I only know Mac, Linux and Windows I don't know what {} is".format(project_os)

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


if __name__ == "__main__":
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
