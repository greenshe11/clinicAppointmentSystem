from dotenv import load_dotenv
import os
import MySQLdb as Mysqldb
from flask import Flask, render_template, redirect
from flask_mysqldb import MySQL
from flask_cors import CORS
# Load environment variables from .env file

#api routes
from api.patient import patient_routes
from api.appointments import appointment_routes
from api.diagnosis import diagnosis_routes
from api.sms import sms_routes

# utils
from utilities import util_functions as util


load_dotenv()

class App:
    def __init__(self):
        """Initializations"""

        self.app = Flask(__name__)
        CORS(self.app, support_credentials=True)
        self.configure_app()
        self.mysql = MySQL(self.app)
        self.create_api_routes()
        self.create_page_routes()
    
    def configure_app(self):
        """Configure Flask app with MySQL settings."""
        self.app.config['SECRET_KEY'] = os.getenv('SESSION_SECRET') 
        self.app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST')
        self.app.config['MYSQL_USER'] = os.getenv('MYSQL_USER')
        self.app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD')
        self.app.config['MYSQL_DB'] = os.getenv('MYSQL_DB')
        #self.app.config['MYSQL_PORT'] = int(os.getenv('MYSQL_PORT')) 

    def connect_db(self):
        """Create a MySQL database connection."""

        return Mysqldb.connect(
            host=self.app.config['MYSQL_HOST'],
            user=self.app.config['MYSQL_USER'],
            password=self.app.config['MYSQL_PASSWORD'],
            db=self.app.config['MYSQL_DB'],
            #port=self.app.config['MYSQL_PORT'] 
        )
    
    def create_page_routes(self):
        @self.app.route('/')
        def home():
            try:
                #return render_template('datetime_reservation.html')
                return redirect('/login')
            except Exception as e:
                return f"Error: {e}", 500
        
        @self.app.route('/login')
        def patient_login():
            if not util.no_user_logged_in(): # proceeds to home if logged in
                return redirect('/home')
            try:
                return render_template('login.html')
            except Exception as e:
                return f"Error: {e}", 500
            
        @self.app.route('/register')
        def patient_register():
            if not util.no_user_logged_in(): # proceeds to home if logged in
                return redirect('/home')
            try:
                return render_template('register.html')
            except Exception as e:
                return f"Error: {e}", 500
           
        @self.app.route('/home')
        def patient_home():
            if util.no_user_logged_in(): #proceeds to login page if not logged in
                return redirect('/login')
            try:
                return render_template('main.html')
            except Exception as e:
                return f"Error: {e}", 500
            
        @self.app.route('/schedule')
        def schedule_home():
            if util.no_user_logged_in(): #proceeds to schedule page if not logged in
                return redirect('/home')
            try:
                return render_template('schedule.html')
            except Exception as e:
                return f"Error: {e}", 500
        
        @self.app.route('/staff/schedules')
        def staff_schedules():
            if util.no_user_logged_in(): #proceeds to schedule page if not logged in
                return redirect('/home')
            try:
                return render_template('dummy_all_appointments.html')
            except Exception as e:
                return f"Error: {e}", 500

    def create_api_routes(self):
        patient_routes(self, 'tblpatient')
        appointment_routes(self, 'tblappointment')
        diagnosis_routes(self, 'tbldiagnosis')
        sms_routes(self, 'tblsmsnotif')

    def run(self):
        """Run the Flask application."""
        self.app.run(debug=True)

if __name__ == '__main__':
    app_instance = App()
    app_instance.run()