from aiogram import Router

from .survey_handlers import router as survey_handlers_router

router = Router(name='survey')
router.include_router(survey_handlers_router)
