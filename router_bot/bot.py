# router-bot
# Copyright (C) 2017 quasiyoke
#
# You should have received a copy of the GNU Affero General Public License v3
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import asyncio
import logging
import telepot
from .admin_handler import AdminHandler
from .human_handler import HumanHandler
from .user_service import UserService
from telepot.delegate import per_from_id_in, per_from_id_except
from telepot.aio.delegate import create_open, pave_event_space

LOGGER = logging.getLogger('router_bot.bot')


class Bot:
    def __init__(self, configuration):
        user_service = UserService.get_instance()
        admins_telegram_ids = user_service.admins_telegram_ids
        self._delegator_bot = telepot.aio.DelegatorBot(
            configuration.token,
            [
                # If the bot isn't chatting with an admin, skip, so for this
                # chat will be used another handler, not AdminHandler.
                pave_event_space()(
                    per_from_id_in(admins_telegram_ids),
                    create_open,
                    AdminHandler,
                    timeout=60,
                    ),
                # If the bot is chatting with an admin, skip, so for this chat
                # will be used another handler, not HumanHandler.
                pave_event_space()(
                    per_from_id_except(admins_telegram_ids),
                    create_open,
                    HumanHandler,
                    timeout=60,
                    ),
                ],
            )

    async def run(self):
        LOGGER.info('Listening')
        await self._delegator_bot.message_loop()
