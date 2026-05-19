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
    page.title = "App Login y Registro"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.padding = 20
    page.spacing = 10

    mensaje = ft.Text("", size=16)

    def correo_valido(correo):
        patron = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return re.match(patron, correo)

    def enviar_codigo(correo, codigo):
        msg = EmailMessage()
        msg['Subject'] = "Codigo de recuperacion"
        msg['From'] = "planifyapp@gmail.com"
        msg['To'] = correo
        msg.set_content(f"Tu codigo de recuperacion es: {codigo}")

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login("planifyapp@gmail.com", "tu_contraseña")
            smtp.send_message(msg)

    def mostrar_login(e=None):
        mensaje.value = ""
        page.controls.clear()

        usuario_input = ft.TextField(
            label="Usuario",
            key="login_usuario",
            width=300,
            text_align=ft.TextAlign.CENTER
        )

        pass_input = ft.TextField(
            label="Contrasena",
            password=True,
            can_reveal_password=True,
            key="login_pass",
            width=300,
            text_align=ft.TextAlign.CENTER
        )

        page.add(
            ft.Column(
                [
                    ft.Text("Inicio de Sesion", size=25),
                    usuario_input,
                    pass_input,
                    ft.Row(
                        [
                            ft.ElevatedButton(
                                "Ingresar",
                                on_click=lambda e: login(
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
                                on_click=lambda e: recuperar_contrasena()
                            )
                        ],
                        alignment=ft.MainAxisAlignment.CENTER
                    ),
                    mensaje
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            )
        )

        page.update()

    def mostrar_registro(e=None):
        mensaje.value = ""
        page.controls.clear()

        usuario_input = ft.TextField(
            label="Usuario",
            key="reg_usuario",
            width=300,
            text_align=ft.TextAlign.CENTER
        )

        correo_input = ft.TextField(
            label="Correo",
            key="reg_correo",
            width=300,
            text_align=ft.TextAlign.CENTER
        )

        pass_input = ft.TextField(
            label="Contrasena",
            password=True,
            can_reveal_password=True,
            key="reg_pass",
            width=300,
            text_align=ft.TextAlign.CENTER
        )

        pass2_input = ft.TextField(
            label="Confirmar Contrasena",
            password=True,
            can_reveal_password=True,
            key="reg_pass2",
            width=300,
            text_align=ft.TextAlign.CENTER
        )

        page.add(
            ft.Column(
                [
                    ft.Text("Registro", size=25),
                    usuario_input,
                    correo_input,
                    pass_input,
                    pass2_input,
                    ft.Row(
                        [
                            ft.ElevatedButton(
                                "Registrar",
                                on_click=lambda e: registrar(
                                    usuario_input.value,
                                    correo_input.value,
                                    pass_input.value,
                                    pass2_input.value
                                )
                            ),

                            ft.TextButton(
                                "Volver al Login",
                                on_click=mostrar_login
                            )
                        ],
                        alignment=ft.MainAxisAlignment.CENTER
                    ),
                    mensaje
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            )
        )

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
            mensaje.value = f"Bienvenido {usuario}"
            mensaje.color = "green"
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

            sql = "SELECT * FROM usuario WHERE nombre=%s"

            cursor.execute(sql, (usuario,))

            existe = cursor.fetchone()

            if existe:
                mensaje.value = "El usuario ya existe"
                mensaje.color = "red"

            else:

                sql = """
                INSERT INTO usuario(nombre, correo, contrasena)
                VALUES(%s,%s,%s)
                """

                valores = (usuario, correo, clave)

                cursor.execute(sql, valores)

                conexion.commit()

                mensaje.value = "Usuario registrado correctamente"
                mensaje.color = "green"

        page.update()

    def recuperar_contrasena():

        page.controls.clear()

        correo_input = ft.TextField(
            label="Correo",
            width=300,
            text_align=ft.TextAlign.CENTER
        )

        codigo_input = ft.TextField(
            label="Codigo",
            width=300,
            text_align=ft.TextAlign.CENTER
        )

        nueva_input = ft.TextField(
            label="Nueva Contrasena",
            password=True,
            can_reveal_password=True,
            width=300,
            text_align=ft.TextAlign.CENTER
        )

        btn_enviar = ft.ElevatedButton(
            "Enviar codigo",
            on_click=lambda e:
            enviar_codigo_recuperacion(
                correo_input.value
            )
        )

        btn_cambiar = ft.ElevatedButton(
            "Cambiar Contrasena",
            on_click=lambda e:
            cambiar_contrasena(
                correo_input.value,
                codigo_input.value,
                nueva_input.value
            )
        )

        page.add(
            ft.Column(
                [
                    ft.Text("Recuperar Contrasena", size=25),

                    correo_input,

                    btn_enviar,

                    codigo_input,

                    nueva_input,

                    btn_cambiar,

                    ft.Row(
                        [
                            ft.TextButton(
                                "Volver al Login",
                                on_click=mostrar_login
                            )
                        ],
                        alignment=ft.MainAxisAlignment.CENTER
                    ),

                    mensaje
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            )
        )

        page.update()

    def enviar_codigo_recuperacion(correo):

        sql = "SELECT * FROM usuario WHERE correo=%s"

        cursor.execute(sql, (correo,))

        usuario = cursor.fetchone()

        if usuario:

            codigo = str(random.randint(100000, 999999))

            codigos_recuperacion[correo] = codigo

            try:

                enviar_codigo(correo, codigo)

                mensaje.value = f"Codigo enviado a {correo}"
                mensaje.color = "green"

            except Exception as e:

                mensaje.value = f"Error: {e}"
                mensaje.color = "red"

        else:

            mensaje.value = "Correo no registrado"
            mensaje.color = "red"

        page.update()

    def cambiar_contrasena(correo, codigo, nueva):

        if not correo or not codigo or not nueva:
            mensaje.value = "Completa todos los campos"
            mensaje.color = "red"
            page.update()
            return

        if correo not in codigos_recuperacion:
            mensaje.value = "Solicita primero un codigo"
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

        cursor.execute(sql, (nueva, correo))

        conexion.commit()

        del codigos_recuperacion[correo]

        mensaje.value = "Contrasena actualizada"
        mensaje.color = "green"

        page.update()

    mostrar_login()

ft.app(target=main)