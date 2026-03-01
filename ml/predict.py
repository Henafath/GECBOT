from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from services.db_service import get_db

def predict_answer(text):
    db = get_db()

    # Fetch only trained Q&A pairs
    data = list(db.unanswered_queries.find({"trained": True}))

    if not data:
        return None

    questions = [item["question"] for item in data]
    answers = [item["answer"] for item in data]

    # Train model in memory
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(questions)

    model = LogisticRegression()
    model.fit(X, answers)

    # Predict
    X_test = vectorizer.transform([text])
    prob = model.predict_proba(X_test)

    if max(prob[0]) < 0.6:
        return None

    return model.classes_[prob.argmax()]