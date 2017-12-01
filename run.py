import ravenbot.bot
import zora.zora
import os


def main():
    ravenbot.bot.Bot(os.environ.get("SLACK_TOKEN_WAFFLE"))  # Waffle
    zora.zora.main()  # Zora

if __name__ == "__main__":
    main()
