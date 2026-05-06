import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from services.db_service import get_db

db = get_db()

def train():
   try:
    data = list(db.unanswered_queries.find({"trained": True}))

    X = [d["question"] for d in data]
    y = [d["answer"] for d in data]
    print("Fetched records:", len(data))
    if not X:
        return

    vectorizer = TfidfVectorizer()
    X_vec = vectorizer.fit_transform(X)

    model = LogisticRegression()
    model.fit(X_vec, y)

    with open("ml/model.pkl", "wb") as f:
        pickle.dump((model, vectorizer), f)

    
    print("Model trained successfully!")
   except Exception as e:
        print("Error:", e)
if __name__ == "__main__":
    train()
