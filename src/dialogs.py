import os
import flet as ft
from func import read_json_file, write_json_file


class AddGameDialog:
    def __init__(self, other_page: ft.Page, on_game_added=None):
        self.path = ft.IconButton(
            icon=ft.icons.FOLDER,
            on_click=lambda _: self.pick_file_dialog.pick_files(allow_multiple=False, allowed_extensions=["exe"])
        )
        self.name_field = ft.TextField(label="Название игры", width=300)
        self.other_page = other_page
        self.dlg = None
        self.data = read_json_file()
        self.selected_file_path = ft.TextField(label="Путь к файлу", width=300, disabled=True)
        self.pick_file_dialog = ft.FilePicker(on_result=self.pick_files_result)

        self.other_page.overlay.append(self.pick_file_dialog)
        self.on_game_added = on_game_added

    def create(self):
        add_button = ft.TextButton(
            text="Добавить",
            icon=ft.icons.ADD,
            on_click=self.on_click,
        )

        dialog_content = [
            ft.Container(content=self.name_field, padding=ft.padding.all(10), width=350),
            ft.Container(
                content=ft.Row(
                    [
                        self.path,
                        ft.Container(content=self.selected_file_path, width=250, padding=ft.padding.all(5)),
                    ],
                    alignment=ft.MainAxisAlignment.START,
                    spacing=10,
                ),
                width=350,
                padding=ft.padding.all(10),
            ),
            add_button
        ]

        title = ft.Text("Добавить игру", size=20, weight=ft.FontWeight.BOLD)

        self.dlg = ft.AlertDialog(
            title=title,
            actions=[content for content in dialog_content],
            bgcolor=ft.colors.GREY_800,
        )

        self.other_page.overlay.append(self.dlg)
        self.dlg.open = True
        self.other_page.update()

    def on_click(self, e):
        self.add_game()

    def pick_files_result(self, e: ft.FilePickerResultEvent):
        if e.files and isinstance(e.files, list) and e.files:
            self.selected_file_path.value = e.files[0].path
        else:
            self.selected_file_path.value = "Cancelled!"

        self.selected_file_path.update()

    def add_game(self):
        game_name = self.name_field.value
        game_path = self.selected_file_path.value

        if not game_name or not game_path or not game_path.endswith(".exe"):
            self.show_error("Ошибка: Неверный путь к файлу или имя игры пусто.")
            return

        game_dir = os.path.dirname(game_path)

        game_image_path = None
        for filename in os.listdir(game_dir):
            if filename.lower().endswith(".ico"):
                game_image_path = os.path.join(game_dir, filename)
                break

        new_game = {
            "name": game_name,
            "path": game_path,
        }
        if game_image_path:
            new_game["game_image"] = game_image_path

        games_data = read_json_file()

        existing_games = [game for game in games_data["games"] if game["name"] == new_game["name"]]
        if existing_games:
            self.show_error(f"Игра '{game_name}' уже добавлена.")
            return

        games_data["games"].append(new_game)
        write_json_file(games_data)

        self.dlg.open = False
        self.other_page.update()

        if self.on_game_added:
            self.on_game_added(new_game)

        self.show_info(f"Игра '{game_name}' успешно добавлена!")

    def show_error(self, message: str):
        error_message = ft.Text(message, color=ft.colors.RED, size=18)
        self.other_page.add(ft.Container(content=error_message, padding=ft.padding.symmetric(10, 10)))
        self.other_page.update()

    def show_info(self, message: str):
        info_message = ft.Text(message, color=ft.colors.GREEN, size=18)
        self.other_page.add(ft.Container(content=info_message, padding=ft.padding.symmetric(10, 10)))
        self.other_page.update()
