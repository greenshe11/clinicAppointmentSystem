from flask import request, jsonify
from flask_cors import cross_origin
from utilities.util_functions import pull_from_db, push_to_db, update_db, delete_from_db, remove_sessions, calendar, hashPassword, get_session, set_session, check_password

def patient_routes(self, table_name):
    """Define Flask routes."""

    @self.app.route('/api/patient', methods=['GET'])
    @cross_origin(supports_credentials=True)
    def patient_pull():
        # example: http://localhost:5000/api/patient?Patient_ID=10
        # url parameters will are used for filtering
        data = request.args.to_dict()
        processed_data = {}

      
        arguments = data
        # having parameter: "for" will have special processes
        if 'for' in arguments.keys():
            if arguments['for'] == 'session':
                processed_data = {'Patient_ID': get_session('userId')}
            
        else:
            for key, value in zip(data.keys(), data.values()):
                if value != 'null':
                    processed_data[key] = int(value)

        
        return pull_from_db(self, processed_data, table_name)
    
    @self.app.route('/api/patient/getCalendar', methods=['GET'])
    @cross_origin(supports_credentials=True)
    def patient_pull_calendar():
        return jsonify({"html": calendar.html})

    @self.app.route('/api/patient', methods=['POST'])
    def patient_push():
        """Add a new user to the database."""
        data = request.json

       
        arguments = request.args.to_dict()
        # having parameter: "for", will give special processes
        if "for" in arguments.keys():
            if arguments['for'] == 'registration':
                # For security purpose, encrypts password sent to database
                data["PatientPassword"] = hashPassword(data["PatientPassword"])
                duplicates = pull_from_db(self, {"PatientEmail": data['PatientEmail'], "PatientContactNo": data["PatientContactNo"]}, table_name, jsonify_return=False, logical_op="OR")
                print(duplicates)
                if len(duplicates) > 0:
                    return jsonify({"customError": "Contact No. or Email is in use!"}), 200
        
            if arguments['for'] == 'login':
                credentials = pull_from_db(self, {"PatientEmail": data['PatientEmail']}, table_name, jsonify_return=False)
                print(credentials)
                #correct_password = hashPassword(data["PatientPassword"]) == credentials[0]['PatientPassword']
                correct_password = check_password(data["PatientPassword"], credentials[0]["PatientPassword"])
                
                if correct_password:
                    set_session('userId', credentials[0]['Patient_ID'])
                    # logging in doesnt require to add data to database atm; returns back to the client immediately without error
                    # all good as long as session has been set
                    return jsonify({})
                else:
                    return jsonify({"customError": "Password or Email is incorrect!"}), 200
                
            if arguments['for'] == 'logout':
                # logging out doesnt require to add data to database atm; returns back to the client immediately without error
                # all good as long as session has been removed
                remove_sessions()
                return jsonify({}), 201
                

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
    
