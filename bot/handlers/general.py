from http.client import responses

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.types import Document

from bot.helpers.reader import read_excel_file
from bot.states.file_upload import UploadFileState
from bot.keyboards.general import main_menu
from  bot.helpers.parser import get_summarize


router = Router()


@router.message(Command("start"))
async def start_handler(message: Message):
    await message.answer(f"Добро пожаловать", reply_markup=main_menu)


@router.message(F.text == "Загрузить Файл")
async def ask_file(message: Message, state: FSMContext):
    await message.answer(f"Отправьте файл Excel содержащий следующие поля:\n\
title - название \n\
url - ссылка на сайт источник \n\
xpath - путь к элементу с ценой")

    await state.set_state(UploadFileState.get_file)


@router.message(UploadFileState.get_file)
async def register_login_handler(message: Message, state: FSMContext, bot):
    if not message.document:
        await message.answer("Отправьте Excel-файл")
        return

    document: Document = message.document
    file_id = document.file_id

    response: str = await read_excel_file(bot, file_id, document)

    await message.answer(response)

    await state.clear()



@router.message(F.text == "Получить отчет по товарам")
async def ask_file(message: Message):
    await message.answer(f"Получаем отчет...")

    response = await get_summarize()
    await message.answer(response)
