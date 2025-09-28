from api.datab import db_start_connection as db

#ORM Base Model that will return specific tables when called by their respective ORM
class Model():

    table_name = None #This will be assingned by the working table
    column_id = None #Will also be set by the table

    #Defines the operation function which will handle MySQL operations.
    def CRUD_FUNCTION(cls, operation, db_cursor, db_connection,**kwargs):
        match operation:
            case 'READ':
                query_command = f"SELECT * FROM {cls.table_name} WHERE {cls.column_id} = %s"
                db_cursor.execute(query_command, (kwargs['record_id'],))
                output = db_cursor.fetchall()
                return output
            case 'WRITE':
                print("WRITE OPERATION STARTED")
                query_command = f"INSERT INTO {cls.table_name} (message_text, sent_by_id, parent_conversation_id, username) VALUES (%s, %s, %s, %s)"
                db_cursor.execute(query_command, (kwargs['raw_text'], kwargs['sent_by'], kwargs['parent_id'], kwargs['username']))
                db_connection.commit()
                return print("WRITE OPERATION SUCCESS")
            case 'WRITE-CONVERSATION':
                query_command = f"INSERT INTO {cls.table_name} (conversation_name, created_by) VALUES  (%s, %s)"
                db_cursor.execute(query_command, (kwargs['conversation_name'], kwargs['created_by']))
                db_connection.commit()
            case 'WRITE_CONVERSATION_MEMBER':
                query_command = f"INSERT INTO {cls.table_name} (conv_id, user_id, username) VALUES  (%s, %s, %s)"
                db_cursor.execute(query_command, (kwargs['conv_id'], kwargs['user_id'], kwargs['username']))
                db_connection.commit()


    @classmethod #built-in decorator that runs the function from the class as part of the class and not within the class
    #cls is common name for the class passing/calling this method and record_id is used to define the individual calling table
    #record_id is the ID of the column of the table calling it + operation is the operation being done on the database
    def caller_id(cls, sql_operation, **kwargs): 
        conn = db()
        cursor = conn.cursor(dictionary=True)
        operation = sql_operation
        if kwargs.get('record_id'): #checks if kwargs is getting record-id (conversation_id) passed if not moves on to message post operation 
            entry_id = kwargs['record_id']
            output = cls.CRUD_FUNCTION(cls, operation, cursor, conn, record_id=entry_id)
        elif kwargs.get('parent_id'): #checks of kwargs is being passed parent_id, if it is, then a user is sending a message, otherwise nothing else happens
            sent_by = kwargs['sent_by'] #Sets the sent_id for insertion
            raw_text = kwargs['raw_text']
            parent_id = kwargs['parent_id']
            username = kwargs['user']
            output = cls.CRUD_FUNCTION(cls, operation, cursor, conn, sent_by=sent_by, raw_text=raw_text, parent_id=parent_id, username=username)
        elif kwargs.get('created_by'): #Checks if a userID is being passed from the back end route to create a new conversation
            title = kwargs.get('title')
            created_by = kwargs.get('created_by')
            output = cls.CRUD_FUNCTION(cls,operation, cursor, conn, conversation_name=title, created_by=created_by)
        elif kwargs.get('conv_id'): #Checks if a conv_id is being passed which means new conversation members are being added for this context
            conv_id = kwargs['conv_id']
            user_id = kwargs['user_id']
            username = kwargs['username']
            output = cls.CRUD_FUNCTION(cls, operation, cursor, conn, conv_id=conv_id, user_id=user_id, username=username)
            
        if output:
            #for row in output:      ----DEBUGGING----
                #print(f'RAW TUPLE OUTPUT: {output}')
                #print(f'MySQL OUTPUT ROW: {row}')
                #print("Returning this below: ")
                #print([cls(**row) for row in output])
            return [cls(**row) for row in output]
        return None