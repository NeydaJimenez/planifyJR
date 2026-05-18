import flet as ft
import mysql.connector
import re


conexion = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="planify"
)

cursor = conexion.cursor()

usuarios = {"admin": "12345"}

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

    def mostrar_login(e=None):
        mensaje.value = ""
        page.controls.clear()
        usuario_input = ft.TextField(label="Usuario", key="login_usuario", width=300, text_align=ft.TextAlign.CENTER)
        pass_input = ft.TextField(label="Contraseña", password=True, can_reveal_password=True, key="login_pass", width=300, text_align=ft.TextAlign.CENTER)
        page.add(
            ft.Column(
                [
                    ft.Text("Inicio de Sesión", size=25),
                    usuario_input,
                    pass_input,
                    ft.Row([
                        ft.ElevatedButton("Ingresar", on_click=lambda e: login(usuario_input.value, pass_input.value)),
                        ft.TextButton("Registrarse", on_click=mostrar_registro)
                    ], alignment=ft.MainAxisAlignment.CENTER),
                    mensaje
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            )
        )
        page.update()

    def mostrar_registro(e=None):
        mensaje.value = ""
        page.controls.clear()
        usuario_input = ft.TextField(label="Usuario", key="reg_usuario", width=300, text_align=ft.TextAlign.CENTER)
        correo_input = ft.TextField(label="Correo", key="reg_correo", width=300, text_align=ft.TextAlign.CENTER)
        pass_input = ft.TextField(label="Contraseña", password=True, can_reveal_password=True, key="reg_pass", width=300, text_align=ft.TextAlign.CENTER)
        pass2_input = ft.TextField(label="Confirmar Contraseña", password=True, can_reveal_password=True, key="reg_pass2", width=300, text_align=ft.TextAlign.CENTER)
        page.add(
            ft.Column(
                [
                    ft.Text("Registro", size=25),
                    usuario_input,
                    correo_input,
                    pass_input,
                    pass2_input,
                    ft.Row([
                        ft.ElevatedButton("Registrar", on_click=lambda e: registrar(usuario_input.value, correo_input.value, pass_input.value, pass2_input.value)),
                        ft.TextButton("Volver al Login", on_click=mostrar_login)
                    ], alignment=ft.MainAxisAlignment.CENTER),
                    mensaje
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            )
        )
        page.update()

    def login(usuario, clave):

        sql = "SELECT * FROM usuario WHERE nombre=%s AND contraseña=%s"
        valores = (usuario, clave)

        cursor.execute(sql, valores)

        resultado = cursor.fetchone()

        if resultado:
            mensaje.value = f"¡Bienvenido {usuario}!"
            mensaje.color = "green"
        else:
            mensaje.value = "Usuario o contraseña incorrectos"
            mensaje.color = "red"

        page.update()

    def registrar(usuario, correo, clave, clave2):

        sql = "SELECT * FROM usuario WHERE nombre=%s"
        cursor.execute(sql, (usuario,))
        existe = cursor.fetchone()

        if existe:
            mensaje.value = "El usuario ya existe"
            mensaje.color = "red"

        elif clave != clave2:
            mensaje.value = "Las contraseñas no coinciden"
            mensaje.color = "red"

        elif not correo_valido(correo):
            mensaje.value = "Correo inválido"
            mensaje.color = "red"

        elif not usuario or not clave or not correo:
            mensaje.value = "Rellena todos los campos"
            mensaje.color = "red"

        else:

            sql = "INSERT INTO usuario(nombre, correo, contraseña) VALUES(%s,%s,%s)"
            valores = (usuario, correo, clave)

            cursor.execute(sql, valores)
            conexion.commit()

            mensaje.value = "Usuario registrado correctamente"
            mensaje.color = "green"

        page.update()

    mostrar_login()

ft.app(target=main)