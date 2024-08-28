from flask import request
from flask_cors import cross_origin
from utilities.util_functions import pull_from_db, push_to_db, update_db, delete_from_db

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
    
