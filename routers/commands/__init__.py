# Этот инит файл нужен ТОЛЬКО для пакета COMMANDS
# Подключение к роутеру то, что нам нужно
__all__ = ("router",)

# Подразумевается, что экспорт отсюда (импорт в другие модули) - только экспорт основного роутера
from aiogram import Router

from .basic_commands import router as base_commands_router
from .user_commands import router as user_commands_router

router = Router(name=__name__)

# Можно и так:
# router.include_router(base_commands_router)
# router.include_router(user_commands_router)
# router.include_routers()

# здесь перечислены модули для папки COMMANDS
router.include_routers(
    base_commands_router,
    user_commands_router,
)
