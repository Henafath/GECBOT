from flask import Blueprint, jsonify, request
from services.db_service import get_ug_programs, get_pg_programs, get_db
import random
import re
department_bp = Blueprint("department_bp", __name__)

# ✅ Get all UG Programs
def fetch_ug_programs():
    try:
        programs = get_ug_programs()

        if not programs:
            return jsonify({"fulfillmentText": "No UG programs found."})
        formatted_programs = "  ".join([f"• {p['course']} (Intake: {p['intake']})" for p in programs])
       
        responses = [
    "Here are the UG programs available:",
    "You can explore the following undergraduate courses:",
    "These are the B.Tech programs offered:"
]
        intro = random.choice(responses)
        result= jsonify({
    "fulfillmentText": f"{intro}         {formatted_programs}"
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
    "fulfillmentText": f"{intro}  {formatted_programs}."
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
            "fulfillmentText": f"{intro}\n\n{formatted_departments}\n\nTotal Departments: {count}.\n\nYou can ask about any department for more details."
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
            f"Department: {department.get('branch')},\n"
            f"HOD: {department.get('hod')},\n"
            f"UG Programs: {formatted_ugprograms}\n"
            f"PG Programs: {formatted_pgprograms},\n"
            f"Contact: {department.get('email')}"
        )

        return jsonify({"fulfillmentText": text})

    except Exception:
        return jsonify({"fulfillmentText": "Unable to fetch department details."})




def compare_departments(req):
    try:
        db = get_db()

        params = req["queryResult"]["parameters"]

        dept_list = params.get("departments", [])

        # Validate
        if len(dept_list) < 2:
            return jsonify({
                "fulfillmentText": "Please provide two departments to compare."
            })

        # Take first two
        dept1_name = dept_list[0]
        dept2_name = dept_list[1]

        dept1 = db.departments.find_one({
        "branch": {"$regex": f"^{re.escape(dept1_name)}", "$options": "i"}
        })
        dept2 = db.departments.find_one({
        "branch": {"$regex": f"^{re.escape(dept2_name)}", "$options": "i"}
        })

        if not dept1 or not dept2:
            return jsonify({
                "fulfillmentText": "I couldn't find one or both departments."
            })

        # Extract data
        ug1 = [p.get("course") for p in dept1.get("ug programs", [])]
        ug2 = [p.get("course") for p in dept2.get("ug programs", [])]

        pg1 = [p.get("course") for p in dept1.get("pg programs", [])]
        pg2 = [p.get("course") for p in dept2.get("pg programs", [])]

        # Format response
        text = (
            f"📊 Comparison between {dept1.get('branch')} and {dept2.get('branch')}:\n\n"

            f"🔹 {dept1.get('branch')}\n"
            f"HOD: {dept1.get('hod')}\n"
            f"UG: {', '.join(ug1) if ug1 else 'N/A'}\n"
            f"PG: {', '.join(pg1) if pg1 else 'N/A'}\n\n"

            f"🔹 {dept2.get('branch')}\n"
            f"HOD: {dept2.get('hod')}\n"
            f"UG: {', '.join(ug2) if ug2 else 'N/A'}\n"
            f"PG: {', '.join(pg2) if pg2 else 'N/A'}\n\n"

            f"You can ask more details about any department!"
        )

        return jsonify({"fulfillmentText": text})

    except Exception as e:
        print(e)
        return jsonify({
            "fulfillmentText": "Unable to compare departments right now."
        })
    
def get_hod(req):
    try:
        db = get_db()

        params = req["queryResult"]["parameters"]
        dept_name = params.get("department")

        if not dept_name:
            return jsonify({
                "fulfillmentText": "Please mention the department."
            })


        # Flexible search (case-insensitive)
        department = db.departments.find_one({
            "branch": {"$regex": dept_name, "$options": "i"}
        })

        if not department:
            return jsonify({
                "fulfillmentText": "I couldn't find that department."
            })

        hod = department.get("hod")

        if not hod:
            return jsonify({
                "fulfillmentText": f"HOD information for {department.get('branch')} is not available."
            })

        return jsonify({
            "fulfillmentText": f"The HOD of {department.get('branch')} is {hod}."
        })

    except Exception as e:
        print(e)
        return jsonify({
            "fulfillmentText": "Unable to fetch HOD details right now."
        })

def get_program_intake(req):
    try:
        db = get_db()
        params = req["queryResult"]["parameters"]

        dept_name = params.get("department")

        if not dept_name:
            return jsonify({
                "fulfillmentText": "Please specify the department."
            })


        # Fetch department
        department = db.departments.find_one({
            "branch": {"$regex": dept_name, "$options": "i"}
        })

        if not department:
            return jsonify({
                "fulfillmentText": "I couldn't find that department."
            })

        # UG Programs
        ug_programs = department.get("ug programs", [])
        ug_list = [
            f"• {p.get('course')} (Intake: {p.get('intake', 'N/A')})"
            for p in ug_programs if p.get("course")
        ]

        # PG Programs
        pg_programs = department.get("pg programs", [])
        pg_list = [
            f"• {p.get('course')} (Intake: {p.get('intake', 'N/A')})"
            for p in pg_programs if p.get("course")
        ]

        text = f"📊 Intake details for {department.get('branch')}:\n\n"

        if ug_list:
            text += "🎓 UG Programs:\n" + "\n".join(ug_list) + "\n\n"
        else:
            text += "🎓 UG Programs: Not available\n\n"

        if pg_list:
            text += "🎓 PG Programs:\n" + "\n".join(pg_list)
        else:
            text += "🎓 PG Programs: Not available"

        return jsonify({"fulfillmentText": text})

    except Exception as e:
        print(e)
        return jsonify({
            "fulfillmentText": "Unable to fetch intake details right now."
        })
