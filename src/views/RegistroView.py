
import flet as ft
import re


class RegistroView:

    def __init__(self, page, controller):

        self.page = page
        self.controller = controller

        self.mostrar()

    def correo_valido(self, correo):

        patron = r'^[\w\.-]+@[\w\.-]+\.\w+$'

        return re.match(
            patron,
            correo
        )

    def mostrar(self):

        self.page.clean()

        mensaje = ft.Text("")

        usuario_input = ft.TextField(
            label="Usuario",
            width=300
        )

        correo_input = ft.TextField(
            label="Correo",
            width=300
        )

        password_input = ft.TextField(
            label="Contraseña",
            password=True,
            can_reveal_password=True,
            width=300
        )

        confirmar_input = ft.TextField(
            label="Confirmar contraseña",
            password=True,
            can_reveal_password=True,
            width=300
        )

        def registrar(e):

            usuario = usuario_input.value
            correo = correo_input.value
            password = password_input.value
            confirmar = confirmar_input.value

            if not usuario or not correo or not password or not confirmar:

                mensaje.value = "Completa todos los campos"
                mensaje.color = "red"

                self.page.update()
                return

            if password != confirmar:

                mensaje.value = "Las contraseñas no coinciden"
                mensaje.color = "red"

                self.page.update()
                return

            if not self.correo_valido(correo):

                mensaje.value = "Correo inválido"
                mensaje.color = "red"

                self.page.update()
                return

            try:

                self.controller.registrar(
                    usuario,
                    correo,
                    password
                )

                mensaje.value = "Usuario registrado correctamente"
                mensaje.color = "green"

            except Exception as ex:

                mensaje.value = str(ex)
                mensaje.color = "red"

            self.page.update()

        def volver_login(e):

            from src.views.LoginView import LoginView

            LoginView(
                self.page,
                self.controller
            )

        card = ft.Container(
            width=350,
            bgcolor="white",
            border_radius=25,
            padding=30,
            content=ft.Column(
                [
                    ft.Text(
                        "Registro",
                        size=28,
                        weight="bold"
                    ),

                    usuario_input,
                    correo_input,
                    password_input,
                    confirmar_input,

                    ft.ElevatedButton(
                        "Registrar",
                        width=300,
                        bgcolor="#4A7DFF",
                        color="white",
                        on_click=registrar
                    ),

                    ft.TextButton(
                        "Volver al Login",
                        on_click=volver_login
                    ),

                    mensaje
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            )
        )

        self.page.add(
            ft.Column(
                [card],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            )
        )

        self.page.update()