# router-bot
# Copyright (C) 2017 quasiyoke
#
# You should have received a copy of the GNU Affero General Public License v3
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import logging
from .error import StrangerSenderServiceError
from .stranger_sender import StrangerSender

LOGGER = logging.getLogger('router_bot.stranger_sender_service')


class StrangerSenderService:
    _instance = None

    def __init__(self, bot):
        self._bot = bot
        self._stranger_senders = {}

    @classmethod
    def get_instance(cls, bot=None):
        if cls._instance is None:
            if bot is None:
                raise StrangerSenderServiceError(
                    'Instance wasn\'t initialized. Provide arguments to '
                    'construct one.',
                    )
            else:
                cls._instance = cls(bot)
        return cls._instance

    def get_cache_size(self):
        return len(self._stranger_senders)

    def get_or_create_stranger_sender(self, stranger):
        try:
            return self._stranger_senders[stranger.telegram_id]
        except KeyError:
            stranger_sender = StrangerSender(self._bot, stranger)
            self._stranger_senders[stranger.telegram_id] = stranger_sender
            return stranger_sender
