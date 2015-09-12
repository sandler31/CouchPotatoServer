from .main import Telegram


def autoload():
    return Telegram()


config = [{
    'name': 'telegram',
    'groups': [
        {
            'tab': 'automation',
            'list': 'watchlist_providers',
            'name': 'telegram_automation',
            'label': 'Telegram',
            'description': '<PLACEHOLDER>',
            'options': [
                {
                    'name': 'automation_enabled',
                    'default': False,
                    'type': 'enabler',
                },
                {
                    'name': 'bot_token',
                    'description': 'Your bot token. Contact <a href="http://telegram.me/BotFather">@BotFather</a> on Telegram to get one.'
                },
                {
                    'name': 'receiver_user_id',
                    'label': 'Recieving User/Group ID',
                    'description': 'Receiving user/group - notifications will be sent to this user or group. Contact <a href="http://telegram.me/myidbot">@myidbot</a> on Telegram to get an ID.'
                },
                {
                    'name': 'tg_poll_interval',
                    'label': 'Telegram poll interval',
                    'type': 'int',
                    'default': 2,
                    'unit': 'seconds',
                    'advanced': True,
                    'description': 'Your bot token. Contact <a href="http://telegram.me/BotFather">@BotFather</a> on Telegram to get one.'
                },
            ],
        },
    ],
}]
