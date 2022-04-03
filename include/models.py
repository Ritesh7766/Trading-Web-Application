from include import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True) 
    username = db.Column(db.String(20), unique = True, nullable = False)
    email = db.Column(db.String(120), unique = True, nullable = False)
    password = db.Column(db.String(60), nullable = False)

    # Specifying how the object is printed whenever we print it out.
    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"


class Stocks_Owned(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key = True)
    stock_id = db.Column(db.String(20), primary_key = True)
    quantity = db.Column(db.Integer, nullable = False)

    # Specifying how the object is printed whenever we print it out.
    def __repr__(self):
        return f"Stocks_Owned('{self.user_id}', '{self.stock_id}, '{self.quantity}')"
