from flask import Blueprint, request, jsonify, render_template
from services.chatbot_service import get_chatbot_response

chatbot_bp = Blueprint("chatbot", __name__)

@chatbot_bp.route("/")
def home():
    return render_template("index.html")

@chatbot_bp.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message", "")
    response = get_chatbot_response(user_message)
    return jsonify({"reply": response})
