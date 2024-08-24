from flask import request, jsonify

def patient_routes(self):
    """Define Flask routes."""

    @self.app.route('/api/patient', methods=['GET'])
    def pull_all():
        """Retrieve all users from the database."""
        conn = self.connect_db()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM accounts")
            rows = cursor.fetchall()
            # Convert rows to a list of dictionaries
            result = []
            for row in rows:
                result.append({
                    'id': row[0],
                    'email': row[1],
                    'password': row[2]
                })
            return jsonify(result), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
        finally:
            cursor.close()
            conn.close()

    @self.app.route('/api/patient/<int:user_id>', methods=['GET'])
    def pull(user_id):
        """Retrieve a specific user's information from the database based on user_id."""
        conn = self.connect_db()
        cursor = conn.cursor()
        try:
            # Execute SQL query to get user information by user_id
            cursor.execute("SELECT * FROM accounts WHERE id = %s", (user_id,))
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

    @self.app.route('/api/patient', methods=['POST'])
    def push():
        """Add a new user to the database."""
        conn = self.connect_db()
        cursor = conn.cursor()
        try:
            # Get data from the request body
            data = request.json
            email = data.get('email')
            password = data.get('password')

            # Insert new user into the database
            cursor.execute(
                "INSERT INTO accounts (email, password) VALUES (%s, %s)",
                (email, password)
            )
            conn.commit()

            return jsonify({"message": "User added successfully"}), 201
        except Exception as e:
            conn.rollback()  # Rollback transaction on error
            return jsonify({"error": str(e)}), 500
        finally:
            cursor.close()
            conn.close()

    @self.app.route('/api/patient', methods=['PUT'])
    def update():
        """Update a user's information in the database."""
        conn = self.connect_db()
        cursor = conn.cursor()
        try:
            # Get data from the request body
            data = request.json
            user_id = data.get('id')
            email = data.get('email')
            password = data.get('password')

            # Validate input
            if not email or not password:
                return jsonify({"error": "Missing required fields"}), 400

            # Update user information
            cursor.execute(
                "UPDATE accounts SET email = %s, password = %s WHERE id = %s",
                (email, password, user_id)
            )
            conn.commit()

            if cursor.rowcount == 0:
                return jsonify({"error": "User not found"}), 404

            return jsonify({"message": "User updated successfully"}), 200
        except Exception as e:
            conn.rollback()  # Rollback transaction on error
            return jsonify({"error": str(e)}), 500
        finally:
            cursor.close()
            conn.close()

    @self.app.route('/api/patient', methods=['DELETE'])
    def delete():
        """Delete a user from the database."""
        conn = self.connect_db()
        cursor = conn.cursor()
        # Get data from the request body
        data = request.json
        user_id = data.get('id')
        try:
            # Delete user from the database
            cursor.execute(
                "DELETE FROM accounts WHERE id = %s",
                (user_id,)
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
