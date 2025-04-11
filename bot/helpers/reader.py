import pandas as pd
from pathlib import Path
import os
from uuid import uuid4


from bot.db.services import SiteService
from bot.helpers.schemas import SiteInput


async def read_excel_file(bot, file_id, document):
    file = await bot.get_file(file_id)
    file_path_on_server = file.file_path
    doc_format = document.file_name.split(".")[1]

    if doc_format not in ["xls", "xlsx", "csv"]:
        return "Данный формат файла не поддерживается"

    local_path = Path(f"temp_sites/{uuid4()}_{document.file_name}")
    os.makedirs(local_path.parent, exist_ok=True)

    file_bytes = await bot.download_file(file_path_on_server)
    with open(local_path, "wb") as f:
        f.write(file_bytes.read())

    try:
        if doc_format == "csv": df = pd.read_csv(local_path, sep=";")
        else: df = pd.read_excel(local_path)

        required_columns = ['title', 'url', 'xpath']
        for col in required_columns:
            if col not in df.columns:
                return f"Ошибка: отсутствует столбец '{col}' в файле"

        records = df.to_dict(orient="records")

    except Exception as e:
        return f"Ошибка при чтении файла: {e}"

    for record in records:
        SiteService.add_site(SiteInput(**record))

    os.remove(local_path)

    text = "Добавлены данные:\n"
    text += "\n".join([f"{s.title} | {s.url} | {s.xpath}" for s in [SiteInput(**record) for record in records]])
    return text