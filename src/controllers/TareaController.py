from src.models.TareaModel import TareaModel

class TareaController:

    def __init__(self):
        self.model = TareaModel()

    def obtener_tareas(self, id_usuario):
        return self.model.obtener_tareas(id_usuario)

    def agregar_tarea(self, nombre, fecha_entrega, id_usuario):
        """
        Agrega una nueva tarea con fecha de entrega
        :param nombre: str - Nombre de la tarea
        :param fecha_entrega: str o datetime - Fecha en formato 'YYYY-MM-DD'
        :param id_usuario: int - ID del usuario que crea la tarea
        """
        self.model.agregar_tarea(
            nombre,
            fecha_entrega,
            id_usuario
        )

    def eliminar_tarea(self, id_tarea):
        self.model.eliminar_tarea(id_tarea)