from mmpy_bot.utils import allow_only_direct_message
from mmpy_bot.bot import respond_to

conn = psycopg2.connect("")

@respond_to('^set_username (.*)')
@allow_only_direct_message()
def set_username(message, user):
    uid = message.get_user_id()
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO rcos_creds
            (uid, username)
            VALUES (%s, %s)
            ON CONFLICT (uid)
            DO UPDATE
            SET username = EXCLUDED.username
        """, (uid, user))
    conn.commit()
    message.reply('Updated Username')


@respond_to('^set_password (.*)')
@allow_only_direct_message()
def set_password(message, pas):
    uid = message.get_user_id()
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO rcos_creds
            (uid, password)
            VALUES (%s, %s)
            ON CONFLICT (uid)
            DO UPDATE
            SET password = EXCLUDED.password
        """, (uid, user))
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
    username, password = None, None
    with conn.cursor() as cur:
        cur.execute("SELECT username, password FROM rcos_creds WHERE uid = %s", (uid))
        username, password = cur.fetchone()
    message.reply('attend: %s' % code)

