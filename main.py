import flet as ft

from src.controllers.UserController import UserController
from src.views.LoginView import LoginView


def main(page: ft.Page):

    page.title = "Planify"

    page.window_width = 400
    page.window_height = 850

    page.bgcolor = "#4A7DFF"

    controller = UserController()

    LoginView(
        page,
        controller
    )


ft.app(target=main)