from dotenv import load_dotenv
import os
import MySQLdb as Mysqldb
from flask import Flask, render_template
from flask_mysqldb import MySQL
from api.patient import patient_routes
from api.appointments import appointment_routes
from flask_cors import CORS
# Load environment variables from .env file
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

        self.app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST')
        self.app.config['MYSQL_USER'] = os.getenv('MYSQL_USER')
        self.app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD')
        self.app.config['MYSQL_DB'] = os.getenv('MYSQL_DB')
        self.app.config['MYSQL_PORT'] = int(os.getenv('MYSQL_PORT')) 

    def connect_db(self):
        """Create a MySQL database connection."""

        return Mysqldb.connect(
            host=self.app.config['MYSQL_HOST'],
            user=self.app.config['MYSQL_USER'],
            password=self.app.config['MYSQL_PASSWORD'],
            db=self.app.config['MYSQL_DB'],
            port=self.app.config['MYSQL_PORT'] 
        )
    
    def create_page_routes(self):
        @self.app.route('/')
        def home():
            # Here you would fetch any necessary data from the database to render the page
            try:
                return render_template('datetime_reservation.html')
            except Exception as e:
                return f"Error: {e}", 500
<<<<<<< Updated upstream
=======
        
        @self.app.route('/login')
        def patient_login():
            # Here you would fetch any necessary data from the database to render the page
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
                return render_template('main.html')
            except Exception as e:
                return f"Error: {e}", 500
        
        @self.app.route('/home')
        def patient_home():
            if util.no_user_logged_in(): #proceeds to login page if not logged in
                return redirect('/login')
            try:
                return render_template('PLACEHOLDER_home.html')
            except Exception as e:
                return f"Error: {e}", 500
>>>>>>> Stashed changes

    def create_api_routes(self):
        patient_routes(self)
        appointment_routes(self)

    def run(self):
        """Run the Flask application."""
        self.app.run(debug=True)


if __name__ == '__main__':
    app_instance = App()
    app_instance.run()