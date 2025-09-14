from services.db_service import get_ug_programs, get_pg_programs, get_placements, get_faculty_contacts

def get_chatbot_response(user_message: str) -> str:
    user_message = user_message.lower()

    if "ug" in user_message:
        programs = get_ug_programs()
        return "UG Programs:\n" + "\n".join([f"{p['course']} (Intake: {p['intake']}, Vacant: {p['vacant']}, Last Rank: {p['last_rank']})" for p in programs])

    elif "pg" in user_message:
        programs = get_pg_programs()
        return "PG Programs:\n" + "\n".join([f"{p['course']} (Intake: {p['intake']}, Vacant: {p['vacant']}, Last Rank: {p['last_rank']})" for p in programs])

    elif "placement" in user_message:
        placements = get_placements()
        return "Placement Records:\n" + "\n".join([f"{p['year']} - {p['company']} - {p['students_selected']} students, Highest: {p['highest_package']}, Avg: {p['average_package']}" for p in placements])

    elif "contact" in user_message or "email" in user_message:
        contact = get_faculty_contacts()
        return f"Email: {contact['email']}, Phone: {contact['phone']}"

    else:
        return "Sorry, I don’t have that info yet."
