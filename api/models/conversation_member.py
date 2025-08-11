from ..models.Model import Model

class conversation_member(Model):
    #Assigns the respective table and row information
    table_name = 'conversation_member'
    column_id = 'user_id'

    #Object constructor
    #Assigns the class some values when a new instance of it is created
    def __init__(self, conv_id, user_id, datetime_joined, datetime_left): #self always points to the actual object instance this case being conversation
        self.conv_id = conv_id
        self.user_id = user_id
        self.datetime_joined = datetime_joined
        self.datetime_left = datetime_left

    def __repr__(self): #repr worked since we are returning a tuple of objects with fetchall
        dict = {
            'conv_id' : self.conv_id,
            'user_id': self.user_id,
            'datetime_joined': self.datetime_joined,
            'datetime_left': self.datetime_left,
        }
        ##print(f'str method ran! Dictionary: {dict}')
        return f'{dict}'
