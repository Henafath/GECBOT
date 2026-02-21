from flask import Flask, jsonify,request, render_template
from routes.chatbot_routes import chatbot_bp
from routes.department_routes import department_bp, fetch_ug_programs, fetch_pg_programs, fetch_departments, get_department
from routes.faculty_routes import faculty_bp, df_get_all_faculties, df_get_faculty_contacts, df_get_faculty_by_department
from routes.placement_routes import placement_bp, df_get_all_placements, df_get_placements_by_year
from routes.contact_routes import df_get_contact
from ml.predict import predict_answer
from routes.admin_routes import admin_bp
from ml.train_model import train
from datetime import datetime,timezone
from services.db_service import get_db
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

    @app.route('/webhook', methods=['POST'])
    def webhook():
        req = request.get_json()
        intent = req['queryResult']['intent']['displayName']
    
        if intent == "GetUGProgramsIntent":
          return fetch_ug_programs()

        elif intent == "GetPGProgramsIntent":
          return fetch_pg_programs()

        elif intent == "GetAllDepartmentsIntent":
          return fetch_departments()

        elif intent == "GetDepartmentInfoIntent":
          return get_department(req)
        
        elif intent == "GetAllFacultiesIntent":
          return df_get_all_faculties()

        elif intent == "GetFacultyContactsIntent":
           return df_get_faculty_contacts()

        elif intent == "GetFacultyByDepartmentIntent":
          return df_get_faculty_by_department(req)
        
        elif intent == "GetAllPlacementsIntent":
          return df_get_all_placements()

        elif intent == "GetPlacementsByYearIntent":
         return df_get_placements_by_year(req)

        elif intent == "GetContactIntent":
         return df_get_contact()
        
        elif intent == "Default Fallback Intent":
          answer = predict_answer(req["queryResult"]["queryText"])

          if answer:
           return jsonify({"fulfillmentText": answer})

          db = get_db()
          db.unanswered_queries.insert_one({
            "question": req["queryResult"]["queryText"],
           "answer": None,
            "trained": False,
            "created_at": datetime.now(timezone.utc)
            })

          return jsonify({"fulfillmentText": "I will learn this soon. Our team will update me."})

        else:
             return jsonify({"fulfillmentText": "Sorry, I didn't understand that."})

   
# Register chatbot routes
    return app

if __name__ == "__main__":
    app = create_app()
    
    app.run(debug=True)
    
