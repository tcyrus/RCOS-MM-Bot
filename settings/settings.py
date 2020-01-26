import os

SSL_VERIFY = True
BOT_URL = 'https://chat.rcos.io/api/v4'
BOT_LOGIN = os.environ.get('MATTERMOST_BOT_LOGIN', '')
BOT_PASSWORD = os.environ.get('MATTERMOST_BOT_PASSWORD', '')
BOT_SECRET = os.environ.get('MATTERMOST_BOT_SECRET', '')
BOT_TOKEN = None
BOT_TEAM = 'rcos'
PLUGINS = ['plugins']

POSTGRES_USER = os.environ.get('PGUSER', '')
POSTGRES_PASSWORD = os.environ.get('PGPASSWORD', '')
POSTGRES_DB = os.environ.get('PGDATABASE', '')
POSTGRES_HOST = os.environ.get('PGHOST', '')
