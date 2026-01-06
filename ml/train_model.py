import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from services.db_service import get_db

db = get_db()

def train():
    data = list(db.unanswered_queries.find({"trained": True}))

    X = [d["question"] for d in data]
    y = [d["answer"] for d in data]

    if not X:
        return

    vectorizer = TfidfVectorizer()
    X_vec = vectorizer.fit_transform(X)

    model = LogisticRegression()
    model.fit(X_vec, y)

    with open("ml/model.pkl", "wb") as f:
        pickle.dump((model, vectorizer), f)
