import os, sys
import requests, json
from six import string_types
from couchpotato.core.logger import CPLog #~

log = CPLog(__name__) #~

class TelegramApiException(Exception):
    pass

class TelegramApi:
    """
    This class implements function of the Telegram Bot API needed
    for Telegram Automation to work
    """
    API_URL =       'https://api.telegram.org/bot%s/%s' # Telegram API URL (https://url/bot<TOKEN>/function)
    api_key =       None                                # Bot API access key
    offset  =       -1                                  # Offset from last message

    def __init__(self, api_key):
        # TODO: API Init stuff?
        self.api_key = api_key

    def _send_api_message(self, method, chat_id=None, data=None, files=None):
        """
        This function issues an API message to Telegram's servers
        * method: Telegram method to call
        * chat_id: recepient chat id
        * data: data to be provided along with the method to the Telegram API
        * files: files to be provided with the data, if needed
        """
        # Build request
        req_url = self.API_URL % (self.api_key, method)

        req_data = {'chat_id': chat_id}
        req_data.update(data)

        # Issue request
        resp = None
        try:
            resp = requests.post(req_url, data=req_data, files=files)
        except:
            log.error('Exception while issuing API request to Telegram Bot API. data: data: [%s], url: [%s],\
                exception: [%s]' % (req_data, req_url, sys.exc_info()))

        # Check response, if successful return JSON object of response
        json_result = None
        if 200 != resp.status_code:
            log.error('Could not issue API request to Telegram Bot API. data: [%s], url: [%s], response: [%s]'\
             % (req_data, req_url, resp.text))
        else:
            json_result = json.loads(resp.text) 

        # Check result
        if None != json_result:
            if True != json_result['ok']:
                log.error('Server did not return "ok" on sent message. response: [%s]'\
                    % json_result)
            else:
                return json_result

        # We didn't get a valid response
        return None

    def reply_message(self, chat_id, msg, keyboard=None,
                        keyboard_hide=None, one_time_keyboard=True, reply_to_id=None):
        """
        This method allows to send a message to a Telegram user
        * chat_id: recepient chat id
        * msg: message to send
        * keyboard: a list with optional keyboard buttons to send
        * keyboard_hide: a boolean, which if set True, closes an open keyboard on
        user's Telegram chat
        * one_time_keyboard: should be used with keyboard variable, specifying to close
        the keyboard after a button click
        * reply_to_id: specifies that the message should be a reply to specific user message
        referenced by it's ID

        TODO: Allow customization of the keyboard via the object constructor for TelegramApi?
        TODO: Add cancel button to keyboards? should be created outside of this method?
        """
        telegram_method_name = 'sendMessage'

        # Build data to send
        data = {'text': msg}
        if None != keyboard:
            if isinstance(keyboard, list):
                # Create a table of buttonsf from the list, consisting of one row
                nested_keyboard = map(lambda x: keyboard[x:(x+1)], range (len(keyboard)))
                keyboard_markup = {'keyboard': nested_keyboard,
                                    'one_time_keyboard': one_time_keyboard}
                # Note, as per Telegram docs, the reply_markup should be serialized JSON (?!)
                data['reply_markup'] = json.dumps(keyboard_markup)
            else:
                raise TelegramApiException('Keyboard should be list!')
        if None != keyboard_hide:
            if None != keyboard:
                raise TelegramApiException('You can\'t hide and show the keyboard at the same time!')
            if True == keyboard_hide:
                keyboard_markup = {'hide_keyboard': True}
                data['reply_markup'] = json.dumps(keyboard_markup)
        if None != reply_to_id:
            data['reply_to_message_id'] = reply_to_id

        # Issue request
        result = self._send_api_message(telegram_method_name, chat_id, data)

    def reply_sticker(self, chat_id, sticker_id):
        """
        This method allows to send a sticker to a Telegram user, using the sticker ID
        * chat_id: recepient chat id
        * sticker_id: id of the sticker to send

        TODO: Add option to send a new sticker? possible?
        """
        telegram_method_name = 'sendSticker'

        # Build data to send
        data = {'sticker': sticker_id}

        # Issue request
        result = self._send_api_message(telegram_method_name, chat_id, data)

    def reply_photo(self, chat_id, photo, caption=None, reply_to_id=None):
        """
        This method allows sending pictures to a telegram user
        * chat_id: recepient chat id
        * photo: an open file handle, a file path, or existing Telegram image ID
        * caption: optional caption to send with the picture
        * reply_to_id: specifies that the message should be a reply to specific user message
        referenced by it's ID

        TODO: Add markup (keyboard) option? as in text
        """
        telegram_method_name = 'sendPhoto'

        # Prepare data to send
        files = None
        data = {}
        f_handle = None
        if not isinstance(photo, string_types):
            # This is probably an opened file, pass it down as it is
            # to requests
            files = {'photo': photo}
        else:
            if os.path.isfile(photo):
                # This is a valid path to a file, open it, and pass handle
                # to requests
                f_handle = open(photo, "rb")
                files = {'photo': f_handle}
            else:
                # This might be a string of an existing image ID
                data['photo'] = photo
        if None != caption:
            data['caption'] = caption
        if None != reply_to_id:
            data['reply_to_message_id'] = reply_to_id

        # Issue request
        result = self._send_api_message(telegram_method_name, chat_id, data, files=files)

        # Close open file, if needed
        if None != f_handle:
            f_handle.close()

    def get_updates(self, offset=None):
        """
        This method provides an option to get updates (messages from the Telegram server)
        * offset: message ID offset from which to request messages (marks all message before it
            as read)
        """
        telegram_method_name = 'getUpdates'

        # Prepare data to send
        if None == offset:
            offset = self.offset
        data = {'offset': offset}

        # Issue request
        result = self._send_api_message(telegram_method_name, data=data)

        # Get last message id from request and add 1 (to get relevant updates next time)
        if 0 < len(result["result"]):
            self.offset = int(result["result"][-1]["update_id"]) + 1

        return result

    def listen_msg(self, long_poll_time=60):
        """
        This method requests updates from server, and blocks until an update is
        available.
        This method does not recalculate offset - it is merely to infrom of new messages
        * long_poll_time: timeout after the method stops waiting for updates
        """
        telegram_method_name = 'getUpdates'

        # Prepare data to send
        data = {'offset': self.offset, 'timeout': long_poll_time}

        # Issue request
        result = self._send_api_message(telegram_method_name, data=data)

        # Check for updates
        if 0 == len(result["result"]):
            return None
        
        return result