from models.Database import Database
from flask import Flask, request, jsonify

class TournamentManager:


    def __init__(self, app: Flask, db: Database):
        self.db = db
        app.add_url_rule('/tournaments', 'create_tournament', self.create_tournament, methods=['POST'])
        app.add_url_rule('/view-tournaments', 'get_tournaments', self.get_tournaments, methods=['GET'])
        app.add_url_rule('/tournaments/<int:tournament_id>', 'delete_tournament', self.delete_tournament, methods=['DELETE'])
        app.add_url_rule('/tournaments/<int:tournament_id>', 'update_tournament', self.update_tournament, methods=['PUT'])


    def create_tournament(self):
        data = request.get_json()
        try:
            required_fields = ['tournamentName', 'date', 'location', 'qtd_participants', 'registration_price']
            for field in required_fields:
                if field not in data:
                    return jsonify({"message": f"Campo '{field}' é obrigatório."}), 400
            
            tournament_name = data['tournamentName']
            date = data['date']
            location = data['location']
            qtd_participants = data['qtd_participants']
            registration_price = data['registration_price']

            self.db.ensure_connection()
            cursor = self.db.connection.cursor()
            cursor.execute("""
                INSERT INTO tournament (tournament_name, date_tournament, location, qtd_participants, registration_price)
                VALUES (%s, %s, %s, %s, %s)
            """, (tournament_name, date, location, qtd_participants, registration_price))
            self.db.connection.commit()
            return jsonify({"message": "Torneio criado com sucesso!"}), 201
        
        except Exception as e:
            print(f'Erro ao criar torneio: {e}')
            return jsonify({"message": "Erro ao criar torneio."}), 500


    def get_tournaments(self):
        self.db.ensure_connection()
        cursor = self.db.connection.cursor()
        cursor.execute('SELECT * FROM tournament;')
        tournaments = cursor.fetchall()
        list_tournaments = []
        for tournament in tournaments:
            list_tournaments.append({
                'id': tournament[0],
                'Name': tournament[1],
                'Date': tournament[2],
                'Locale': tournament[3],
                'Qtd_participants': tournament[4],
                'Taxe_pay': float(tournament[5])})
        return jsonify(list_tournaments)


    def update_tournament(self, tournament_id):
        data = request.get_json()
        try:
            tournament_name = data['tournamentName']
            date = data['date']
            location = data['location']
            qtd_participants = data['qtd_participants']
            registration_price = data['registration_price']

            self.db.ensure_connection()
            cursor = self.db.connection.cursor()

            cursor.execute("""
                UPDATE tournament 
                SET tournament_name = %s, date_tournament = %s, location = %s, 
                    qtd_participants = %s, registration_price = %s 
                WHERE id = %s
            """, (tournament_name, date, location, qtd_participants, registration_price, tournament_id))
            self.db.connection.commit()

            return jsonify({"message": "Torneio atualizado com sucesso!"}), 200

        except Exception as e:
            print(f'Erro ao atualizar torneio: {e}')
            return jsonify({"message": "Erro ao atualizar torneio."}), 500


    def delete_tournament(self, tournament_id):
        try:
            self.db.ensure_connection()
            cursor = self.db.connection.cursor()
            cursor.execute("DELETE FROM tournament WHERE id = %s", (tournament_id,))
            self.db.connection.commit()
            
            if cursor.rowcount == 0:
                return jsonify({"message": "Torneio não encontrado."}), 404
            
            return jsonify({"message": "Torneio excluído com sucesso!"}), 200

        except Exception as e:
            print(f'Erro ao deletar torneio: {e}')
            return jsonify({"message": "Erro ao deletar torneio."}), 500