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


# ============================
# DIALOGFLOW HANDLER
# ============================

def df_get_contact():
    try:
        contact = db.contacts.find_one({}, {"_id": 0})

        if not contact:
            return jsonify({
                "fulfillmentText": "Contact information is currently unavailable."
            })

        text = (
            f"Contact Information for GEC Thrissur:\n"
            f"Phone: {contact.get('phone')}\n"
            f"Email: {contact.get('email')}\n"
            f"Address: {contact.get('address')}"
        )

        return jsonify({"fulfillmentText": text})

    except Exception:
        return jsonify({"fulfillmentText": "Unable to fetch contact details."})