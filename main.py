import flet as ft
import mysql.connector
import re
import smtplib
from email.message import EmailMessage
import random

conexion = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="planify",
    charset="utf8mb4"
)

cursor = conexion.cursor()

codigos_recuperacion = {}

def main(page: ft.Page):

    page.title = "Planify"
    page.window_width = 400
    page.window_height = 850
    page.bgcolor = "#4A7DFF"
    page.padding = 0
    page.spacing = 0

    mensaje = ft.Text("", size=16)

    tareas = []

    def correo_valido(correo):
        patron = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return re.match(patron, correo)

    def enviar_codigo(correo, codigo):

        msg = EmailMessage()

        msg['Subject'] = "Codigo de recuperacion"
        msg['From'] = "planifyapp@gmail.com"
        msg['To'] = correo

        msg.set_content(
            f"Tu codigo de recuperacion es: {codigo}"
        )

        with smtplib.SMTP_SSL(
            'smtp.gmail.com',
            465
        ) as smtp:

            smtp.login(
                "planifyapp@gmail.com",
                "tu_contraseña"
            )

            smtp.send_message(msg)

    def mini_card(titulo, subtitulo, color, icono):

        return ft.Container(
            width=145,
            height=100,
            bgcolor=color,
            border_radius=20,
            padding=10,
            content=ft.Column(
                [
                    ft.Icon(
                        icono,
                        size=28,
                        color="black"
                    ),

                    ft.Text(
                        titulo,
                        size=16,
                        weight="bold"
                    ),

                    ft.Text(
                        subtitulo,
                        size=12,
                        color="black54"
                    )
                ]
            )
        )

    def abrir_gestor(usuario):

        page.clean()

        page.bgcolor = "#4A7DFF"
        page.scroll = "auto"

        lista_tareas = ft.Column(
            spacing=10
        )

        tarea_input = ft.TextField(
            hint_text="Agregar nueva tarea",
            border_radius=15,
            bgcolor="white",
            border_color="transparent",
            width=240
        )

        def actualizar_tareas():

            lista_tareas.controls.clear()

            for tarea in tareas:

                texto = ft.Text(
                    tarea["nombre"],
                    size=16,
                    expand=True,
                    color="black",
                    weight="bold" if tarea["hecho"] else "normal"
                )

                check = ft.Checkbox(
                    value=tarea["hecho"],
                    active_color="#4A7DFF",
                    on_change=lambda e, t=tarea:
                    marcar_tarea(t)
                )

                eliminar = ft.IconButton(
                    icon=ft.Icons.DELETE,
                    icon_color="red",
                    on_click=lambda e, t=tarea:
                    borrar_tarea(t)
                )

                tarjeta = ft.Container(
                    bgcolor="white",
                    border_radius=18,
                    padding=10,
                    content=ft.Row(
                        [
                            check,
                            texto,
                            eliminar
                        ]
                    )
                )

                lista_tareas.controls.append(tarjeta)

            page.update()

        def agregar_tarea(e):

            if tarea_input.value != "":

                tareas.append(
                    {
                        "nombre": tarea_input.value,
                        "hecho": False
                    }
                )

                tarea_input.value = ""

                actualizar_tareas()

        def marcar_tarea(tarea):

            tarea["hecho"] = not tarea["hecho"]

            actualizar_tareas()

        def borrar_tarea(tarea):

            tareas.remove(tarea)

            actualizar_tareas()

        tareas.extend([
            {
                "nombre": "Hacer compras",
                "hecho": False
            },
            {
                "nombre": "Estudiar Python",
                "hecho": True
            },
            {
                "nombre": "Terminar app en Flet",
                "hecho": False
            }
        ])

        encabezado = ft.Container(
            padding=25,
            content=ft.Column(
                [
                    ft.Text(
                        "Simplifica tu",
                        size=30,
                        weight="bold",
                        color="white"
                    ),

                    ft.Text(
                        "vida familiar",
                        size=30,
                        weight="bold",
                        color="white"
                    )
                ]
            )
        )

        panel = ft.Container(
            bgcolor="#F4F4F4",
            border_radius=30,
            padding=20,
            width=360,
            content=ft.Column(
                [
                    ft.Row(
                        [
                            ft.Text(
                                "La familia",
                                size=16,
                                weight="bold"
                            ),

                            ft.CircleAvatar(
                                bgcolor="#4A7DFF",
                                color="white",
                                content=ft.Text(
                                    usuario[0].upper()
                                )
                            )
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                    ),

                    ft.Container(
                        bgcolor="#7DC7FF",
                        border_radius=20,
                        padding=15,
                        content=ft.Column(
                            [
                                ft.Text(
                                    "Mi tarea principal",
                                    size=18,
                                    color="white",
                                    weight="bold"
                                ),

                                ft.Text(
                                    "Clase de natacion",
                                    color="white"
                                ),

                                ft.Text(
                                    "Lunes 6:00 PM",
                                    color="white70"
                                ),

                                ft.ProgressBar(
                                    value=0.7,
                                    color="white",
                                    bgcolor="#90CAF9"
                                )
                            ]
                        )
                    ),

                    ft.Row(
                        [
                            mini_card(
                                "Listas",
                                "4 tareas",
                                "#FFF3CD",
                                ft.Icons.LIST
                            ),

                            mini_card(
                                "Calendario",
                                "6 eventos",
                                "#E1BEE7",
                                ft.Icons.CALENDAR_MONTH
                            )
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                    ),

                    ft.Row(
                        [
                            mini_card(
                                "Horario",
                                "5 PM reunion",
                                "#BBDEFB",
                                ft.Icons.ACCESS_TIME
                            ),

                            mini_card(
                                "Mensajes",
                                "2 nuevos",
                                "#C8E6C9",
                                ft.Icons.MESSAGE
                            )
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                    ),

                    ft.Divider(),

                    ft.Text(
                        "Mis tareas",
                        size=22,
                        weight="bold"
                    ),

                    ft.Row(
                        [
                            tarea_input,

                            ft.FloatingActionButton(
                                icon=ft.Icons.ADD,
                                mini=True,
                                bgcolor="#4A7DFF",
                                on_click=agregar_tarea
                            )
                        ]
                    ),

                    lista_tareas,

                    ft.ElevatedButton(
                        "Cerrar sesion",
                        bgcolor="red",
                        color="white",
                        width=300,
                        on_click=mostrar_login
                    )
                ]
            )
        )

        page.add(
            ft.Column(
                [
                    encabezado,
                    panel
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            )
        )

        actualizar_tareas()

    def mostrar_login(e=None):

        page.clean()

        page.bgcolor = "#4A7DFF"

        usuario_input = ft.TextField(
            label="Usuario",
            width=300,
            text_align=ft.TextAlign.CENTER
        )

        pass_input = ft.TextField(
            label="Contrasena",
            password=True,
            can_reveal_password=True,
            width=300,
            text_align=ft.TextAlign.CENTER
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
                        size=30,
                        weight="bold",
                        text_align="center"
                    ),

                    ft.Text(
                        "Inicio de Sesion",
                        size=20,
                        text_align="center"
                    ),

                    usuario_input,
                    pass_input,

                    ft.ElevatedButton(
                        "Ingresar",
                        width=300,
                        bgcolor="#4A7DFF",
                        color="white",
                        on_click=lambda e:
                        login(
                            usuario_input.value,
                            pass_input.value
                        )
                    ),

                    ft.TextButton(
                        "Registrarse",
                        on_click=mostrar_registro
                    ),

                    ft.TextButton(
                        "Recuperar contrasena",
                        on_click=lambda e:
                        recuperar_contrasena()
                    ),

                    mensaje
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            )
        )

        page.add(
            ft.Column(
                [
                    card
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            )
        )

        page.update()

    def mostrar_registro(e=None):

        page.clean()

        usuario_input = ft.TextField(
            label="Usuario",
            width=300,
            text_align=ft.TextAlign.CENTER
        )

        correo_input = ft.TextField(
            label="Correo",
            width=300,
            text_align=ft.TextAlign.CENTER
        )

        pass_input = ft.TextField(
            label="Contrasena",
            password=True,
            can_reveal_password=True,
            width=300,
            text_align=ft.TextAlign.CENTER
        )

        pass2_input = ft.TextField(
            label="Confirmar Contrasena",
            password=True,
            can_reveal_password=True,
            width=300,
            text_align=ft.TextAlign.CENTER
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
                        size=25,
                        weight="bold"
                    ),

                    usuario_input,
                    correo_input,
                    pass_input,
                    pass2_input,

                    ft.ElevatedButton(
                        "Registrar",
                        width=300,
                        bgcolor="#4A7DFF",
                        color="white",
                        on_click=lambda e:
                        registrar(
                            usuario_input.value,
                            correo_input.value,
                            pass_input.value,
                            pass2_input.value
                        )
                    ),

                    ft.TextButton(
                        "Volver al Login",
                        on_click=mostrar_login
                    ),

                    mensaje
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            )
        )

        page.add(card)

        page.update()

    def login(usuario, clave):

        if not usuario or not clave:

            mensaje.value = "Rellena todos los campos"
            mensaje.color = "red"

            page.update()

            return

        sql = """
        SELECT * FROM usuario
        WHERE nombre=%s AND contrasena=%s
        """

        valores = (usuario, clave)

        cursor.execute(sql, valores)

        resultado = cursor.fetchone()

        if resultado:

            abrir_gestor(usuario)

        else:

            mensaje.value = "Usuario o contrasena incorrectos"
            mensaje.color = "red"

        page.update()

    def registrar(usuario, correo, clave, clave2):

        if not usuario or not clave or not correo or not clave2:

            mensaje.value = "Rellena todos los campos"
            mensaje.color = "red"

        elif clave != clave2:

            mensaje.value = "Las contrasenas no coinciden"
            mensaje.color = "red"

        elif not correo_valido(correo):

            mensaje.value = "Correo invalido"
            mensaje.color = "red"

        else:

            sql = """
            SELECT * FROM usuario
            WHERE nombre=%s
            """

            cursor.execute(sql, (usuario,))

            existe = cursor.fetchone()

            if existe:

                mensaje.value = "El usuario ya existe"
                mensaje.color = "red"

            else:

                sql = """
                INSERT INTO usuario(
                    nombre,
                    correo,
                    contrasena
                )
                VALUES(%s,%s,%s)
                """

                valores = (
                    usuario,
                    correo,
                    clave
                )

                cursor.execute(sql, valores)

                conexion.commit()

                mensaje.value = "Usuario registrado correctamente"
                mensaje.color = "green"

        page.update()

    def recuperar_contrasena():

        page.clean()

        correo_input = ft.TextField(
            label="Correo",
            width=300
        )

        codigo_input = ft.TextField(
            label="Codigo",
            width=300
        )

        nueva_input = ft.TextField(
            label="Nueva Contrasena",
            password=True,
            can_reveal_password=True,
            width=300
        )

        card = ft.Container(
            width=350,
            bgcolor="white",
            border_radius=25,
            padding=30,
            content=ft.Column(
                [
                    ft.Text(
                        "Recuperar Contrasena",
                        size=25,
                        weight="bold"
                    ),

                    correo_input,

                    ft.ElevatedButton(
                        "Enviar codigo",
                        width=300,
                        bgcolor="#4A7DFF",
                        color="white",
                        on_click=lambda e:
                        enviar_codigo_recuperacion(
                            correo_input.value
                        )
                    ),

                    codigo_input,
                    nueva_input,

                    ft.ElevatedButton(
                        "Cambiar Contrasena",
                        width=300,
                        bgcolor="green",
                        color="white",
                        on_click=lambda e:
                        cambiar_contrasena(
                            correo_input.value,
                            codigo_input.value,
                            nueva_input.value
                        )
                    ),

                    ft.TextButton(
                        "Volver al Login",
                        on_click=mostrar_login
                    ),

                    mensaje
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            )
        )

        page.add(card)

        page.update()

    def enviar_codigo_recuperacion(correo):

        sql = """
        SELECT * FROM usuario
        WHERE correo=%s
        """

        cursor.execute(sql, (correo,))

        usuario = cursor.fetchone()

        if usuario:

            codigo = str(
                random.randint(100000, 999999)
            )

            codigos_recuperacion[correo] = codigo

            try:

                enviar_codigo(correo, codigo)

                mensaje.value = (
                    f"Codigo enviado a {correo}"
                )

                mensaje.color = "green"

            except Exception as e:

                mensaje.value = f"Error: {e}"
                mensaje.color = "red"

        else:

            mensaje.value = "Correo no registrado"
            mensaje.color = "red"

        page.update()

    def cambiar_contrasena(
        correo,
        codigo,
        nueva
    ):

        if not correo or not codigo or not nueva:

            mensaje.value = (
                "Completa todos los campos"
            )

            mensaje.color = "red"

            page.update()

            return

        if correo not in codigos_recuperacion:

            mensaje.value = (
                "Solicita primero un codigo"
            )

            mensaje.color = "red"

            page.update()

            return

        if codigos_recuperacion[correo] != codigo:

            mensaje.value = "Codigo incorrecto"
            mensaje.color = "red"

            page.update()

            return

        sql = """
        UPDATE usuario
        SET contrasena=%s
        WHERE correo=%s
        """

        cursor.execute(
            sql,
            (
                nueva,
                correo
            )
        )

        conexion.commit()

        del codigos_recuperacion[correo]

        mensaje.value = "Contrasena actualizada"
        mensaje.color = "green"

        page.update()

    mostrar_login()

ft.app(target=main)