import logging
from settings import settings
from mmpy_bot import bot


logging.basicConfig(**{
    'format': '[%(asctime)s] %(message)s',
    'datefmt': '%m/%d/%Y %H:%M:%S',
    'level': logging.INFO,
})


class RcosBot(bot.Bot):
    async def __init__(self):
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
    RcosBot().run()
