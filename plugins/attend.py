from mmpy_bot.utils import allow_only_direct_message
from mmpy_bot.bot import respond_to
from mmpy_bot import settings

from syncasync import async_to_sync

import logging
import asyncpg
import aiohttp
from splinter import Browser


@respond_to('^set_password (.*)')
@allow_only_direct_message()
@async_to_sync
async def set_password(message, pas):
    uid = message.get_user_id()

    conn = await asyncpg.connect()

    async with conn.transaction():
        await conn.execute('''
            INSERT INTO rcos_creds
            (uid, password)
            VALUES ($1, pgp_sym_encrypt($2, $3 || $1))
            ON CONFLICT (uid)
            DO UPDATE
            SET password = EXCLUDED.password
        ''', uid, pas, settings.BOT_SECRET)

    await conn.close()

    message.react('+1')


@respond_to('^clear_creds')
@allow_only_direct_message()
@async_to_sync
async def clear_creds(message):
    uid = message.get_user_id()

    conn = await asyncpg.connect()

    async with conn.transaction():
        await conn.execute('DELETE FROM rcos_creds WHERE uid = $1', uid)

    await conn.close()

    message.react('+1')


@respond_to('^attend (.*)')
@allow_only_direct_message()
@async_to_sync
async def attend(message, code):
    uid = message.get_user_id()
    email = message.get_user_mail()

    password = None
    conn = await asyncpg.connect()

    async with conn.transaction():
        password = await conn.fetchval('''
            SELECT
            pgp_sym_decrypt(password, $2 || $1)
            FROM rcos_creds
            WHERE uid = $1
        ''', uid, settings.BOT_SECRET)

    await conn.close()

    browser = Browser('remote', command_executor="selenium:4444/wd/hub")

    browser.visit('https://rcos.io/login?referrer=~2Fattend')

    if not browser.is_element_present_by_name('email', wait_time=10):
        logging.info("Login page failed to load")
        message.comment("Login page failed to load")
        return

    browser.fill_form({'email': email, 'password': password})
    browser.find_by_css('.btn-login')[0].click()

    if not browser.is_element_present_by_id('dayCodeInput', wait_time=10):
        logging.info("Login failed")
        message.comment("Login failed")
        return

    password = None

    print(browser.cookies['token'])
    token = browser.cookies['token']

    #browser.find_by_id('dayCodeInput')[0].fill(code)
    #browser.find_by_css('.dayCodeForm .btn')[0].click()

    browser.quit()

    result = ''
    async with aiohttp.ClientSession() as session:
        async with session.post(
            'https://rcos.io/api/attendance/attend',
            cookies={'token': token},
            headers={"Authorization": f"Bearer {token}"},
            json={'dayCode': code}) as r2:
            result = await r2.text()

    logging.info(f'User "{email}" submitted dayCode "{code}"')

    logging.info(f'User "{email}" req: "{result}"')

    message.react('+1')
