from src.models.UserModel import UserModel


class UserController:

    def __init__(self):
        self.model = UserModel()

    def login(
        self,
        usuario,
        contrasena
    ):
        return self.model.login(
            usuario,
            contrasena
        )

    def registrar(
        self,
        usuario,
        correo,
        contrasena
    ):
        self.model.registrar(
            usuario,
            correo,
            contrasena
        )