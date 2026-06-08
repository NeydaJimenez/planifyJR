import flet as ft
from datetime import datetime

from src.controllers.TareaController import TareaController


class DashboardView:

    def __init__(
        self,
        page,
        id_usuario,
        nombre_usuario
    ):

        self.page = page
        self.id_usuario = id_usuario
        self.nombre_usuario = nombre_usuario

        self.controller = TareaController()

        self.mostrar()

    def mostrar(self):

        self.page.clean()

        self.page.title = "Planify"
        self.page.bgcolor = "#f5f7fa"
        self.page.scroll = ft.ScrollMode.AUTO

        lista_tareas = ft.Column(spacing=10)

        tarea_input = ft.TextField(
            label="Nombre de la tarea",
            prefix_icon=ft.Icons.TASK_ALT,
            expand=True
        )

        fecha_input = ft.TextField(
            label="Fecha (YYYY-MM-DD)",
            prefix_icon=ft.Icons.CALENDAR_MONTH,
            width=220
        )

        mensaje = ft.Text(
            "",
            color="red"
        )

        def cargar_tareas():

            lista_tareas.controls.clear()

            try:

                tareas = self.controller.obtener_tareas(
                    self.id_usuario
                )

                if not tareas:

                    lista_tareas.controls.append(
                        ft.Container(
                            content=ft.Text(
                                "No tienes tareas registradas.",
                                size=16
                            ),
                            padding=20
                        )
                    )

                for tarea in tareas:

                    id_tarea = tarea[0]
                    nombre = tarea[1]
                    fecha = tarea[2]

                    card = ft.Card(
                        elevation=3,
                        content=ft.Container(
                            padding=15,
                            content=ft.Row(
                                [
                                    ft.Icon(
                                        ft.Icons.CHECK_CIRCLE_OUTLINE,
                                        color="blue"
                                    ),

                                    ft.Column(
                                        [
                                            ft.Text(
                                                nombre,
                                                size=18,
                                                weight=ft.FontWeight.BOLD
                                            ),

                                            ft.Text(
                                                f"Entrega: {fecha}",
                                                color="grey"
                                            )
                                        ],
                                        expand=True,
                                        spacing=5
                                    ),

                                    ft.IconButton(
                                        icon=ft.Icons.DELETE,
                                        icon_color="red",
                                        tooltip="Eliminar tarea",
                                        on_click=lambda e, t=id_tarea: eliminar_tarea(t)
                                    )
                                ]
                            )
                        )
                    )

                    lista_tareas.controls.append(card)

                self.page.update()

            except Exception as ex:

                mensaje.value = f"Error: {ex}"
                self.page.update()

        def agregar_tarea(e):

            nombre = tarea_input.value.strip()
            fecha = fecha_input.value.strip()

            if not nombre:
                mensaje.value = "Debe ingresar una tarea."
                self.page.update()
                return

            if not fecha:
                mensaje.value = "Debe ingresar una fecha."
                self.page.update()
                return

            try:
                datetime.strptime(fecha, "%Y-%m-%d")
            except ValueError:
                mensaje.value = "Fecha inválida. Usa YYYY-MM-DD"
                self.page.update()
                return

            try:

                self.controller.agregar_tarea(
                    nombre,
                    fecha,
                    self.id_usuario
                )

                tarea_input.value = ""
                fecha_input.value = ""
                mensaje.value = ""

                cargar_tareas()

            except Exception as ex:

                mensaje.value = f"Error: {ex}"
                self.page.update()

        def eliminar_tarea(id_tarea):

            try:

                self.controller.eliminar_tarea(id_tarea)

                cargar_tareas()

            except Exception as ex:

                mensaje.value = f"Error: {ex}"
                self.page.update()

        self.page.appbar = ft.AppBar(
            title=ft.Text("PLANIFY"),
            center_title=True,
            bgcolor="#1976D2",
            color="white"
        )

        self.page.add(
            ft.Container(
                padding=20,
                content=ft.Column(
                    [
                        ft.Text(
                            f"Bienvenido, {self.nombre_usuario}",
                            size=24,
                            weight=ft.FontWeight.BOLD
                        ),

                        ft.Text(
                            "Gestiona tus tareas de forma sencilla",
                            color="grey"
                        ),

                        ft.Divider(),

                        ft.Row(
                            [
                                tarea_input,
                                fecha_input
                            ]
                        ),

                        ft.ElevatedButton(
                            "Guardar tarea",
                            icon=ft.Icons.ADD,
                            bgcolor="#1976D2",
                            color="white",
                            on_click=agregar_tarea
                        ),

                        mensaje,

                        ft.Divider(),

                        ft.Text(
                            "Mis tareas",
                            size=22,
                            weight=ft.FontWeight.BOLD
                        ),

                        lista_tareas
                    ]
                )
            )
        )

        cargar_tareas()

        self.page.update()