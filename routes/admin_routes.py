from bson import ObjectId
from flask import Blueprint, jsonify, render_template, request, redirect, session
from services.db_service import get_db
from ml.train_model import train
import os
from flask import url_for
import datetime

admin_bp = Blueprint("admin_bp", __name__)
db=get_db()


ADMIN_USER = os.getenv("ADMIN_USER")
ADMIN_PASS = os.getenv("ADMIN_PASS")
# Login page
@admin_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username == ADMIN_USER and password == ADMIN_PASS:
            session["admin"] = True
            return redirect(url_for("admin_bp.dashboard"))

        return render_template("login.html", error="Invalid credentials")

   
    return render_template("login.html")

@admin_bp.route("/submit_answer", methods=["POST"])
def submit_answer():
    if not session.get("admin"):
        return redirect(url_for("admin_bp.login"))
    db = get_db()

    question_id = request.form.get("id")
    answer = request.form.get("answer")

    if not answer:
        return "Answer cannot be empty"

    db.unanswered_queries.update_one(
        {"_id": ObjectId(question_id)},
        {
            "$set": {
                "answer": answer,
                "trained": True
            }
        }
    )
    train()
    

    return redirect(url_for("admin_bp.all_questions"))
@admin_bp.route("/answer_question/<id>")
def answer_question(id):
        if not session.get("admin"):
         return redirect(url_for("admin_bp.login"))
        db = get_db()

        data = db.unanswered_queries.find_one({"_id": ObjectId(id)})

        if not data:
            return "Question not found"

        return render_template(
            "answer.html",
            id=str(data["_id"]),
            question=data["question"]
        )

@admin_bp.route("/dashboard")
def dashboard():
    if not session.get("admin"):
        return redirect(url_for("admin_bp.login"))
    total_questions = db.unanswered_queries.count_documents({})
    answered = db.unanswered_queries.count_documents({"trained": True})
    unanswered = db.unanswered_queries.count_documents({"trained": False})

    questions = list(
        db.unanswered_queries.find({"trained": False}).sort("created_at", -1).limit(10)
    )

    return render_template(
        "dashboard.html",
        total=total_questions,
        answered=answered,
        unanswered=unanswered,
        questions=questions
    )
# Logout
@admin_bp.route("/logout")
def logout():
    session.pop("admin", None)
    return redirect("/login")
#@admin_bp.route("/admin")
#def admin_home():
 #   if not session.get("admin"):
  #      return redirect("/login")

   # data = list(db.unanswered_queries.find({"trained": False}))
    #return render_template("admin.html", queries=data)

@admin_bp.route("/questions")
def all_questions():
    if not session.get("admin"):
        return redirect(url_for("admin_bp.login"))

    questions = list(
        db.unanswered_queries.find().sort("created_at", -1)
    )

    return render_template("all_questions.html", questions=questions)
# Save admin answers
@admin_bp.route("/admin/answer", methods=["POST"])
def save_answer():
    if not session.get("admin"):
        return redirect(url_for("admin_bp.login"))
    db = get_db()
    payload = request.get_json()

    db.unanswered_queries.update_one(
        {"question": payload["question"]},
        {"$set": {"answer": payload["answer"], "trained": True}}
    )

    return jsonify({"message": "Answer saved"})

# Retrain ML model
@admin_bp.route("/admin/train", methods=["POST"])
def retrain_model():
    if not session.get("admin"):
        return redirect(url_for("admin_bp.login"))
    train()
    return jsonify({"message": "Model retrained successfully"})

@admin_bp.route("/analytics")
def analytics():
    if not session.get("admin"):
        return redirect(url_for("admin_bp.login"))

    total = db.unanswered_queries.count_documents({})
    answered = db.unanswered_queries.count_documents({"trained": True})
    unanswered = db.unanswered_queries.count_documents({"trained": False})

    # Example analytics: questions per day
    pipeline = [
        {
            "$group": {
                "_id": {
                    "year": {"$year": "$created_at"},
                    "month": {"$month": "$created_at"},
                    "day": {"$dayOfMonth": "$created_at"}
                },
                "count": {"$sum": 1}
            }
        },
    {
        "$sort": {
            "_id.year": 1,
            "_id.month": 1,
            "_id.day": 1
        }
    }
    ]

    daily_stats = list(db.unanswered_queries.aggregate(pipeline))

    return render_template(
        "analytics.html",
        total=total,
        answered=answered,
        unanswered=unanswered,
        daily_stats=daily_stats
    )

# Department Program (UG/PG)
@admin_bp.route("/add_department_program", methods=["POST"])
def add_department_program():
    if not session.get("admin"):
        return redirect(url_for("admin_bp.login"))
    db = get_db()

    dept = request.form.get("department")
    level = request.form.get("program_level")
    course = request.form.get("course")
    intake = int(request.form.get("intake") or 0)

    program = {"course": course, "intake": intake}

    key = "ug programs" if level == "ug" else "pg programs"

    db.departments.update_one(
        {"branch": {"$regex": dept, "$options": "i"}},
        {"$addToSet": {key: program}}  # avoids duplicates
    )

    return render_template("add_info.html", message="Program added successfully")


# Faculty
@admin_bp.route("/add_faculty", methods=["POST"])
def add_faculty():
    if not session.get("admin"):
        return redirect(url_for("admin_bp.login"))
    db = get_db()

    db.faculty.insert_one({
        "Name": request.form.get("faculty_name"),
        "Department": request.form.get("department"),
        "Designation": request.form.get("designation"),
        "Qualification": request.form.get("qualification"),
        "Specialisation": request.form.get("specialisation"),
        "Email": request.form.get("email"),
        "PhoneNumber": request.form.get("phone"),
        "Experience": request.form.get("experience"),
        "Publications": int(request.form.get("publications") or 0),
        "Projects": int(request.form.get("projects") or 0)
    })

    return render_template("add_info.html", message="Faculty added successfully")


# Placement
@admin_bp.route("/add_placement", methods=["POST"])
def add_placement():
    if not session.get("admin"):
        return redirect(url_for("admin_bp.login"))
    db = get_db()

    companies = request.form.get("companies", "")
    db.placements.insert_one({
        "year": int(request.form.get("year")),
        "companies": [c.strip() for c in companies.split(",") if c.strip()],
        "created_at": datetime.utcnow()
    })

    return render_template("add_info.html", message="Placement added successfully")

@admin_bp.route("/add_info")
def add_info():
    if not session.get("admin"):
        return redirect(url_for("admin_bp.login"))
    return render_template("add_info.html")