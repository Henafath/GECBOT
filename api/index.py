from flask import jsonify, request
from app import create_app
import requests
from routes.department_routes import fetch_ug_programs, fetch_pg_programs, fetch_departments, get_department, compare_departments,get_hod, get_program_intake
from routes.faculty_routes import df_get_all_faculties, df_get_faculty_contacts, df_get_faculty_by_department
from routes.placement_routes import df_get_all_placements, df_get_placements_by_year
from routes.contact_routes import df_get_contact
from services.db_service import get_db
from datetime import datetime, timezone

app = create_app()
API_KEY = "e54b7136c2d2c3c363d163842859fe35"
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
        result= fetch_departments()
        return result
    elif intent == "GetDepartmentInfoIntent":
        return get_department(req)

    elif intent == "GetAllFacultiesIntent":
        return df_get_all_faculties()

    elif intent == "GetFacultyContactsIntent":
        return df_get_faculty_contacts(req)

    elif intent == "GetFacultyByDepartmentIntent":
        return df_get_faculty_by_department(req)

    elif intent == "GetAllPlacementsIntent":
        return df_get_all_placements()

    elif intent == "GetPlacementsByYearIntent":
        return df_get_placements_by_year(req)

    elif intent=="CompareDepartmentsIntent":
        return compare_departments(req)
    
    elif intent == "GetHODIntent":
        return get_hod(req)
    
    elif intent == "GetProgramIntakeIntent":
        return get_program_intake(req)
    
    elif intent == "WeatherIntent":
        city = req["queryResult"]["parameters"].get("geo-city")

        if not city:
            city = "Kerala"

        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        res = requests.get(url).json()

        if res.get("main"):
            temp = res["main"]["temp"]
            desc = res["weather"][0]["description"]

            response_text = f"The temperature in {city} is {temp}°C with {desc}."
        else:
            response_text = "Sorry, I couldn't fetch the weather."

        return jsonify({"fulfillmentText": response_text})

    elif intent == "Default Fallback Intent":

     user_query = req["queryResult"]["queryText"]

     db = get_db()

    # 🔹 Step 1: Check if already answered in DB
     existing = db.unanswered_queries.find_one({
        "question": {"$regex": f"^{user_query}$", "$options": "i"},
        "answer": {"$ne": None}
     })

     if existing:
        return jsonify({"fulfillmentText": existing["answer"]})

    # 🔹 Step 2: Try ML prediction
     from ml.predict import predict_answer
     answer = predict_answer(user_query)

     if answer:
        return jsonify({"fulfillmentText": answer})

    # 🔹 Step 3: Save as new unanswered query (avoid duplicates)
     already_exists = db.unanswered_queries.find_one({
        "question": {"$regex": f"^{user_query}$", "$options": "i"}
     })

     if not already_exists:
        db.unanswered_queries.insert_one({
            "question": user_query,
            "answer": None,
            "trained": False,
            "created_at": datetime.now(timezone.utc)
        })

    # 🔹 Step 4: Default response
     return jsonify({
        "fulfillmentText": "I will learn this soon. Our team will update me."
     })

    return jsonify({"fulfillmentText": "Sorry, I didn't understand that."})


