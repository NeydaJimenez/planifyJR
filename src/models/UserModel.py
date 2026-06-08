from src.models.DatabaseModel import DatabaseModel


class UserModel:

    def login(self, usuario, contrasena):

        conexion = DatabaseModel.conectar()
        cursor = conexion.cursor()

        cursor.execute(
            """
            SELECT *
            FROM usuario
            WHERE nombre=%s
            AND contrasena=%s
            """,
            (usuario, contrasena)
        )

        resultado = cursor.fetchone()

        conexion.close()

        return resultado

    def registrar(
        self,
        usuario,
        correo,
        contrasena
    ):

        conexion = DatabaseModel.conectar()
        cursor = conexion.cursor()

        cursor.execute(
            """
            INSERT INTO usuario
            (
                nombre,
                correo,
                contrasena
            )
            VALUES(%s,%s,%s)
            """,
            (
                usuario,
                correo,
                contrasena
            )
        )

        conexion.commit()
        conexion.close()

    def obtener_por_correo(
        self,
        correo
    ):

        conexion = DatabaseModel.conectar()
        cursor = conexion.cursor()

        cursor.execute(
            """
            SELECT *
            FROM usuario
            WHERE correo=%s
            """,
            (correo,)
        )

        usuario = cursor.fetchone()

        conexion.close()

        return usuario

    def actualizar_contrasena(
        self,
        correo,
        nueva
    ):

        conexion = DatabaseModel.conectar()
        cursor = conexion.cursor()

        cursor.execute(
            """
            UPDATE usuario
            SET contrasena=%s
            WHERE correo=%s
            """,
            (
                nueva,
                correo
            )
        )

        conexion.commit()
        conexion.close()