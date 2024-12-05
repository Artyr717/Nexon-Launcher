import subprocess
import flet as ft
from dialogs import AddGameDialog, SettingsDialog
import functions.func_games as func_g
import functions.func_settings as func_s


class GameManager:
    def __init__(self, page: ft.Page):
        self.page = page
        self.apply_settings()  # Apply saved theme and color on initialization

        self.header = ft.Container(
            content=ft.Row([
                ft.Text("Nexon Launcher", size=35, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.LEFT,
                        color=self.text_color),
                ft.Container(
                    ft.Row(
                        [
                            ft.ElevatedButton("Обновления", ft.icons.NEWSPAPER, on_click=self.open_repo,
                                              bgcolor=self.page.theme.primary_color, color=self.button_text_color),
                            ft.ElevatedButton("Добавить игру", ft.icons.ADD, on_click=self.add_game,
                                              bgcolor=self.page.theme.primary_color, color=self.button_text_color),
                            ft.IconButton(ft.icons.SETTINGS, icon_color=self.icon_color, on_click=self.open_settings)
                        ]
                    )
                ),
            ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            margin=ft.margin.symmetric(0, 15),
            padding=ft.padding.symmetric(5, 5),
        )

    def apply_settings(self):
        """Apply theme and color settings from the JSON file."""
        settings = func_s.read_json_file()
        theme = settings.get('theme', 'dark')
        color = settings.get('color', 'PURPLE_800')
        color = getattr(ft.colors, color.upper(),
                        ft.colors.PURPLE_800)  # Convert to uppercase and fallback to PURPLE_800

        # Apply the theme
        if theme == 'light':
            self.page.bgcolor = ft.colors.WHITE
            self.page.theme = ft.Theme(color_scheme_seed=color)
            self.text_game_color = ft.colors.WHITE
            self.text_color = ft.colors.BLACK  # Dark text for light theme
            self.button_text_color = ft.colors.WHITE  # Dark text for buttons in light theme
            self.icon_color = ft.colors.BLACK  # Dark icons for light theme
        else:
            self.page.bgcolor = ft.colors.GREY_900
            self.page.theme = ft.Theme(color_scheme_seed=color)
            self.text_game_color = ft.colors.WHITE
            self.text_color = ft.colors.WHITE  # Light text for dark theme
            self.button_text_color = ft.colors.WHITE  # Light text for buttons in dark theme
            self.icon_color = ft.colors.WHITE  # Light icons for dark theme

        # Apply accent color (used for buttons and other elements)
        self.page.theme.primary_color = color
        self.page.update()

    def open_settings(self, e):
        dialog = SettingsDialog(self.page)
        dialog.create()

    def open_repo(self, e):
        self.page.launch_url('https://github.com/Artyr717/Nexon-Launcher/releases')

    def add_game(self, e):
        dialog = AddGameDialog(self.page, on_game_added=self.add_game_to_data)
        dialog.create()

    def add_game_to_data(self, game):
        self.display_games()

    def read_games_data(self):
        return func_g.read_json_file().get("games", [])

    def launch_game(self, game_path: str):
        try:
            # Use subprocess to launch the game
            subprocess.Popen(game_path, shell=True)
        except Exception as e:
            self.page.add(ft.Text(f"Ошибка при запуске игры: {str(e)}", color=ft.colors.RED))
        self.page.update()

    def remove_game(self, game_name: str):
        games_data = func_g.read_json_file()
        games_data['games'] = [game for game in games_data['games'] if game['name'] != game_name]
        func_g.write_json_file(games_data)
        self.display_games()

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
                game_image = game.get("game_image", "")
                if game_image:
                    icon = ft.Image(src=game_image, width=40, height=40)
                else:
                    icon = ft.Text("", size=30)

                # Apply the correct colors to buttons and icons
                play_button = ft.ElevatedButton("Запуск", ft.icons.PLAY_ARROW,
                                                on_click=lambda e, game_element=game: self.launch_game(
                                                    game_element["path"]),
                                                bgcolor=self.page.theme.primary_color, color=self.button_text_color)

                delete_button = ft.IconButton(ft.icons.DELETE,
                                              on_click=lambda e, game_element=game: self.remove_game(
                                                  game_element["name"]),
                                              icon_color=ft.colors.RED_800, )

                game_row = ft.Container(
                    content=ft.Row(
                        controls=[icon, ft.Text(game["name"], size=25, expand=True, weight=ft.FontWeight.BOLD,
                                                color=self.text_game_color),
                                  play_button, delete_button],
                        alignment=ft.MainAxisAlignment.START,
                        spacing=10,
                    ),
                    bgcolor=ft.colors.GREY_800,
                    padding=ft.padding.symmetric(10, 10),
                    margin=ft.margin.symmetric(5, 5),
                    border_radius=ft.border_radius.all(10),
                )

                game_rows.append(game_row)

            game_list = ft.ListView(controls=game_rows, expand=True)
            self.page.add(game_list)

        self.page.update()
