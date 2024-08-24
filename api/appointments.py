from flask import request, jsonify
from flask_cors import cross_origin

def appointment_routes(self):
    """Define Flask routes."""

    @self.app.route('/api/appointments/forPatient', methods=['GET'])
    @cross_origin(supports_credentials=True)
    def client_appointments():
        """Retrieves appointments viewable on patients side: by time in a date"""
        month = request.args.get('month', type=int)
        year = request.args.get('year', type=int)
        day = request.args.get('day', type=int)
        conn = self.connect_db()
        cursor = conn.cursor()
        try:
            # Execute SQL query to get user information by user_id
            cursor.execute("SELECT * FROM tblappointment WHERE appointment_month = %s AND appointment_year = %s AND appointment_day = %s", (month, year, day))
            rows = cursor.fetchall()

            # Get column names from cursor description
            column_names = [desc[0] for desc in cursor.description]

            # Convert rows to a list of dictionaries with column names as keys
            result = []
            for row in rows:
                result.append(dict(zip(column_names, row)))

            return jsonify(result), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
        finally:
            cursor.close()
            conn.close()
