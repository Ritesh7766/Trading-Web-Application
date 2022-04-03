from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = '4a7649d351c052cc24f8f64f3a95f580' # Required for POST requests. Will add this to enviroment variables later.
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///finance.db'   # For testing we will use sqlite3.

# Database instance
db = SQLAlchemy(app)

from include import routes