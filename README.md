# GECBOT

An intelligent chatbot for Government Engineering College Thrissur (GECT) that provides details such as departments, programs, faculty, vacant seats, last rank details, placements, and contact information.
Built using Python Flask + MongoDB and designed for integration into the official GECT website.

🚀 Features

Interactive chatbot interface (appears as “May I help you?” on the website).

Provides details on:

UG/PG Programs with intake, vacancies, and last rank.

Department and faculty information.

Placement statistics (year-wise).

Contact details.

Data dynamically fetched from MongoDB database.

Easily extendable with new modules and APIs.

🛠️ Tech Stack

Backend: Flask (Python)

Database: MongoDB

Frontend: HTML, CSS, JavaScript (basic chatbot UI)

Other Tools: PyMongo (MongoDB driver), JSON for initial data

📂 Project Structure
gect_chatbot/
│── app.py                  # Main Flask entry point
│── config.py               # Configurations (DB URI, settings)
│── routes/
│    └── chatbot_routes.py  # Chatbot routes (API + UI)
│── services/
│    ├── chatbot_service.py # Chatbot response logic
│    └── db_service.py      # MongoDB query helpers
│── data/
│    ├── departments.json   # Department data
│    ├── faculty.json       # Faculty data
│    └── seed_data.py       # Script to insert JSON into MongoDB
│── templates/
│    └── index.html         # Frontend chatbot UI
│── static/
│    └── style.css          # Styling (optional)
│── README.md               # Project documentation

