from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask_wtf.csrf import CSRFProtect
import builtins
builtins.unicode = str
from flask_triangle import Triangle

app = Flask(__name__, static_path='/static')
Triangle(app)
#form csrf protect token upload images
csrf = CSRFProtect(app)
#databse
db = SQLAlchemy(app)
migrate = Migrate(app,db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)
#config.py
app.config.from_object('config')
from app import views,models
manager.run()

