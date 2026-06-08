import flet as ft


class LoginView:

    def __init__(self, page, controller):

        self.page = page
        self.controller = controller

        self.mostrar()

    def mostrar(self):

        self.page.clean()

        self.page.title = "Planify"

        self.page.bgcolor = "#4A7DFF"

        mensaje = ft.Text(
            "",
            color="red"
        )

        usuario_input = ft.TextField(
            label="Usuario",
            width=300
        )

        password_input = ft.TextField(
            label="Contraseña",
            password=True,
            can_reveal_password=True,
            width=300
        )

        def iniciar_sesion(e):

            usuario = usuario_input.value.strip()

            password = password_input.value.strip()

            if not usuario or not password:

                mensaje.value = (
                    "Completa todos los campos"
                )

                mensaje.color = "red"

                self.page.update()

                return

            try:

                resultado = self.controller.login(
                    usuario,
                    password
                )

                if resultado:

                    from src.views.DashboardView import DashboardView

                    id_usuario = resultado[0]

                    nombre_usuario = resultado[1]

                    DashboardView(
                        self.page,
                        id_usuario,
                        nombre_usuario
                    )

                else:

                    mensaje.value = (
                        "Usuario o contraseña incorrectos"
                    )

                    mensaje.color = "red"

                    self.page.update()

            except Exception as ex:

                mensaje.value = str(ex)

                mensaje.color = "red"

                self.page.update()

        def abrir_registro(e):

            from src.views.RegistroView import RegistroView

            RegistroView(
                self.page,
                self.controller
            )

        def abrir_recuperacion(e):

            from src.views.RecuperarView import RecuperarView

            RecuperarView(
                self.page
            )

        card = ft.Container(
            width=350,
            bgcolor="white",
            border_radius=25,
            padding=30,
            content=ft.Column(
                [
                    ft.Text(
                        "Planify",
                        size=32,
                        weight="bold"
                    ),

                    ft.Text(
                        "Inicio de Sesión",
                        size=20
                    ),

                    usuario_input,

                    password_input,

                    ft.ElevatedButton(
                        "Ingresar",
                        width=300,
                        bgcolor="#4A7DFF",
                        color="white",
                        on_click=iniciar_sesion
                    ),

                    ft.TextButton(
                        "Registrarse",
                        on_click=abrir_registro
                    ),

                    ft.TextButton(
                        "Recuperar contraseña",
                        on_click=abrir_recuperacion
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