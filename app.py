# app.py

import os
import subprocess
import flet as ft
from func import read_json_file, write_json_file
from dialogs import AddGameDialog  # Импортируем класс AddGameDialog


def main(page: ft.Page):
    page.title = "Nexon Launcher"
    page.bgcolor = ft.colors.GREY_900
    page.window.bgcolor = ft.colors.WHITE
    page.window.width = 1000
    page.window.height = 800
    page.window.resizable = False

    page.theme = ft.Theme(color_scheme_seed=ft.colors.PURPLE_800)

    def open_repo(e):
        page.launch_url('https://github.com/')

    def add_game(e):
        dialog = AddGameDialog(page, on_game_added=add_game_to_data)
        dialog.create()

    def add_game_to_data(game):
        display_games()

    def read_games_data():
        return read_json_file().get("games", [])

    def launch_game(game_path: str):
        try:
            # Используем subprocess для запуска игры
            subprocess.Popen(game_path, shell=True)
        except Exception as e:
            page.add(ft.Text(f"Ошибка при запуске игры: {str(e)}", color=ft.colors.RED))
        page.update()

    def remove_game(game_name: str):
        games_data = read_json_file()
        games_data['games'] = [game for game in games_data['games'] if game['name'] != game_name]
        write_json_file(games_data)
        display_games()

    header = ft.Container(
        content=ft.Row([
            ft.Text("Nexon Launcher", size=35, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.LEFT),
            ft.Container(
                ft.Row([
                    ft.ElevatedButton("Обновления", ft.icons.NEWSPAPER, on_click=open_repo,
                                      bgcolor=ft.colors.PURPLE_800, color=ft.colors.WHITE),
                    ft.ElevatedButton("Добавить игру", ft.icons.ADD, on_click=add_game, bgcolor=ft.colors.PURPLE_800,
                                      color=ft.colors.WHITE)
                ])
            ),
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
        margin=ft.margin.symmetric(0, 20),
        padding=ft.padding.symmetric(10, 10),
    )

    page.add(header)
    page.add(ft.Divider())

    def display_games():
        games = read_games_data()

        page.controls.clear()

        page.add(header)
        page.add(ft.Divider())

        if not games:
            page.add(
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
                                                on_click=lambda e, game=game: launch_game(game["path"]),
                                                bgcolor=ft.colors.GREEN_800, color=ft.colors.WHITE)

                delete_button = ft.IconButton(ft.icons.DELETE, on_click=lambda e, game=game: remove_game(game["name"]),
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
            page.add(game_list)

        page.update()

    display_games()


ft.app(main)
