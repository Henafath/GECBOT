from flask import Blueprint, jsonify, render_template, request, redirect, session
from services.db_service import get_db
from ml.train_model import train
import os
from flask import url_for

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