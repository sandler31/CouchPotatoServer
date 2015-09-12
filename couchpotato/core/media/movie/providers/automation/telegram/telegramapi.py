import os
import requests

class TelegramApi:
    """
    This class implements function of the Telegram Bot API needed
    for Telegram Automation to work
    """
    def __init__(self, api_key):
        # TODO: API Init stuff?
        raise NotImplementedError
        pass

    def reply_message(self, chat_id, msg, keyboard=None, reply_to_id=None):
        # TODO: Send a message
        # TODO: Reply with keyboard
        # TODO: Reply with hide keyboard
        # TODO: Send message as reply to specific message ID
        raise NotImplementedError
        pass

    def reply_sticker(self, chat_id, sticker_id):
        # TODO: Send a sticker
        raise NotImplementedError
        pass

    def reply_photo(self, chat_id, photo_file_path=None, photo_file=None, photo_id=None, reply_to_id=None):
        # TODO: Read photo (from memory? from file?)
        # TODO: Send photo as reply to specific message
        # TODO: Send photo
        raise NotImplementedError
        pass

    def get_updates(self):
        # TODO: Get messages from server
        # TODO: Store last message (offset calc, to make messages as read on server)
        raise NotImplementedError
        pass

    def listen_msg(self):
        # TODO: Listen for messages
        # TODO: Call the callback function when message is received (synchronous?)
        raise NotImplementedError
        pass