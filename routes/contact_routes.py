from flask import Blueprint, jsonify
from services.db_service import get_db

contact_bp = Blueprint('contact_bp', __name__)
db = get_db()

@contact_bp.route("/", methods=["GET"])
def get_contact():
    contact = db.contacts.find_one({}, {"_id": 0})
    if not contact:
        return jsonify({"error": "Contact info not found"}), 404
    return jsonify(contact)
