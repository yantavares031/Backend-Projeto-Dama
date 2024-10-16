from flask import Flask
from flask_cors import CORS
from models.Database import Database
from models.UserLogin import UserLogin
from models.AdminLogin import AdminLogin
from models.UserRegister import UserRegister
from models.AdminRegister import AdminRegister
from models.TournamentManager import TournamentManager

app = Flask(__name__)
CORS(app)
db = Database("45.181.230.74", "root", "WikitelecomuGr+dX@u2%", 'c')

user_register = UserRegister(app, db)
user_login = UserLogin(app, db)

admin_login = AdminLogin(app, db)
admin_register = AdminRegister(app, db)

tournament_manager = TournamentManager(app, db)

app.run(host='0.0.0.0', debug=True)