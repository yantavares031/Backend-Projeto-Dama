from flask_cors import CORS
from models.Database import Database
from flask import Flask, request, jsonify, Blueprint
from models.Cryptography import Cryptography
from datetime import timedelta
from flask_jwt_extended import (
    create_access_token, jwt_required, get_jwt_identity
)

class UserLogin:

    def __init__(self, app: Blueprint, db: Database):
        self.db = db
        app.config["JWT_SECRET_KEY"] = "sua_chave_super_secreta"
        app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
        CORS(app)
        app.add_url_rule('/user/login', 'login_user', self.login_user, methods=['POST'])


    def check_cpf_exists(self, cpf: str):
        self.db.ensure_connection()
        cursor = self.db.connection.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE cpf = %s", (cpf,))
        existing_user = cursor.fetchone()
        return existing_user
    

    def check_fields(self, data: dict):
        required_fields = ['cpf', 'password']
        for field in required_fields:
            if field not in data:
                return jsonify({"message": f"Campo '{field}' é obrigatório."}), 400
            

    def password_user_db(self, cpf: str):
        self.db.ensure_connection()
        cursor = self.db.connection.cursor()
        try:
            cursor.execute("SELECT senha FROM usuarios WHERE cpf = %s", (cpf,))
            result = cursor.fetchone()
            if result:
                return result[0].encode('utf-8')
        except Exception as e:
            print(f'Erro: {e}')
            return None
            

    def login_user(self):
        data = request.get_json()   
        try:
            self.db.ensure_connection()
            self.check_fields(data)
            cpf = data['cpf']
            password = data['password']
            existing_user = self.check_cpf_exists(cpf)

            if existing_user:
                hashed_password_db = self.password_user_db(cpf)
                hasRegister = Cryptography.check_password(password, hashed_password_db)

                if hasRegister:
                    user_name = existing_user[1]
                    access_token = create_access_token(identity=cpf)
                    return jsonify({
                        'token': access_token,
                        'userName': user_name,
                        'message': 'Login efeutuado com sucesso'
                    })
                else:
                    return jsonify({'message': 'Senha incorreta'}), 401
                
            else:
                return jsonify({'message': 'CPF não cadastrado'}), 401
        
        except KeyError as e:
            return jsonify({"message": f"Campo ausente: {str(e)}"}), 400
        except Exception as e:
            return jsonify({"message": f"Erro interno: {str(e)}"}), 500

    @jwt_required()
    def protected(self):
        current_user = get_jwt_identity()
        return jsonify({
            'message': f'bem vindo(a), user {current_user}'
        })