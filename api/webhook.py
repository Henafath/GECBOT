from flask import jsonify, request

from routes.department_routes import fetch_ug_programs, fetch_pg_programs
from routes.department_routes import fetch_departments, get_department
from routes.faculty_routes import df_get_all_faculties, df_get_faculty_contacts, df_get_faculty_by_department
from routes.placement_routes import df_get_all_placements, df_get_placements_by_year
from routes.contact_routes import df_get_contact
from ml.predict import predict_answer
from services.db_service import get_db

def handler(req):
    data = req.get_json()
    intent = data["queryResult"]["intent"]["displayName"]

    if intent == "GetUGProgramsIntent":
        return fetch_ug_programs()

    elif intent == "GetPGProgramsIntent":
        return fetch_pg_programs()

    elif intent == "GetAllDepartmentsIntent":
        return fetch_departments()

    elif intent == "GetDepartmentInfoIntent":
        return get_department(data)

    elif intent == "GetAllFacultiesIntent":
        return df_get_all_faculties()

    elif intent == "GetFacultyContactsIntent":
        return df_get_faculty_contacts()

    elif intent == "GetFacultyByDepartmentIntent":
        return df_get_faculty_by_department(data)

    elif intent == "GetAllPlacementsIntent":
        return df_get_all_placements()

    elif intent == "GetPlacementsByYearIntent":
        return df_get_placements_by_year(data)

    elif intent == "GetContactIntent":
        return df_get_contact()

    elif intent == "Default Fallback Intent":
        answer = predict_answer(data["queryResult"]["queryText"])
        if answer:
            return jsonify({"fulfillmentText": answer})

        db = get_db()
        db.unanswered_queries.insert_one({
            "question": data["queryResult"]["queryText"],
            "answer": None,
            "trained": False
        })
        return jsonify({"fulfillmentText": "I will learn this soon."})

    return jsonify({"fulfillmentText": "Sorry, I couldn't understand your request."})
