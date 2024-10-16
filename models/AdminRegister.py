from flask_cors import CORS
from models.Database import Database
from flask import Flask, request, jsonify
from models.Cryptography import Cryptography

class AdminRegister:


    def __init__(self, app: Flask, db: Database):
        self.db = db
        CORS(app)
        app.add_url_rule('/create-adm', 'register_admin', self.register_admin, methods=['POST'])


    def check_cpf_exists(self, cpf: str):
        self.db.ensure_connection()
        cursor = self.db.connection.cursor()
        cursor.execute("SELECT * FROM adm WHERE cpf = %s", (cpf,))
        existing_adm = cursor.fetchone()
        return existing_adm
    

    def check_fields(self, data: dict):
        required_fields = ['name', 'cpf', 'password']
        for field in required_fields:
            if field not in data:
                return jsonify({"message": f"Campo '{field}' é obrigatório."}), 400
            

    def register_admin(self):
         
         try:
            data = request.get_json()

            self.check_fields(data)

            name = data['name'].upper()
            cpf = data['cpf']

            existing_adm = self.check_cpf_exists(cpf)
            if existing_adm:
                return jsonify({"message": "CPF já cadastrado!"}), 400

            password = data['password']

            hashed_password = Cryptography.hash_password(password)

            insert_query = """
                INSERT INTO adm (nome, cpf, senha)
                VALUES (%s, %s, %s);
            """
            
            data_to_insert = (
                name, cpf, hashed_password
            )

            self.db.ensure_connection()
            self.db.execute_query(insert_query, data_to_insert)

            return jsonify({
                "message": "Adm registrado com sucesso!",
                "data": {
                    "name": name,
                    "cpf": cpf
                }
            }), 201

         except KeyError as e:
            return jsonify({"message": f"Campo ausente: {str(e)}"}), 400
         except Exception as e:
            return jsonify({"message": f"Erro interno: {str(e)}"}), 500
