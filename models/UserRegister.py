from requests import get
from flask_cors import CORS
from models.Database import Database
from flask import Flask, request, jsonify
from models.Cryptography import Cryptography


class UserRegister:


    def __init__(self, app: Flask, db: Database):
        self.db = db
        CORS(app)
        app.add_url_rule('/user/register', 'register_user', self.register_user, methods=['POST'])


    def search_cep(self, cep: str):
        url_viacep = f'https://viacep.com.br/ws/{cep}/json/'
        response = get(url_viacep)
        
        if response.status_code == 200:
            response_json = response.json()
            state = response_json['estado']
            city = response_json['localidade']
            street = response_json['logradouro']
            neighborhood = response_json['bairro']
            complement = response_json['complemento']
            return {
                "state": state,
                "city": city,
                "neighborhood": neighborhood,
                "street": street,
                "complement": complement
            }
        else:
            print(f'Falha na requisição api viacep: {response.status_code}')
            return {'message': 'erro na requisição api viacep'}, 400


    def check_cpf_exists(self, cpf: str):
        self.db.ensure_connection()
        cursor = self.db.connection.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE cpf = %s", (cpf,))
        existing_user = cursor.fetchone()
        return existing_user
    

    def check_fields(self, data: dict):
        required_fields = ['name', 'cpf', 'birthdate', 'phone', 'cep', 'email', 'password']
        for field in required_fields:
            if field not in data:
                return jsonify({"message": f"Campo '{field}' é obrigatório."}), 400
            

    def register_user(self):
         
         try:
            data = request.get_json()

            self.check_fields(data)

            name = data['name'].upper()
            cpf = data['cpf']

            existing_user = self.check_cpf_exists(cpf)
            if existing_user:
                return jsonify({"message": "CPF já cadastrado!"}), 400

            birthdate = data['birthdate']
            ddd = data['phone'][0:2]
            phone = data['phone'][2:]
            cep = data['cep']
            email = data['email'].lower()
            password = data['password']

            hashed_password = Cryptography.hash_password(password)

            address_info = self.search_cep(cep)
            if 'message' in address_info:
                return jsonify({"message": "CEP inválido ou não encontrado."}), 400

            insert_query = """
                INSERT INTO usuarios (nome, cpf, data_nascimento, ddd, telefone, cep, estado, localidade, logradouro, bairro, complemento, email, senha)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
            """
            
            data_to_insert = (
                name, cpf, birthdate, ddd, phone, cep, 
                address_info['state'], address_info['city'], 
                address_info['street'], address_info['neighborhood'], 
                address_info['complement'], email, hashed_password
            )

            self.db.ensure_connection()
            self.db.execute_query(insert_query, data_to_insert)

            return jsonify({
                "message": "Usuário registrado com sucesso!",
                "data": {
                    "name": name,
                    "cpf": cpf,
                    "birthdate": birthdate,
                    "phone": phone,
                    "email": email,
                    "address": address_info
                }
            }), 201

         except KeyError as e:
            return jsonify({"message": f"Campo ausente: {str(e)}"}), 400
         except Exception as e:
            return jsonify({"message": f"Erro interno: {str(e)}"}), 500
