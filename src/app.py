import flet as ft
from game_manager import GameManager


def main(page: ft.Page):
    page.title = "Nexon Launcher"
    page.bgcolor = ft.colors.GREY_900
    page.window.width = 1000
    page.window.height = 800
    page.window.resizable = False
    page.theme = ft.Theme(color_scheme_seed=ft.colors.PURPLE_800)
    game_manager = GameManager(page)
    game_manager.display_games()


ft.app(main)
