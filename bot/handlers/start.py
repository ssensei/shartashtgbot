from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from bot.keyboards.menu import build_main_menu

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    await message.answer(
        "Добро пожаловать в чат-бот «Клуб друзей Шарташа».\n\n"
        "Здесь вы можете узнать о проекте, школе ведущих прогулок, "
        "материалах, контактах и актуальных активностях.",
        reply_markup=build_main_menu(),
    )
