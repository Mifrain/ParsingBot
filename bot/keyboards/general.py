from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Загрузить Файл")],
        [KeyboardButton(text="Получить отчет по товарам")]
    ],
    resize_keyboard=True
)