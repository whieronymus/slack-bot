import waffle.bot
import zora.zora
import logging
import os


def main():
    logging.basicConfig(level=logging.INFO)
    waffle.bot.Bot(os.environ.get("SLACK_TOKEN_WAFFLE"))  # Waffle
    zora.zora.main()  # Zora

if __name__ == "__main__":
    main()
