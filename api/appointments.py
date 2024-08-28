from flask import request, jsonify
from flask_cors import cross_origin

def appointment_routes(self):
    """Define Flask routes."""
    @self.app.route('/api/appointments/forPatient', methods=['GET'])
    @cross_origin(supports_credentials=True)
    def pull():
        """Retrieves appointments viewable on patients side: by time in a date"""
        month = request.args.get('month', type=int)
        year = request.args.get('year', type=int)
        if request.args.get('day') != 'null':
            day = request.args.get('day', type=int)
        else:
            day = None
        conn = self.connect_db()
        cursor = conn.cursor()
        try:
            # Execute SQL query to get user information by user_id
            if day is not None:
                cursor.execute("SELECT * FROM tblappointment WHERE Appointment_Month = %s AND Appointment_Year = %s AND Appointment_Day = %s", (month, year, day))
            else:
                cursor.execute("SELECT * FROM tblappointment WHERE Appointment_Month = %s AND Appointment_Year = %s", (month, year))

            rows = cursor.fetchall()

            # Get column names from cursor description
            column_names = [desc[0] for desc in cursor.description]
        

            # Convert rows to a list of dictionaries with column names as keys
            result = []
            for row in rows:
                result.append(dict(zip(column_names, row)))
           
            print(result)
            return jsonify(result), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
        finally:
            cursor.close()
            conn.close()


    @self.app.route('/api/appointments', methods=['POST'])
    def push():
        """Add a new user to the database."""
        conn = self.connect_db()
        cursor = conn.cursor()
        try:
            # Get data from the request body
            data = request.json
            data = (
                data.get('Appointment_ID'),
                data.get()
            )

            # Insert new user into the database
            cursor.execute(
                
                "CALL insert_patient (%s,%s,%s,%s,%s,%s)",
             ("Roan", "Langreo", "Roo11", "123", "roan@email.com", "096782")
            )
            conn.commit()

            return jsonify({"message": "User added successfully"}), 201
        except Exception as e:
            conn.rollback()  # Rollback transaction on error
            return jsonify({"error": str(e)}), 500
        finally:
            cursor.close()
            conn.close()