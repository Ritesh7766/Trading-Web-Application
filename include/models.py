from include import db, bcrypt, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True, autoincrement = True) 
    username = db.Column(db.String(20), unique = True, nullable = False)
    email = db.Column(db.String(120), unique = True, nullable = False)
    password_hash = db.Column(db.String(60), nullable = False)

    # Specifying how the object is printed whenever we print it out.
    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

    @property
    def password(self):
        return self.password

    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    def check_password(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)



class Stocks_Owned(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key = True)
    stock_id = db.Column(db.String(20), primary_key = True)
    quantity = db.Column(db.Integer, nullable = False)

    # Specifying how the object is printed whenever we print it out.
    def __repr__(self):
        return f"Stocks_Owned('{self.user_id}', '{self.stock_id}, '{self.quantity}')"
