from api.datab import db_start_connection as db

#ORM Base Model that will return specific tables when called by their respective ORM
class Model():

    table_name = None #This will be assingned by the working table
    column_id = None #Will also be set by the table

    @classmethod #built-in decorator that runs the function from the class as part of the class and not within the class
    def caller_id(cls, record_id): #cls is common name for the class passing/calling this method and record_id is used to define the individual calling table
        conn = db()
        cursor = conn.cursor(dictionary=True)
        query_command = f"SELECT * FROM {cls.table_name} WHERE {cls.column_id} = %s"

        cursor.execute(query_command, (record_id,))

        output = cursor.fetchall()

        if output:
            #for row in output:
                #print(f'RAW TUPLE OUTPUT: {output}')
                #print(f'MySQL OUTPUT ROW: {row}')
                #print("Returning this below: ")
                #print([cls(**row) for row in output])
            return [cls(**row) for row in output]
        return None