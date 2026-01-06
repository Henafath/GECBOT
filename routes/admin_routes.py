from flask import Blueprint, jsonify, request
from services.db_service import get_db
from ml.train_model import train

admin_bp = Blueprint("admin_bp", __name__)

# View unanswered questions
@admin_bp.route("/admin/unanswered", methods=["GET"])
def get_unanswered():
    db = get_db()
    data = list(db.unanswered_queries.find({"trained": False}, {"_id": 0}))
    return jsonify(data)

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
