from mmpy_bot.utils import allow_only_direct_message
from mmpy_bot.bot import respond_to
from mmpy_bot import settings

from syncasync import async_to_sync

import logging
import asyncpg
import aiohttp


@respond_to('^set_password (.*)')
@allow_only_direct_message()
@async_to_sync
async def set_password(message, pas):
    uid = message.get_user_id()

    async with asyncpg.connect() as conn:
        async with conn.transaction():
            await conn.execute('''
                INSERT INTO rcos_creds
                (uid, password)
                VALUES ($1, pgp_sym_encrypt($2, $3 || $1))
                ON CONFLICT (uid)
                DO UPDATE
                SET password = EXCLUDED.password
            ''', uid, pas, settings.BOT_SECRET)

    message.react('+1')


@respond_to('^clear_creds')
@allow_only_direct_message()
@async_to_sync
async def set_username(message):
    uid = message.get_user_id()

    async with asyncpg.connect() as conn:
        async with conn.transaction():
            await conn.execute('DELETE FROM rcos_creds WHERE uid = $1', uid)

    message.react('+1')


@respond_to('^attend (.*)')
@allow_only_direct_message()
@async_to_sync
async def attend(message, code):
    uid = message.get_user_id()
    email = message.get_user_mail()

    password = None
    async with asyncpg.connect() as conn:
        async with conn.transaction():
            password = await conn.fetch('''
                SELECT
                pgp_sym_decrypt(password, $2 || $1)
                FROM rcos_creds
                WHERE uid = $1
            ''', uid, settings.BOT_SECRET)


    async with aiohttp.ClientSession() as session:
        token = None
        async with session.post(
            'https://rcos.io/auth/local',
            json={'email': email, 'password': password}) as r1:
            token = (await r1.json())['token']

        password = None

        logging.info(f'User "{email}" obtained token "{token}"')

        result = None
        async with session.post(
            'https://rcos.io/api/attendance/attend',
            cookies={'token': token},
            json={'dayCode': code}) as r2:
            result = await r2.text()

        logging.info(f'User "{email}" req: "{result}"')

    logging.info(f'User "{email}" submitted dayCode "{code}"')

    message.comment(result)
