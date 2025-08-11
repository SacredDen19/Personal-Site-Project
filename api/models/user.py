from api.datab import db_start_connection as db
from datetime import datetime

class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.datetime.now())

    def to_jsonify(self):
        return {
            "Userid": self.user_id,
            "Username":self.user_name,
            "Password": self.password,
            "DateCreated": self.date_created,
        }