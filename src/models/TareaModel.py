from src.models.DatabaseModel import DatabaseModel


class TareaModel:

    def obtener_tareas(self, id_usuario):

        conexion = DatabaseModel.conectar()
        cursor = conexion.cursor()

        cursor.execute(
            """
            SELECT *
            FROM tareas
            WHERE id_usuario = %s
            """,
            (id_usuario,)
        )

        tareas = cursor.fetchall()

        conexion.close()

        return tareas

    def agregar_tarea(
        self,
        nombre,
        fecha_entrega,
        id_usuario
    ):

        conexion = DatabaseModel.conectar()
        cursor = conexion.cursor()

        cursor.execute(
            """
            INSERT INTO tareas (
                nombre,
                fecha_entrega,
                id_usuario
            )
            VALUES (%s, %s, %s)
            """,
            (
                nombre,
                fecha_entrega,
                id_usuario
            )
        )

        conexion.commit()
        conexion.close()

    def eliminar_tarea(self, id_tarea):

        conexion = DatabaseModel.conectar()
        cursor = conexion.cursor()

        cursor.execute(
            """
            DELETE FROM tareas
            WHERE id_tarea = %s
            """,
            (id_tarea,)
        )

        conexion.commit()
        conexion.close()