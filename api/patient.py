from flask import request, jsonify
from flask_cors import cross_origin
from utilities.util_functions import pull_from_db, push_to_db, update_db, delete_from_db, hashPassword, set_session, get_session

def patient_routes(self, table_name):
    """Define Flask routes."""

    @self.app.route('/api/patient', methods=['GET'])
    @cross_origin(supports_credentials=True)
    def patient_pull():
        # example: http://localhost:5000/api/patient?Patient_ID=10
        # url parameters will are used for filtering
        data = request.args.to_dict()
        processed_data = {}

        for key, value in zip(data.keys(), data.values()):
            if value != 'null':
                processed_data[key] = int(value)
        
        return pull_from_db(self, processed_data, table_name)

    @self.app.route('/api/patient', methods=['POST'])
    def patient_push():
        """Add a new user to the database."""
        data = request.json

        # For security purpose, encrypts password sent to database
        arguments = request.args.to_dict()
        if arguments['for'] == 'registration':
            data["PatientPassword"] = hashPassword(data["PatientPassword"])
            duplicates = pull_from_db(self, {"PatientEmail": data['PatientEmail'], "PatientContactNo": data["PatientContactNo"]}, table_name, jsonify_return=False, logical_op="OR")
            print(duplicates)
            if len(duplicates) > 0:
                return jsonify({"customError": "Contact No. or Email is in use!"}), 200
       
        if arguments['for'] == 'login':
            credentials = pull_from_db(self, {"PatientEmail": data['PatientEmail']}, table_name, jsonify_return=False)
            correct_password = hashPassword(data["PatientPassword"]) == credentials[0]['PatientPassword']
            set_session('userId', credentials[0]['Patient_ID'])
            if correct_password:
                return jsonify({"customError": "Password or Email is incorrect!"}), 200

        return push_to_db(self, data, table_name=table_name)

    @self.app.route('/api/patient', methods=['PUT'])
    def patient_update():
        data = request.json
        print(data)
        return update_db(self, data, table_name, filter_names=['Patient_ID'])
    
    @self.app.route('/api/patient', methods=['DELETE'])
    def patient_delete():
        data = request.json
        print(data)
        return delete_from_db(self, data, table_name, filter_names = ['Patient_ID'])
    
