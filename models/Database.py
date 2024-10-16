from mysql.connector import Error
from mysql.connector import connect

class Database:


    def __init__(self, host: str, user: str, password: str, database: str) -> None:
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
        self.create_db_connection() 


    def create_db_connection(self):
        try:
            self.connection = connect(
                host=self.host,
                user=self.user,
                passwd=self.password,
                database=self.database
            )
            print("MySQL Database connection successful")
        except Error as err:
            print(f"Error: '{err}'")
            self.connection = None


    def execute_query(self, query, data):
        cursor = self.connection.cursor()
        try:
            cursor.execute(query, data)
            self.connection.commit()
            print("Query successful")
        except Error as err:
            print(f"Error: '{err}'")


    def ensure_connection(self):
        if not self.connection or not self.connection.is_connected():
            print("Conexão perdida. Tentando reconectar...")
            self.create_db_connection("federacao_dama")

    
    def close_connection(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("Conexão com o banco de dados fechada.")
