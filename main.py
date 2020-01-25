from mmpy_bot import bot
from mmpy_bot import settings
from mmpy_bot.scheduler import schedule


from syncasync import sync_to_async


import logging
import asyncio

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

    async def run(self):
        self._plugins.init_plugins()
        self._dispatcher.start()
        await asyncio.gather(
            asyncio.create_task(self._keep_active()),
            asyncio.create_task(self._run_jobs()),
            sync_to_async(self._dispatcher.loop)()
        )

    async def _keep_active(self):
        logging.info('keep active thread started')
        while True:
            await asyncio.sleep(60)
            self._client.ping()

    async def _run_jobs(self):
        logging.info('job running thread started')
        while True:
            await asyncio.sleep(settings.JOB_TRIGGER_PERIOD)
            schedule.run_pending()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    loop = asyncio.get_event_loop()
    bot = AsyncBot()
    loop.run_until_complete(bot.run())
