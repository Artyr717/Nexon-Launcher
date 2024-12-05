import os

import flet as ft

import functions.func_games as func_g
import functions.func_settings as func_s


class AddGameDialog:
    def __init__(self, other_page: ft.Page, on_game_added=None):
        self.path = ft.IconButton(
            icon=ft.icons.FOLDER,
            on_click=lambda _: self.pick_file_dialog.pick_files(allow_multiple=False, allowed_extensions=["exe"])
        )
        self.name_field = ft.TextField(label="Название игры", width=300)
        self.other_page = other_page
        self.dlg = None
        self.data = func_g.read_json_file()
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

        games_data = func_g.read_json_file()

        existing_games = [game for game in games_data["games"] if game["name"] == new_game["name"]]
        if existing_games:
            self.show_error(f"Игра '{game_name}' уже добавлена.")
            return

        games_data["games"].append(new_game)
        func_g.write_json_file(games_data)

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


class SettingsDialog:
    def __init__(self, other_page):
        self.other_page = other_page
        self.dlg = None
        self.data = func_s.read_json_file()

    def create(self):
        # Button to save settings
        add_button = ft.TextButton(
            text="Сохранить",
            icon=ft.icons.SAVE,
            on_click=self.on_click,
            icon_color=ft.colors.WHITE,
        )
        to_default_button = ft.TextButton("По умолчанию",
                                          on_click=self.on_click_default)

        # Accent color options (example colors)
        color_options = [
            "PURPLE_800", "RED_800", "GREEN_800", "BLUE_800"
        ]

        # Creating color buttons
        color_buttons = [
            ft.IconButton(
                icon=ft.icons.COLOR_LENS,
                on_click=lambda e, color=color: self.set_color(e, color),
                tooltip=f"Выберите {color}",
                bgcolor=getattr(ft.colors, color),
                icon_color=ft.colors.WHITE  # Set icon color to white
            )
            for color in color_options
        ]

        # Creating theme selection buttons (light and dark)
        theme_buttons = [
            ft.IconButton(
                icon=ft.icons.BRIGHTNESS_7 if theme == "light" else ft.icons.BRIGHTNESS_3,
                on_click=lambda e, theme=theme: self.set_theme(e, theme),
                tooltip=f"Выберите тему {theme.capitalize()}",
                bgcolor=ft.colors.AMBER_800 if theme == "light" else ft.colors.GREY_700,
                icon_color=ft.colors.WHITE  # Set icon color to white
            )
            for theme in ["light", "dark"]
        ]

        # Creating the dialog content with buttons
        dialog_content = ft.Column([
            ft.Container(
                content=ft.Row([ft.Text("Выберите тему:", size=20, color=ft.colors.WHITE, weight=ft.FontWeight.BOLD),
                                *theme_buttons]),
                padding=ft.padding.all(10),
            ),
            ft.Container(
                content=ft.Row(
                    [ft.Text("Выберите акцентный цвет:", size=20, color=ft.colors.WHITE, weight=ft.FontWeight.BOLD),
                     *color_buttons]),
                padding=ft.padding.all(10),
            )
        ], alignment=ft.MainAxisAlignment.START, height=150)

        # Setting the dialog title and content
        title = ft.Text("Настройки", size=30, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE)
        self.dlg = ft.AlertDialog(
            title=title,
            content=dialog_content,
            bgcolor=ft.colors.GREY_800,
            actions=[to_default_button, add_button]  # Add the save button to the dialog actions
        )

        # Adding the dialog to the overlay and opening it
        self.other_page.overlay.append(self.dlg)
        self.dlg.open = True
        self.other_page.update()

    def set_color(self, e, color):
        """ Set the accent color """
        self.data['color'] = color
        self.other_page.update()

    def set_theme(self, e, theme):
        """ Set the theme (light or dark) """
        self.data['theme'] = theme
        self.other_page.update()

    def on_click(self, e):
        """ Save settings and restart the app """
        func_s.write_json_file(self.data)
        self.restart(self.other_page)
        self.dlg.open = False
        self.other_page.update()

    def on_click_default(self, e):
        self.data['theme'] = "dark"
        self.data['color'] = "PURPLE_800"
        func_s.write_json_file(self.data)
        self.restart(self.other_page)
        self.dlg.open = False
        self.other_page.update()

    def restart(self, page: ft.Page):
        from launcher import Launcher
        """ Function to restart the app by clearing the page and reinitializing GameManager """
        page.controls.clear()  # Clear current page controls
        game_manager = Launcher(page)  # Reinitialize the GameManager
        game_manager.display_games()  # Re-display the games or any other content after restart
        page.update()  # Update the page with the new content


class UpdateDialog:
    def __init__(self, other_page, current_version, latest_version, download_url):
        self.other_page = other_page
        self.dlg = None
        self.current_version = current_version
        self.latest_version = latest_version
        self.download_url = download_url
        self.data = func_s.read_json_file()

    def create(self):
        update_button = ft.ElevatedButton("Обновить", icon=ft.icons.DOWNLOAD, color=ft.colors.WHITE,
                                          icon_color=ft.colors.WHITE, bgcolor=self.other_page.theme.primary_color,
                                          on_click=self.update)
        close_button = ft.TextButton("Не сейчас...", on_click=self.close_message)

        dialog_content = ft.Column([
            ft.Divider(color=ft.colors.GREY_700),
            ft.Container(
                content=ft.Column([
                    ft.Text(f"Ваша версия: {self.current_version}",
                            size=20, color=ft.colors.WHITE, weight=ft.FontWeight.BOLD),
                    ft.Text(f"Актуальная версия: {self.latest_version}",
                            size=20, color=ft.colors.WHITE, weight=ft.FontWeight.BOLD)
                ]),
            ),
        ], alignment=ft.MainAxisAlignment.START, height=100)

        title = ft.Text("Доступно обновление", size=25, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE,
                        text_align=ft.TextAlign.CENTER)
        self.dlg = ft.AlertDialog(
            title=title,
            content=dialog_content,
            bgcolor=ft.colors.GREY_800,
            actions=[close_button, update_button]
        )

        self.other_page.overlay.append(self.dlg)
        self.dlg.open = True
        self.other_page.update()

    def update(self, e):
        try:
            self.other_page.launch_url(self.download_url)
        except Exception as e:
            print(e)

        self.data["version"] = self.latest_version
        func_s.write_json_file(self.data)
        self.dlg.open = False
        self.other_page.update()

    def close_message(self, e):
        self.dlg.open = False
        self.other_page.update()
