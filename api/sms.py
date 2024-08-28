from flask import request
from flask_cors import cross_origin
from utilities.util_functions import pull_from_db, push_to_db, update_db, delete_from_db

def sms_routes(self, table_name):
    """Define Flask routes."""

    @self.app.route('/api/sms', methods=['GET'])
    @cross_origin(supports_credentials=True)
    def sms_pull():
        # url parameters will are used for filtering
        data = request.args.to_dict()
        processed_data = {}

        for key, value in zip(data.keys(), data.values()):
            if value != 'null':
                processed_data[key] = int(value)
        
        return pull_from_db(self, processed_data, table_name)

    @self.app.route('/api/sms', methods=['POST'])
    def sms_push():
        """Add a new user to the database."""
        data = request.json
        return push_to_db(self, data, table_name=table_name)

    
    @self.app.route('/api/sms', methods=['PUT'])
    def sms_update():
        data = request.json
        print(data)
        return update_db(self, data, table_name, filter_names=['Smsnotif_ID'])
    
    @self.app.route('/api/sms', methods=['DELETE'])
    def sms_delete():
        data = request.json
        print(data)
        return delete_from_db(self, data, table_name, filter_names = ['Smsnotif_ID'])