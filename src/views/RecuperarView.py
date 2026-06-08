import flet as ft
import random
import smtplib

from email.message import EmailMessage

from src.models.UserModel import UserModel


class RecuperarView:

    codigos = {}

    def __init__(self, page):

        self.page = page

        self.user_model = UserModel()

        self.mostrar()

    def enviar_codigo(
        self,
        correo,
        codigo
    ):

        EMAIL = "jimenezrangelplanify@gmail.com"

        APP_PASSWORD = "snhwrqbzaqnzqpuk"

        mensaje = EmailMessage()

        mensaje["Subject"] = "Recuperación de contraseña"

        mensaje["From"] = EMAIL

        mensaje["To"] = correo

        mensaje.set_content(
            f"Tu código de recuperación es: {codigo}"
        )

        with smtplib.SMTP_SSL(
            "smtp.gmail.com",
            465
        ) as smtp:

            smtp.login(
                EMAIL,
                APP_PASSWORD
            )

            smtp.send_message(
                mensaje
            )

    def mostrar(self):

        self.page.clean()

        mensaje = ft.Text("")

        correo_input = ft.TextField(
            label="Correo",
            width=300
        )

        codigo_input = ft.TextField(
            label="Código",
            width=300
        )

        nueva_input = ft.TextField(
            label="Nueva contraseña",
            password=True,
            can_reveal_password=True,
            width=300
        )

        def enviar(e):

            correo = correo_input.value

            usuario = (
                self.user_model.obtener_por_correo(
                    correo
                )
            )

            if not usuario:

                mensaje.value = (
                    "Correo no registrado"
                )

                mensaje.color = "red"

                self.page.update()

                return

            codigo = str(
                random.randint(
                    100000,
                    999999
                )
            )

            RecuperarView.codigos[
                correo
            ] = codigo

            try:

                self.enviar_codigo(
                    correo,
                    codigo
                )

                mensaje.value = (
                    "Código enviado"
                )

                mensaje.color = "green"

            except Exception as ex:

                mensaje.value = str(ex)

                mensaje.color = "red"

            self.page.update()

        def cambiar(e):

            correo = correo_input.value

            codigo = codigo_input.value

            nueva = nueva_input.value

            if (
                correo not in RecuperarView.codigos
            ):

                mensaje.value = (
                    "Solicita primero un código"
                )

                mensaje.color = "red"

                self.page.update()

                return

            if (
                RecuperarView.codigos[
                    correo
                ]
                != codigo
            ):

                mensaje.value = (
                    "Código incorrecto"
                )

                mensaje.color = "red"

                self.page.update()

                return

            self.user_model.actualizar_contrasena(
                correo,
                nueva
            )

            del RecuperarView.codigos[
                correo
            ]

            mensaje.value = (
                "Contraseña actualizada"
            )

            mensaje.color = "green"

            self.page.update()

        card = ft.Container(
            width=350,
            bgcolor="white",
            border_radius=25,
            padding=30,
            content=ft.Column(
                [
                    ft.Text(
                        "Recuperar contraseña",
                        size=25,
                        weight="bold"
                    ),

                    correo_input,

                    ft.ElevatedButton(
                        "Enviar código",
                        bgcolor="#4A7DFF",
                        color="white",
                        width=300,
                        on_click=enviar
                    ),

                    codigo_input,

                    nueva_input,

                    ft.ElevatedButton(
                        "Cambiar contraseña",
                        bgcolor="green",
                        color="white",
                        width=300,
                        on_click=cambiar
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
    