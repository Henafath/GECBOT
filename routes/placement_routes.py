from flask import Blueprint, jsonify, request
from services.db_service import get_placements

placement_bp = Blueprint("placement_bp", __name__)

#Route 1: Get all placement data

@placement_bp.route("/api/placements", methods=["GET"])
def get_all_placements():
  try:
     data = get_placements()
     return jsonify(data), 200
  except Exception as e:
     return jsonify({"error": str(e)}), 500

#Route 2: Get placement data by year (example:/api/placements/2024)

@placement_bp.route("/api/placements/<int-year>", methods=["GET"])
def get_placements_by_year(year):
   try:
     data = get_placements(year)
     if data:
      return jsonify(data), 200
     else:
         return jsonify({"message": f"No placement data found for {year}"}), 404 
   except Exception as e: return jsonify({"error": str(e)}), 500
# ============================
# DIALOGFLOW HANDLERS
# ============================

def df_get_all_placements():
    try:
        data = get_placements()

        if not data:
            return jsonify({"fulfillmentText": "No placement data available."})

        text = "Placement Statistics at GEC Thrissur:\n"
        for p in data:
            text += f"- {p.get('company')} | {p.get('year')} | {p.get('package')} LPA\n"

        return jsonify({"fulfillmentText": text})

    except Exception:
        return jsonify({"fulfillmentText": "Unable to fetch placement details."})


def df_get_placements_by_year(req):
    try:
        params = req["queryResult"]["parameters"]
        year = params.get("year")

        if not year:
            return jsonify({"fulfillmentText": "Please specify the placement year."})

        data = get_placements(int(year))

        if not data:
            return jsonify({"fulfillmentText": f"No placement data found for {year}."})

        text = f"Placement details for {year}:\n"
        for p in data:
            text += f"- {p.get('company')} | {p.get('package')} LPA\n"

        return jsonify({"fulfillmentText": text})

    except Exception:
        return jsonify({"fulfillmentText": "Unable to fetch placement details."})
