from settings import settings
from mmpy_bot import bot

import logging


class RcosBot(bot.Bot):
    def __init__(self):
        self._client = bot.MattermostClient(
            settings.BOT_URL,
            settings.BOT_TEAM,
            settings.BOT_LOGIN,
            settings.BOT_PASSWORD,
            settings.SSL_VERIFY
        )
        self._plugins = bot.PluginsManager()
        self._plugins.init_plugins()
        self._dispatcher = bot.MessageDispatcher(self._client, self._plugins)


if __name__ == '__main__':
	logging.basicConfig(level=logging.INFO)
    RcosBot().run()
