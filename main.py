from mmpy_bot import bot
from mmpy_bot import settings
from mmpy_bot.scheduler import schedule


from syncasync import sync_to_async


import logging

class AsyncBot(bot.Bot):
    def __init__(self):
        self._client = bot.MattermostClient(
            settings.BOT_URL,
            settings.BOT_TEAM,
            settings.BOT_LOGIN,
            settings.BOT_PASSWORD,
            settings.SSL_VERIFY
        )
        self._plugins = bot.PluginsManager()
        self._dispatcher = bot.MessageDispatcher(self._client, self._plugins)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    AsyncBot().run()
