import os
import pickle

model = None
vectorizer = None

def load_model():
    global model, vectorizer

    if model is None:
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        MODEL_PATH = os.path.join(BASE_DIR, "model.pkl")

        with open(MODEL_PATH, "rb") as f:
            model, vectorizer = pickle.load(f)

def predict_answer(text):
    load_model()

    X = vectorizer.transform([text])
    pred = model.predict_proba(X)

    if max(pred[0]) < 0.6:
        return None

    return model.classes_[pred.argmax()]