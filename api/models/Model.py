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
            case 'UPDATE':
                query_command = f"SELECT * FROM {cls.table_name} WHERE {cls.column_id} = %s"
                db_cursor.execute(query_command, (kwargs['record_id'],))
                pass
            case 'DELETE':
                query_command = f"SELECT * FROM {cls.table_name} WHERE {cls.column_id} = %s"
                db_cursor.execute(query_command, (kwargs['record_id'],))
                pass


    @classmethod #built-in decorator that runs the function from the class as part of the class and not within the class
    #cls is common name for the class passing/calling this method and record_id is used to define the individual calling table
    #record_id is the ID of the column of the table calling it + operation is the operation being done on the database
    def caller_id(cls, sql_operation, **kwargs): 
        conn = db()
        cursor = conn.cursor(dictionary=True)
        operation = sql_operation
        if kwargs.get('record_id'):
            entry_id = kwargs['record_id']
            output = cls.CRUD_FUNCTION(cls, operation, cursor, conn, record_id=entry_id)
        elif kwargs.get('parent_id'):
            sent_by = kwargs['sent_by'] #Sets the sent_id for insertion
            raw_text = kwargs['raw_text']
            parent_id = kwargs['parent_id']
            username = kwargs['user']
            output = cls.CRUD_FUNCTION(cls, operation, cursor, conn, sent_by=sent_by, raw_text=raw_text, parent_id=parent_id, username=username)

        if output:
            #for row in output:      ----DEBUGGING----
                #print(f'RAW TUPLE OUTPUT: {output}')
                #print(f'MySQL OUTPUT ROW: {row}')
                #print("Returning this below: ")
                #print([cls(**row) for row in output])
            return [cls(**row) for row in output]
        return None