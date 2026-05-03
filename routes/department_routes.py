from flask import Blueprint, jsonify, request
from services.db_service import get_ug_programs, get_pg_programs, get_db
import random
department_bp = Blueprint("department_bp", __name__)

# ✅ Get all UG Programs
def fetch_ug_programs():
    try:
        programs = get_ug_programs()

        if not programs:
            return jsonify({"fulfillmentText": "No UG programs found."})
        formatted_programs = "  ".join([f"• {p['course']} (Intake: {p['intake']})" for p in programs])
       
        responses = [
    "Here are the PG programs available:",
    "You can explore the following postgraduate courses:",
    "These are the M.Tech programs offered:"
]
        intro = random.choice(responses)
        result= jsonify({
    "fulfillmentText": f"{intro}         {formatted_programs}.Let me know if you need details about any specific course!"
})
        return result

    except Exception:
        return jsonify({
    "fulfillmentText": "Hmm, I’m not completely sure about that yet 🤔. But I’ll learn it soon! Meanwhile, you can try asking about courses, faculty, or placements."
})

# ✅ Get all PG Programs
def fetch_pg_programs():
    try:
        programs = get_pg_programs()

        if not programs:
            return jsonify({"fulfillmentText": "No PG programs found."})
        formatted_programs = "  ".join([f"• {p['course']} (Intake: {p['intake']})" for p in programs])
        responses = [
    "Here are the PG programs available:",
    "You can explore the following postgraduate courses:",
    "These are the M.Tech programs offered:"
]
        intro = random.choice(responses)
        result= jsonify({
    "fulfillmentText": f"{intro}  {formatted_programs}.  Let me know if you need details about any specific course!"
})
        return result

    except Exception:
        return jsonify({
    "fulfillmentText": "Hmm, I’m not completely sure about that yet 🤔. But I’ll learn it soon! Meanwhile, you can try asking about courses, faculty, or placements."
})


# ✅ Get all Departments (with UG + PG Programs)
import random

def fetch_departments():
    try:
        db = get_db()
        departments = list(db.departments.find({}, {"_id": 0}))

        if not departments:
            return jsonify({
                "fulfillmentText": "No departments found."
            }), 200

        # Random intro
        responses = [
            "Here are all the departments available at GEC Thrissur:",
            "The following departments are available:",
            "These are the departments in GEC Thrissur:"
        ]

        intro = random.choice(responses)
        print(intro)
        # Extract department names
        dept_names = [d.get("branch") for d in departments if d.get("branch")]

        # Format list nicely
        formatted_departments = "\n".join([f"• {name}" for name in dept_names])
        print(formatted_departments)
        # Count
        count = len(dept_names)

        # Suggestion chips (Dialogflow quick replies)
        suggestions = [
            {"title": "UG Programs"},
            {"title": "PG Programs"},
            {"title": "Faculty Details"},
            {"title": "Placements"}
        ]

         return jsonify({
            "fulfillmentText": f"{intro}\n\n{formatted_departments}\n\nTotal Departments: {count}\n\nYou can ask about any department for more details."
        })

    except Exception as e:
        print(e)
        return jsonify({
            "fulfillmentText": "Unable to fetch departments."
        }), 500

# Get department info
def get_department(req):
    try:
        db = get_db()
        params = req["queryResult"]["parameters"]
        name = params.get("department")

        if not name:
            return jsonify({"fulfillmentText": "Please specify the department name."})
        
        department = db.departments.find_one(
         {"branch": name},
         {"_id": 0})
        
            
        if not department:
            return jsonify({"fulfillmentText": "Department not found."})
        
        formatted_ugprograms = "  ".join([f"• {p['course']} (Intake: {p['intake']})" for p in department.get("ug programs", [])])
        formatted_pgprograms = "  ".join([f"• {p['course']} (Intake: {p['intake']})" for p in department.get("pg programs", [])])

        text = (
            f"Department: {department.get('branch')}\n"
            f"HOD: {department.get('hod')}\n"
            f"UG Programs: {', '.join(formatted_ugprograms)}\n"
            f"PG Programs: {', '.join(formatted_pgprograms)}\n"
            f"Contact: {department.get('email')}"
        )

        return jsonify({"fulfillmentText": text})

    except Exception:
        return jsonify({"fulfillmentText": "Unable to fetch department details."})

