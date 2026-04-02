from flask import jsonify, request
from app import create_app
from routes.department_routes import fetch_ug_programs, fetch_pg_programs, fetch_departments, get_department
from routes.faculty_routes import df_get_all_faculties, df_get_faculty_contacts, df_get_faculty_by_department
from routes.placement_routes import df_get_all_placements, df_get_placements_by_year
from routes.contact_routes import df_get_contact
from services.db_service import get_db
from datetime import datetime, timezone

app = create_app()

@app.route('/api/webhook', methods=['POST'])
def webhook():
    print("STEP 1: Webhook received")
    req = request.get_json()
    intent = req['queryResult']['intent']['displayName']
    print("STEP 2: Intent detected =", intent)
    if intent == "GetUGProgramsIntent":
        return fetch_ug_programs()

    elif intent == "GetPGProgramsIntent":
        return fetch_pg_programs()
        
    elif intent == "GetAllDepartmentsIntent":
        print("STEP 3: Enter depts intent")
        result= fetch_departments()
        print("STEP 4: dept data fetched")
        return result
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


    elif intent == "Default Fallback Intent":
       
       from ml.predict import predict_answer
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

    return jsonify({"fulfillmentText": "Sorry, I didn't understand that."})


