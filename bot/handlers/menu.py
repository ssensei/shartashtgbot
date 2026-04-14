from aiogram import F, Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import CallbackQuery
from aiogram.types import InputMediaPhoto
from aiogram.types.input_file import FSInputFile
from pathlib import Path

from bot.data.content import MAIN_MENU, SECTIONS
from bot.keyboards.menu import build_item_menu, build_main_menu, build_section_menu

router = Router()
IMAGES_DIR = Path("assets/images")


def resolve_image_path(image_name: str) -> Path | None:
    exact_path = IMAGES_DIR / image_name
    if exact_path.exists():
        return exact_path

    stem = Path(image_name).stem
    for candidate in IMAGES_DIR.glob(f"{stem}.*"):
        if candidate.is_file():
            return candidate
    return None


async def edit_or_send_text(callback: CallbackQuery, text: str, section_id: str | None = None) -> None:
    markup = build_main_menu() if section_id is None else build_section_menu(section_id)
    try:
        await callback.message.edit_text(text, reply_markup=markup)
    except TelegramBadRequest as error:
        if "there is no text in the message to edit" not in str(error):
            raise
        await callback.message.delete()
        await callback.message.answer(text, reply_markup=markup)


@router.callback_query(F.data == "main_menu")
async def show_main_menu(callback: CallbackQuery) -> None:
    await edit_or_send_text(callback, "Выберите раздел:")
    await callback.answer()


@router.callback_query(F.data.startswith("section:"))
async def show_section_menu(callback: CallbackQuery) -> None:
    _, section_id = callback.data.split(":", maxsplit=1)
    if section_id not in MAIN_MENU:
        await callback.answer("Раздел не найден", show_alert=True)
        return

    section_title = SECTIONS[section_id]["title"]
    await edit_or_send_text(callback, f"Раздел: {section_title}\nВыберите пункт:", section_id=section_id)
    await callback.answer()


@router.callback_query(F.data.startswith("item:"))
async def show_item(callback: CallbackQuery) -> None:
    _, section_id, item_id = callback.data.split(":", maxsplit=2)
    section = SECTIONS.get(section_id)
    if not section:
        await callback.answer("Раздел не найден", show_alert=True)
        return

    item = section["items"].get(item_id)
    if not item:
        await callback.answer("Пункт не найден", show_alert=True)
        return

    images = item.get("images", [])
    if images:
        resolved_paths = [resolve_image_path(image_name) for image_name in images]
        resolved_paths = [path for path in resolved_paths if path]
        if resolved_paths:
            text = f"<b>{item['title']}</b>\n\n{item['text']}"
            await callback.message.delete()

            if len(resolved_paths) == 1:
                await callback.message.answer_photo(
                    photo=FSInputFile(resolved_paths[0]),
                    caption=text,
                    reply_markup=build_item_menu(section_id),
                )
            else:
                media = []
                for index, image_path in enumerate(resolved_paths):
                    if index == 0:
                        media.append(
                            InputMediaPhoto(
                                media=FSInputFile(image_path),
                                caption=text,
                                parse_mode="HTML",
                            )
                        )
                    else:
                        media.append(InputMediaPhoto(media=FSInputFile(image_path)))

                await callback.message.answer_media_group(media=media)
                await callback.message.answer(
                    "Навигация по разделу:",
                    reply_markup=build_item_menu(section_id),
                )

            await callback.answer()
            return

    text = f"<b>{item['title']}</b>\n\n{item['text']}"
    try:
        await callback.message.edit_text(text, reply_markup=build_item_menu(section_id))
    except TelegramBadRequest as error:
        if "there is no text in the message to edit" not in str(error):
            raise
        await callback.message.delete()
        await callback.message.answer(text, reply_markup=build_item_menu(section_id))
    await callback.answer()
