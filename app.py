from flask import Flask, render_template
from routes.chatbot_routes import chatbot_bp
from routes.department_routes import department_bp
from routes.faculty_routes import faculty_bp


def create_app():
    app = Flask(__name__)
    app.register_blueprint(chatbot_bp) 
    app.register_blueprint(department_bp)
    app.register_blueprint(faculty_bp) # Register chatbot routes
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
