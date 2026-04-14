from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.data.content import MAIN_MENU, SECTIONS


def build_main_menu() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for section_id, section_name in MAIN_MENU.items():
        builder.button(text=section_name, callback_data=f"section:{section_id}")
    builder.adjust(1)
    return builder.as_markup()


def build_section_menu(section_id: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    section = SECTIONS[section_id]
    for item_id, item in section["items"].items():
        builder.button(text=item["title"], callback_data=f"item:{section_id}:{item_id}")
    builder.button(text="⬅️ Назад в главное меню", callback_data="main_menu")
    builder.adjust(1)
    return builder.as_markup()


def build_item_menu(section_id: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="⬅️ Назад к разделу", callback_data=f"section:{section_id}")
    builder.button(text="🏠 Главное меню", callback_data="main_menu")
    builder.adjust(1)
    return builder.as_markup()
