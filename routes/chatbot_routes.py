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

@chatbot_bp.route("/webhook", methods=["POST"])
def dialogflow_webhook():
    req = request.get_json()

    parameters = req.get("queryResult", {}).get("parameters", {})
    branch = parameters.get("branch")
    year = parameters.get("year")

    # Temporary logic (replace with DB/JSON later)
    if branch == "CSE" and year == "2023":
        reply = "The last rank for CSE in 2023 was 4230 (General category)."
    elif branch == "ECE" and year == "2023":
        reply = "The last rank for ECE in 2023 was 5610."
    else:
        reply = "Sorry, I don't have data for that branch or year yet."

    return jsonify({
        "fulfillmentText": reply
    })