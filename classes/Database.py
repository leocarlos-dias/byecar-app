import mysql.connector
import uuid
from datetime import datetime


class Database:
    def __init__(self, host, username, password, database, port):
        self.host = host
        self.username = username
        self.password = password
        self.database = database
        self.port = port
        self.connection = None

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.username,
                password=self.password,
                database=self.database,
                port=self.port,
            )
            self.cursor = self.connection.cursor()
        except mysql.connector.Error as err:
            raise Exception(f"Erro ao conectar ao banco de dados: {err}")

    def disconnect(self):
        if self.connection:
            self.connection.close()

    def execute_query(self, query):
        try:
            cursor = self.connection.cursor()
            cursor.execute(query)
            result = cursor.fetchall()
            return result
        except mysql.connector.Error as err:
            print(f"Erro ao executar a query: {err}")

    def insert(self, name, fipe_code, price):
        sql = "INSERT INTO vehicles (id, name, fipe_code, price, created_at) VALUES (%s, %s, %s, %s, %s)"
        val = (
            str(uuid.uuid4()),
            name,
            fipe_code,
            price,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        )
        self.cursor.execute(sql, val)
        self.connection.commit()
