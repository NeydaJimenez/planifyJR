import flet as ft

usuarios = {}  
def main(page: ft.Page):
    page.title = "App con Login y Registro"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.padding = 20
    page.spacing = 10

    mensaje = ft.Text("", size=16, color="red")

 
    def mostrar_login(e=None):
        mensaje.value = ""
        page.controls.clear()
        page.add(
            ft.Text("Inicio de Sesión", size=25),
            ft.TextField(label="Usuario", key="login_usuario"),
            ft.TextField(label="Contraseña", password=True, can_reveal_password=True, key="login_pass"),
            ft.Row([
                ft.ElevatedButton("Ingresar", on_click=login),
                ft.TextButton("Registrarse", on_click=mostrar_registro)
            ]),
            mensaje
        )
        page.update()

    def mostrar_registro(e=None):
        mensaje.value = ""
        page.controls.clear()
        page.add(
            ft.Text("Registro", size=25),
            ft.TextField(label="Usuario", key="reg_usuario"),
            ft.TextField(label="Contraseña", password=True, can_reveal_password=True, key="reg_pass"),
            ft.TextField(label="Confirmar Contraseña", password=True, can_reveal_password=True, key="reg_pass2"),
            ft.Row([
                ft.ElevatedButton("Registrar", on_click=registrar),
                ft.TextButton("Volver al Login", on_click=mostrar_login)
            ]),
            mensaje
        )
        page.update()

    def login(e):
        usuario = page.get_control("login_usuario").value
        clave = page.get_control("login_pass").value

        if usuario in usuarios and usuarios[usuario] == clave:
            mensaje.value = f"¡Bienvenido {usuario}!"
            mensaje.color = "green"
        else:
            mensaje.value = "Usuario o contraseña incorrectos"
            mensaje.color = "red"
        page.update()

    def registrar(e):
        usuario = page.get_control("reg_usuario").value
        clave = page.get_control("reg_pass").value
        clave2 = page.get_control("reg_pass2").value

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