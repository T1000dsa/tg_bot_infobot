import logging
from typing import Any, Awaitable, Callable, Dict
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

logger = logging.getLogger(__name__)


class SimpleMiddle(BaseMiddleware):
    result = None
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:

        logger.info(
            'Вошли в миддлварь %s, тип события %s',
            __class__.__name__,
            event.__class__.__name__
        )
        try:
            result = await handler(event, data)
            logger.info('Выходим из миддлвари  %s', __class__.__name__)
            #print(data['event_context'].user.id)
        except:
            logger.critical('Выходим из миддлвари  %s', __class__.__name__)
        return result