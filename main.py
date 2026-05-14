import flet as ft


usuarios = {"admin": "12345"}

def main(page: ft.Page):
    page.title = "App Login y Registro"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.padding = 20
    page.spacing = 10

    mensaje = ft.Text("", size=16)

    def mostrar_login(e=None):
        mensaje.value = ""
        page.controls.clear()
        usuario_input = ft.TextField(label="Usuario", key="login_usuario")
        pass_input = ft.TextField(label="Contraseña", password=True, can_reveal_password=True, key="login_pass")
        page.add(
            ft.Text("Inicio de Sesión", size=25),
            usuario_input,
            pass_input,
            ft.Row([
                ft.ElevatedButton("Ingresar", on_click=lambda e: login(usuario_input.value, pass_input.value)),
                ft.TextButton("Registrarse", on_click=mostrar_registro)
            ]),
            mensaje
        )
        page.update()

    def mostrar_registro(e=None):
        mensaje.value = ""
        page.controls.clear()
        usuario_input = ft.TextField(label="Usuario", key="reg_usuario")
        pass_input = ft.TextField(label="Contraseña", password=True, can_reveal_password=True, key="reg_pass")
        pass2_input = ft.TextField(label="Confirmar Contraseña", password=True, can_reveal_password=True, key="reg_pass2")
        page.add(
            ft.Text("Registro", size=25),
            usuario_input,
            pass_input,
            pass2_input,
            ft.Row([
                ft.ElevatedButton("Registrar", on_click=lambda e: registrar(usuario_input.value, pass_input.value, pass2_input.value)),
                ft.TextButton("Volver al Login", on_click=mostrar_login)
            ]),
            mensaje
        )
        page.update()

    def login(usuario, clave):
        if usuario in usuarios and usuarios[usuario] == clave:
            mensaje.value = f"¡Bienvenido {usuario}!"
            mensaje.color = "green"
        else:
            mensaje.value = "Usuario o contraseña incorrectos"
            mensaje.color = "red"
        page.update()

    def registrar(usuario, clave, clave2):
        if usuario in usuarios:
            mensaje.value = "El usuario ya existe"
            mensaje.color = "red"
        elif clave != clave2:
            mensaje.value = "Las contraseñas no coinciden"
            mensaje.color = "red"
        elif not usuario or not clave:
            mensaje.value = "Rellena todos los campos"
            mensaje.color = "red"
        else:
            usuarios[usuario] = clave
            mensaje.value = "Usuario registrado correctamente"
            mensaje.color = "green"
        page.update()

    mostrar_login()

ft.app(target=main)