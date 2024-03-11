# THIS IS THE MAIN ROUTER
__all__ = ("router",)  # импортируем только основной роутер

from aiogram import Router

from .admin_handlers import router as admin_router
from .callback_handlers import router as callback_router
from .commands import router as commands_router
from .common import router as common_router
from .media_handlers import router as media_router
from .custom.business import router as business_router
from .custom.games import router as games_router
from .custom.mathix import router as mathix_router
from .custom.photobot import router as photobot_router

# здесь мы уже импортируем из COMMANDS

router = Router(name=__name__)

# router.include_router(commands_router)  # у нас будет любое количество вложенных routers
# router.include_router(commands_router) - этот роутер мы подключаем к основному приложению
# router.include_router(media_router)  # media handler

router.include_routers(callback_router,
                       commands_router,
                       media_router,
                       business_router,
                       games_router,
                       mathix_router,
                       photobot_router,
                       # add your router here (if you want)
                       admin_router  # this should be the last one here
                       )

# the router below has to be the final, echo-bot command!!!
router.include_router(common_router)  # этот роутер подключаем самым последним, потому что это echo bot
