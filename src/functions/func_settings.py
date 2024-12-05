import json
import os
from pathlib import Path

from . import func_update


# Функция для создания файла JSON
def create_json_file():
    # Получаем путь к папке "Документы" пользователя
    documents_folder = Path.home() / "Documents"

    # Создаем путь к папке "Nexon Launcher"
    nexon_launcher_folder = documents_folder / "Nexon Launcher"

    # Если папка не существует, создаем её
    if not nexon_launcher_folder.exists():
        nexon_launcher_folder.mkdir(parents=True)

    # Путь к файлу data.json
    json_file_path = nexon_launcher_folder / "settings.json"

    latest_version, release_url, download_url = func_update.get_latest_release()
    # Создаем словарь с данными
    data = {"theme": "dark",
            "color": "PURPLE_800",
            "version": latest_version}

    # Записываем данные в файл
    with open(json_file_path, 'w') as file:
        json.dump(data, file, indent=4)


# Функция для чтения данных из JSON файла
def read_json_file():
    # Получаем путь к папке "Документы" пользователя
    documents_folder = Path.home() / "Documents"

    # Путь к файлу data.json
    json_file_path = documents_folder / "Nexon Launcher" / "settings.json"

    # Если файл не существует, создаем его
    if not json_file_path.exists():
        create_json_file()

    # Читаем данные из файла
    with open(json_file_path, 'r') as file:
        data = json.load(file)
        return data  # Возвращаем данные из файла


# Функция для записи данных в JSON файл
def write_json_file(data):
    # Получаем путь к папке "Документы" пользователя
    documents_folder = Path.home() / "Documents"

    # Путь к файлу data.json
    json_file_path = documents_folder / "Nexon Launcher" / "settings.json"

    # Записываем данные в файл
    with open(json_file_path, 'w') as file:
        json.dump(data, file, indent=4)


def update_json_file():
    documents_folder = Path.home() / "Documents"
    json_file_path = documents_folder / "Nexon Launcher" / "settings.json"

    if not json_file_path.exists():
        create_json_file()

    latest_version, release_url, download_url = func_update.get_latest_release()

    data = {"theme": read_json_file()["theme"],
            "color": read_json_file()["color"],
            "version": latest_version}

    with open(json_file_path, 'w') as file:
        json.dump(data, file, indent=4)


# Проверяем, существует ли файл, если нет - создаем его
if __name__ == '__main__':
    if not os.path.exists(Path.home() / "Documents" / "Nexon Launcher" / "settings.json"):
        create_json_file()
