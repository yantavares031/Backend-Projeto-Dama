from flask import Blueprint, Flask
from flask_cors import CORS
from models.Database import Database
from models.UserLogin import UserLogin
from models.AdminLogin import AdminLogin
from models.UserRegister import UserRegister
from models.AdminRegister import AdminRegister
from models.TournamentManager import TournamentManager
from flask_jwt_extended import (
    JWTManager, create_access_token, jwt_required, get_jwt_identity
)
from datetime import timedelta

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "sua_chave_super_secreta"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
jwt = JWTManager(app)

CORS(app)
db = Database("45.181.230.74", "root", "WikitelecomuGr+dX@u2%", 'federacao_dama')

api_bp = Blueprint('api', __name__, url_prefix='/api')

user_register = UserRegister(api_bp, db)
user_login = UserLogin(app, db)
admin_login = AdminLogin(app, db)
admin_register = AdminRegister(api_bp, db)
tournament_manager = TournamentManager(api_bp, db)
app.register_blueprint(api_bp)

if __name__ == "__main__":
    app.run()