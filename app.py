from flask import Flask, render_template
from routes.chatbot_routes import chatbot_bp
from routes.department_routes import department_bp
from routes.faculty_routes import faculty_bp
from routes.placement_routes import placement_bp
from flask_cors import CORS


def create_app():
    app = Flask(__name__)
    CORS(app)
    app.register_blueprint(chatbot_bp) 
    app.register_blueprint(department_bp,url_prefix="/api")
    app.register_blueprint(faculty_bp,url_prefix="/api")
    app.register_blueprint(placement_bp)
# Register chatbot routes
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
