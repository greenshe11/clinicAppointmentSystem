from flask import jsonify

def get_query(cursor, table_name, data, method, filter_names):
    """
        optional:
            filter_names (string []): to be used for PUT and DELETE methods. 
                the query will use the values from data passed as filter values for filter_names for filtering purposes,
                and will exclude them to selected/target columns.

                for the case of GET, it will count the whole data as filter. Thus, will count as target columns.
    """

    # Class for easy access of values
    class Query:
        def __init__(self, statement, values):
            self.statement = statement
            self.values = values

    # gets the column names from table name
    cursor.execute(f"SELECT * FROM {table_name} LIMIT 1") 
    column_names = [description[0] for description in cursor.description]

    # values and placeholders
    columns_selected = []
    filter_columns = []
    filter_values = []
    values = []

    # distributes data to its corresponding types above
    for colname in column_names:
        for data_key in data.keys():
            if colname == data_key: # only takes data/keys that are found in database columns
                if colname in filter_names: # distributes data as filter
                    filter_columns.append(colname)
                    filter_values.append(data[colname])
                else: # distributes data as target columns
                    columns_selected.append(colname)
                    values.append(data[colname])

    
    # storing WHERE statement to this variable for shortening
    insert_filter = ' AND '.join(['{} = %s'.format(name) for name in filter_columns])


    # make statements using correct sql syntax based on request method
    if method.upper() == "GET":
        statement = f"SELECT * FROM {table_name} WHERE {' AND '.join(['{} = %s'.format(name) for name in columns_selected])}"

    elif method.upper() == "POST":
        statement = f"INSERT INTO {table_name} ({', '.join(columns_selected)}) VALUES ({', '.join('%s' for x in range(len(columns_selected)))})"

    elif method.upper() == "PUT":
        statement = f"UPDATE {table_name} SET {', '.join(['{} = %s'.format(name) for name in columns_selected])} WHERE {insert_filter}"
        for x in filter_values: # with the current values, filter values at the end
            values.append(x) 

    elif method.upper() == "DELETE":
        statement = f"DELETE FROM {table_name} WHERE {insert_filter}"
        values = filter_values # delet method doesnt use values. for this case, filter values will be the only values passed.

    values = tuple(values)
    return Query(statement, values)

def pull_from_db(self, data, table_name):
    try:
        conn = self.connect_db()
        cursor = conn.cursor()
        query = get_query(cursor=cursor,
                            table_name=table_name,
                            data=data,
                            method='get')
        
        cursor.execute(query.statement, query.values)
        
        rows = cursor.fetchall()

        column_names = [desc[0] for desc in cursor.description]
        result = []
        for row in rows:
            result.append(dict(zip(column_names, row)))
    
        return jsonify(result), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

def push_to_db(self, data, table_name, success_response = None):
    if success_response is None:
        success_response =  {"message": f'New instance is added to {table_name}!'}
    try:
        conn = self.connect_db()
        cursor = conn.cursor()
        query = get_query(cursor, table_name, data, 'post')

        # Insert new user into the database
        cursor.execute(query.statement, query.values)
        conn.commit()

        return jsonify(success_response), 201
    except Exception as e:
        conn.rollback()  # Rollback transaction on error
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()


def update_db(self, data, table_name, filter_names, success_response = None):
    if success_response is None:
        success_response = {"message": f'An instance from {table_name} is updated!'}
    conn = self.connect_db()
    cursor = conn.cursor()
    try:
        # Update user information
        query = get_query(cursor, table_name, data, method = 'put', filter_names = filter_names)
        cursor.execute(
            query.statement,
            query.values
        )

        conn.commit()

        if cursor.rowcount == 0:
            return jsonify({"error": "User not found"}), 404

        return jsonify(success_response), 200
    except Exception as e:
        conn.rollback()  # Rollback transaction on error
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

def delete_from_db(self, data, table_name, filter_names, success_response = None):
    if success_response is None:
        success_response = {"message": 'An instance from {table_name} is deleted!'}
    
   
    try:
        conn = self.connect_db()
        cursor = conn.cursor()
        query = get_query(cursor, table_name, data, method='delete', filter_names=filter_names)
        # Delete user from the database
        cursor.execute(
            query.statement, 
            query.values
        )
        conn.commit()

        if cursor.rowcount == 0:
            return jsonify({"error": "User not found"}), 404

        return jsonify({"message": "User deleted successfully"}), 200
    except Exception as e:
        conn.rollback()  # Rollback transaction on error
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()