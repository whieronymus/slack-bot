from .Slack.slack import SlackBot, SlackCommand
from .Slack.attachments import Attachment
import requests
import json
import logging
import os
from pytz import timezone
from datetime import datetime
from fuzzywuzzy import process

GITHUB_TAGS_SOURCES = "whieronymus/slack-bot/waffle/sources"


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
    def tag(context, *query):
        """Get useful information with tags"""
        query = " ".join(w.lower() for w in query)
        path = GITHUB_TAGS_SOURCES.split("/")
        path.insert(2, "contents")  # tell github we want the contents of this path
        github_path = "https://api.github.com/repos/" + "/".join(path)  # reconstruct the path into a github api query
        response = requests.get(github_path)
        items = response.json()
        matches = process.extract(query,
                                  map(lambda i: i.get("name").replace(".md", "").lower(), items))
        best_matches = list(filter(lambda result: result[1] > 70, matches))
        if len(best_matches) > 1:
            return context.send("*Multiple matches:*" + "\n".join(best_matches))
        elif len(best_matches) < 1:
            return context.send("Couldn't find anything")
        else:
            # very ugly I know, it basically just gets the item from the json which is the best match
            info = [i for i in items if i.get("name").replace(".md", "").lower() == best_matches[0][0]][0]
            title = info.get("name")
            body = requests.get(info.get("download_url")).text
            return context.send("*{}*\n\n{}".format(title, body))

    @SlackCommand()
    def joke(context):
        """Tell me a joke!"""
        response = requests.get("https://icanhazdadjoke.com/", headers={"Accept": "application/json",
                                                                        "User-Agent": "Waffle Slack Bot",
                                                                        "From": "https://github.com/whieronymus"})
        json_load = response.json()
        if json_load.get("status") == 200:
            context.send(json_load.get("joke"))

    @SlackCommand()
    def weather(context, *area):
        """What's the weather?"""
        query = " ".join(area)
        tmp_message = context.send("Retrieving information for {}".format(query))

        # Request OpenWeatherMap for information (json)
        weather_webapi = "https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&APPID={}"
        weather = weather_webapi.format(query, os.environ.get("OPENWEATHERMAP_API_KEY"))
        weather_response = requests.get(weather)
        weather_json = weather_response.json()

        # Request Google Timezone API for information (json)
        google_tz_webapi = "https://maps.googleapis.com/maps/api/timezone/json?location={},{}&timestamp={}&key={}"
        try:
            google_tz = google_tz_webapi.format(weather_json["coord"]["lat"], weather_json["coord"]["lon"],
                                                weather_json["dt"], os.environ.get("TZ_GOOGLE_API_KEY"))
        except KeyError:
            return context.send("I can't find anywhere by that name")
        google_tz_response = requests.get(google_tz)
        google_tz_json = google_tz_response.json()
        local_tz = timezone(google_tz_json.get("timeZoneId"))

        # Convert sunrise/set times to local timezone
        sunrise_dt = datetime.fromtimestamp(weather_json.get("sys").get("sunrise"))
        sunrise_time = local_tz.localize(sunrise_dt)
        sunset_dt = datetime.fromtimestamp(weather_json.get("sys").get("sunset"))
        sunset_time = local_tz.localize(sunset_dt)
        country_code = weather_json.get("sys").get("country")

        area = weather_json.get("name")
        weather = weather_json.get("main")
        description = weather_json["weather"][0].get("description")
        icon_download_url = "http://download.spinetix.com/content/widgets/icons/weather/{}.png"
        icon = icon_download_url.format(weather_json["weather"][0].get("icon"))

        attachment = Attachment(f"Weather in {area} is: {description}")
        attachment.title = ":flag-{}: Weather in {} ({})".format(country_code, area, description)
        attachment.color = "good"
        attachment.footer = "Information provided by OpenWeatherMap"
        attachment.thumb_url = icon
        attachment.add_field(name="Temperature",
                             value="{} °C / {} °F".format(int(weather.get("temp")),
                                                          int(weather.get("temp") * 1.8 + 32)),
                             short=False)
        attachment.add_field(name="Humidity",
                             value="{}%".format(weather.get("humidity")))
        attachment.add_field(name="Sunrise & Sunset",
                             value="{} / {}".format(sunrise_time.strftime("%H:%M"),
                                                    sunset_time.strftime("%H:%M")))

        context.bot.edit_attachment(*tmp_message, attachment.data)

    def on_member_join_team(self, **output):
        """Send welcome message if a user joins"""
        user = output.get("user").get("profile")
        if user.get("display_name"):  # Check which username to use. Preferably the display name.
            username = user.get("display_name")
        else:
            username = user.get("real_name")

        self.send_message(self.welcome_channel, "{} has joined ClubPython <!here>".format(username))
        self.logger.info("New member has joined the team! ({})".format(user.get("display_name")))
