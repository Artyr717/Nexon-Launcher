import flet as ft
from launcher import Launcher


def main(page: ft.Page):
    page.title = "Nexon Launcher"
    page.bgcolor = ft.colors.GREY_900
    page.window.width = 1000
    page.window.height = 800
    page.window.resizable = False
    page.theme = ft.Theme(color_scheme_seed=ft.colors.PURPLE_800)
    game_manager = Launcher(page)
    game_manager.display_games()
    game_manager.check_for_updates()


ft.app(main)
