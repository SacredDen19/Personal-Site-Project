from ..models.Model import Model

##class conversation_create():
##    __tablename__ = 'conversation'
  ##  conversation_id = db.Column(db.Integer, primary_key=True)
    ##conversation_name = db.Column(db.String(80), unique=True, nullable=False)
    ##date_created = db.Column(db.DateTime)
    ##created_by = db.Column(db.Integer, db.ForeignKey('users.Userid'))

    ##def to_jsonify(self):
    ##    return {
    ##        "Userid": self.user_id,
    ##        "Username":self.user_name,
    ##        "Password": self.password,
    ##       "DateCreated": self.date_created,
    ##    }
    

    

class conversation(Model):
    #Assigns the respective table and row information
    table_name = 'conversation'
    column_id = 'conversation_id'

    #Object constructor
    #Assigns the class some values when a new instance of it is created
    def __init__(self, conversation_id, conversation_name, date_created, created_by): #self always points to the actual object instance this case being conversation
        self.conversation_id = conversation_id
        self.conversation_name = conversation_name
        self.date_created = date_created
        self.created_by = created_by

    def __str__(self):
        dict = {
            'conversation_id' : self.conversation_id,
            'conversation_name': self.conversation_name,
            'date_created': self.date_created,
            'created_by': self.created_by,
        }
        return f'{dict}'


