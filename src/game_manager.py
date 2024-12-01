import subprocess

import flet as ft

from dialogs import AddGameDialog
from func import read_json_file, write_json_file


class GameManager:

    def __init__(self, page: ft.Page):
        self.page = page
        self.header = ft.Container(
            content=ft.Row([
                ft.Text("Nexon Launcher", size=35, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.LEFT),
                ft.Container(
                    ft.Row([
                        ft.ElevatedButton("Обновления", ft.icons.NEWSPAPER, on_click=self.open_repo,
                                          bgcolor=ft.colors.PURPLE_800, color=ft.colors.WHITE),
                        ft.ElevatedButton("Добавить игру", ft.icons.ADD, on_click=self.add_game,
                                          bgcolor=ft.colors.PURPLE_800,
                                          color=ft.colors.WHITE)
                    ])
                ),
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            margin=ft.margin.symmetric(0, 15),
            padding=ft.padding.symmetric(5, 5),
        )

    def open_repo(self, e):
        self.page.launch_url('https://github.com/Artyr717/Nexon-Launcher/releases')

    def add_game(self, e):
        dialog = AddGameDialog(self.page, on_game_added=self.add_game_to_data)
        dialog.create()

    def add_game_to_data(self, game):
        self.display_games()

    def read_games_data(self):
        return read_json_file().get("games", [])

    def launch_game(self, game_path: str):
        try:
            # Используем subprocess для запуска игры
            subprocess.Popen(game_path, shell=True)
        except Exception as e:
            self.page.add(ft.Text(f"Ошибка при запуске игры: {str(e)}", color=ft.colors.RED))
        self.page.update()

    def remove_game(self, game_name: str):
        games_data = read_json_file()
        games_data['games'] = [game for game in games_data['games'] if game['name'] != game_name]
        write_json_file(games_data)
        self.display_games()

    # page.add(header)
    # page.add(ft.Divider())

    def display_games(self):
        games = self.read_games_data()

        self.page.controls.clear()

        self.page.add(self.header)
        self.page.add(ft.Divider())

        if not games:
            self.page.add(
                ft.Container(
                    content=ft.Text("Нет игр", size=25, weight=ft.FontWeight.BOLD, color=ft.colors.RED,
                                    text_align=ft.TextAlign.CENTER),
                    padding=ft.padding.symmetric(10, 20),
                    expand=True
                )
            )
        else:
            game_rows = []

            for game in games:
                # Проверка на наличие изображения игры
                game_image = game.get("game_image", "")
                if game_image:
                    icon = ft.Image(src=game_image, width=40, height=40)
                else:
                    # Если картинки нет, отображаем только название
                    icon = ft.Text("", size=30)  # Место для иконки, но оставляем пустым

                play_button = ft.ElevatedButton("Запуск", ft.icons.PLAY_ARROW,
                                                on_click=lambda e, game_element=game: self.launch_game(
                                                    game_element["path"]),
                                                bgcolor=ft.colors.GREEN_800, color=ft.colors.WHITE)

                delete_button = ft.IconButton(ft.icons.DELETE,
                                              on_click=lambda e, game_element=game: self.remove_game(
                                                  game_element["name"]),
                                              icon_color=ft.colors.RED_800, )

                # Новый стиль для строки с игрой
                game_row = ft.Container(
                    content=ft.Row(
                        controls=[icon, ft.Text(game["name"], size=25, expand=True, weight=ft.FontWeight.BOLD),
                                  play_button, delete_button],
                        alignment=ft.MainAxisAlignment.START,
                        spacing=10,
                    ),
                    bgcolor=ft.colors.GREY_800,  # Темный фон
                    padding=ft.padding.symmetric(10, 10),
                    margin=ft.margin.symmetric(5, 5),  # Отступы для каждой строки
                    border_radius=ft.border_radius.all(10),  # Закругленные углы
                )

                game_rows.append(game_row)

            # Убираем фиксированную высоту и даём возможность контейнеру с играми занимать всё пространство
            game_list = ft.ListView(controls=game_rows, expand=True)
            self.page.add(game_list)

        self.page.update()
