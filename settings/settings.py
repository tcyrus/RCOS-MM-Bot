import os

SSL_VERIFY = True
BOT_URL = 'https://chat.rcos.io/api/v4'
BOT_LOGIN = os.environ.get('MATTERMOST_BOT_LOGIN', '')
BOT_PASSWORD = os.environ.get('MATTERMOST_BOT_PASSWORD', '')
BOT_TOKEN = None
BOT_TEAM = 'rcos'
PLUGINS = ['plugins']

os.environ['MATTERMOST_BOT_SETTINGS_MODULE'] = 'settings.settings'