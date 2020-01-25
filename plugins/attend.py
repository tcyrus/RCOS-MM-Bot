from mmpy_bot.utils import allow_only_direct_message
from mmpy_bot.bot import respond_to
from mmpy_bot import settings

import logging
import psycopg2

conn = psycopg2.connect("")


@respond_to('^set_password (.*)')
@allow_only_direct_message()
def set_password(message, pas):
    uid = message.get_user_id()
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO rcos_creds
            (uid, password)
            VALUES (
                %(uid)s,
                pgp_sym_encrypt(%(pass)s, %(secret)s || %(uid)s)
            )
            ON CONFLICT (uid)
            DO UPDATE
            SET password = EXCLUDED.password
        """, {'uid': uid, 'pass': pas, 'secret': settings.BOT_SECRET})
    conn.commit()
    message.reply('Update Password')


@respond_to('^clear_creds')
@allow_only_direct_message()
def set_username(message):
    uid = message.get_user_id()
    with conn.cursor() as cur:
        cur.execute("DELETE FROM rcos_creds WHERE uid = %s", (uid))
    conn.commit()
    message.reply('Cleared Credentials')


@respond_to('^attend (.*)')
@allow_only_direct_message()
def attend(message, code):
    uid = message.get_user_id()
    email = message.get_user_mail()
    password = None
    with conn.cursor() as cur:
        cur.execute("""
            SELECT
            pgp_sym_decrypt(password, %(secret)s || %(uid)s)
            FROM rcos_creds
            WHERE uid = %(uid)s
        """, {'uid': uid, 'secret': settings.BOT_SECRET})
        password = cur.fetchone()

    token = requests.post(
        'https://rcos.io/auth/local',
        data={'email': email, 'password': password}
    ).json()['token']

    password = None

    logging.info(f'User "{email}" obtained token "{token}"')

    r = requests.post(
        "https://rcos.io/api/attendance/attend",
        data={'dayCode': code},
        cookies={'token': token}
    )

    logging.info(f'User "{email}" submitted dayCode "{code}"')

    logging.info(f'User "{email}" req: "{r.text}"')

    message.reply(f'attend: {code}')

