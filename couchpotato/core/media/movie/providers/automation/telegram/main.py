from bs4 import BeautifulSoup
from couchpotato.core.logger import CPLog
from couchpotato.core.media.movie.providers.automation.base import Automation
from .telegramapi import TelegramApi

log = CPLog(__name__)

autoload = 'Telegram'

class Telegram(Automation):
    """
    Implements CouchPotato automation using Telegram Bot API
    """
    telegram_api = None     # Telegram bot API communication object
    poller_thread = None    # Telegram messages poller thread
    interval = 60           # Probably irellevant, as we fire the event by ourselves

    def __init__(self):
        """
        Create the telegramapi communication object, and call super
        """
        self.telegram_api = TelegramApi(self.conf('bot_token'))
        super(Telegram, self).__init__()

    def getIMDBids(self):
        """
        Calls a method which interacts with the user to retreive requested movies
        Upon return of a list with movies the built-in search method is used to retreive IMDB IDs
        All retreived IMDB id's are returned back to caller
        """
        raise NotImplementedError
        pass

    def getUserRequestedMovies(self):
        """
        * For each requested movie, a web search is issued, and in case of
          more than one movie, a selection is presented to the user, with a cancel button
        * Upon selection, the movie title and year are added to a return list, which 
          is returned to caller when user interaction is finished
        """
        raise NotImplementedError
        pass

    def interactWithUser(self):
        """
        Retreives the messages sent from user, and processes it for commands.
        When no command is recognized, message is treated as freetext, and is passed to 
        movie interaction method.
        """
        raise NotImplementedError
        pass

    def searchMovie(self):
        """
        Searches a movie given freetext, returns list
        of possible choices + years
        """
        raise NotImplementedError
        pass

    def messagePollThread(self):
        """
        This method is run in a thread, and it's sole purpose is to fire the
        automation.get_movies event when new messages are available from user, to 
        provide a seamless interaction with the user
        """
        raise NotImplementedError
        pass