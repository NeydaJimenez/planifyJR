import mysql.connector

class DatabaseModel:

    @staticmethod
    def conectar():
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="planify"
        )