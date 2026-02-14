from flask import Blueprint, jsonify, render_template, request, redirect, session
from services.db_service import get_db
from ml.train_model import train
import os

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
            return redirect("/admin")

        return "Invalid credentials"

    return render_template("login.html")

# Logout
@admin_bp.route("/logout")
def logout():
    session.pop("admin", None)
    return redirect("/login")
@admin_bp.route("/admin")
def admin_home():
    if not session.get("admin"):
        return redirect("/login")

    data = list(db.unanswered_queries.find({"trained": False}))
    return render_template("admin.html", queries=data)


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
