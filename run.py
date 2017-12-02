import ravenbot.bot
import zora.zora
import logging
import os


def main():
    logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(message)s")
    ravenbot.bot.Bot(os.environ.get("SLACK_TOKEN_WAFFLE"))  # Waffle
    zora.zora.main()  # Zora

if __name__ == "__main__":
    main()
