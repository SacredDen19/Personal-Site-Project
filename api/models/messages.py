from ..models.Model import Model

class message(Model):
    #Assigns the respective table and row information
    table_name = 'message'
    column_id = 'parent_conversation_id'

    #Object constructor
    #Assigns the class some values when a new instance of it is created
    def __init__(self, message_id, message_text, sent_by_id, parent_conversation_id, datetime_sent): #self always points to the actual object instance this case being conversation
        self.message_id = message_id
        self.message_text = message_text
        self.sent_by_id = sent_by_id
        self.parent_conversation_id = parent_conversation_id
        self.datetime_sent = datetime_sent

    def __repr__(self): #repr worked since we are returning a tuple of objects with fetchall. to_dict is used to return a dictionary
                        #and repr is more for debugging
        dict = {
            'message_id' : self.message_id,
            'message_text': self.message_text,
            'sent_by_id': self.sent_by_id,
            'parent_conversation_id': self.parent_conversation_id,
            'datetetime_sent': self.datetime_sent,
        }
        #print(f'str method ran! Dictionary: {dict}')
        return f'{dict}'
    
    def to_dict(self): #repr worked since we are returning a tuple of objects with fetchall. to_dict is used to return a dictionary
                    #and repr is more for debugging
        dict = {
            'message_id' : self.message_id,
            'message_text': self.message_text,
            'sent_by_id': self.sent_by_id,
            'parent_conversation_id': self.parent_conversation_id,
            'datetetime_sent': self.datetime_sent,
        }
        #print(f'str method ran! Dictionary: {dict}')
        return dict
