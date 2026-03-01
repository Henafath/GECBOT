from flask import Flask
from routes.chatbot_routes import chatbot_bp
from routes.department_routes import department_bp
from routes.faculty_routes import faculty_bp
from routes.placement_routes import placement_bp
from routes.admin_routes import admin_bp
from flask_cors import CORS
from dotenv import load_dotenv
import os

load_dotenv()


def create_app():
    app = Flask(__name__)
    app.secret_key = "CTdgxUYFrdf276GFVa"
    CORS(app)
    
    app.register_blueprint(admin_bp)
    app.register_blueprint(chatbot_bp) 
    app.register_blueprint(department_bp,url_prefix="/api")
    app.register_blueprint(faculty_bp,url_prefix="/api")
    app.register_blueprint(placement_bp)

# Register chatbot routes
    return app

if __name__ == "__main__":
    app = create_app()
    
    app.run(debug=True)
    
