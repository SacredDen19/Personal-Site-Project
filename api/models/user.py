from ..models.Model import Model
from api.datab import db_start_connection as db
from datetime import datetime

class getUser(Model):
    table_name = 'users'
    column_id = 'Username'

    def __init__(self, Userid, Username, Password, created_at):
        self.Userid = Userid
        self.Username = Username
        self.Password = Password
        self.created_at = created_at

    def to_json(self):
        dict =  {
            "Userid": self.Userid,
            "Username":self.Username,
            "Password": self.Password,
            "Date Created": self.created_at,
        }
        return dict
    
    def __repr__(self):
        dict =  {
            "Userid": self.Userid,
            "Username":self.Username,
            "Password": self.Password,
            "Date Created": self.created_at,
        }
        return f'{dict}'