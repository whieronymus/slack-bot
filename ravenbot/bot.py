try:
    from ravenbot.Slack.slack import SlackBot, SlackCommand
except ImportError:
    from Slack.slack import SlackBot, SlackCommand
import requests
import json
import logging
import os
from pytz import timezone
from datetime import datetime


class Bot(SlackBot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.welcome_channel = "#greeters"
        self.logger = logging.getLogger(__name__)

    @SlackCommand()
    def ping(context):
        """Pong!"""
        context.send(":table_tennis_paddle_and_ball: Pong!")

    @SlackCommand()
    def help(context, command=None):
        """Get a list of commands or extra information"""
        if command in SlackCommand.commands:  # If command specified exists
            cmd = context.bot.get_command(command)  # Get the command
            help_info = "*Description:* " + cmd.get("callback").__doc__  # Description is docstring
            help_info += "\n*Usage:* `" + context.bot.get_usage(cmd) + "`"  # Get usage
        else:
            help_info = "*--------------------- Help Commands ---------------------*"
            for cmd in SlackCommand.commands:
                help_info += "\n• `" + cmd + "`"  # List commands
            help_info += "\n\n Type `help <command>` for more info on that command"
        context.send(help_info)

    @SlackCommand()
    def joke(context):
        """Tell me a joke!"""
        response = requests.get("https://icanhazdadjoke.com/", headers={"Accept": "application/json",
                                                                        "User-Agent": "Waffle Slack Bot",
                                                                        "From": "https://github.com/whieronymus"})
        json_load = json.loads(response.text)
        if json_load.get("status") == 200:
            context.send(json_load.get("joke"))

    @SlackCommand()
    def weather(context, *area):
        query = " ".join(area)

        # Request OpenWeatherMap for information (json)
        weather_webapi = "https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&APPID={}"
        weather = weather_webapi.format(query, os.environ.get("OPENWEATHERMAP_API_KEY"))
        weather_response = requests.get(weather)
        weather_json = json.loads(weather_response.text)

        # Request Google Timezone API for information (json)
        google_tz_webapi = "https://maps.googleapis.com/maps/api/timezone/json?location={},{}&timestamp={}&key={}"
        try:
            google_tz = google_tz_webapi.format(weather_json["coord"]["lat"], weather_json["coord"]["lon"],
                                                weather_json["dt"], os.environ.get("TZ_GOOGLE_API_KEY"))
        except KeyError:
            return context.send("I can't find anywhere by that name")
        google_tz_response = requests.get(google_tz)
        google_tz_json = json.loads(google_tz_response.text)
        local_tz = timezone(google_tz_json.get("timeZoneId"))

        # Convert sunrise/set times to local timezone
        sunrise_dt = datetime.fromtimestamp(weather_json.get("sys").get("sunrise"))
        sunrise_time = local_tz.localize(sunrise_dt)
        sunset_dt = datetime.fromtimestamp(weather_json.get("sys").get("sunset"))
        sunset_time = local_tz.localize(sunset_dt)

        area = weather_json.get("name")
        weather = weather_json.get("main")
        description = weather_json.get("weather")[0].get("description")

        information = ("> _*Weather in {} ({})*_".format(area, description),
                       "> Temperature: {} °C / {} °F".format(int(weather.get("temp")),
                                                             int(weather.get("temp") * 1.8 + 32)),  # Convert C to F
                       "> Humidity: {}%".format(weather.get("humidity")),
                       "> Sunrise and Sunset: {} / {}".format(sunrise_time.strftime("%H:%M"),
                                                              sunset_time.strftime("%H:%M")))
        context.send("\n".join(information))

    def on_member_join_team(self, **output):
        user = output.get("user").get("profile")
        self.send_message(self.welcome_channel, "{} has joined ClubPython <!here>".format(user.get("display_name")))
        self.logger.info("New member has joined the team! ({})".format(user.get("display_name")))

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    token = open("token.txt").read().strip()
    Bot(token)
