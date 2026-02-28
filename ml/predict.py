import pickle
import os
os.environ["JOBLIB_MULTIPROCESSING"] = "0"


# Load model once when module loads
with open("ml/model.pkl", "rb") as f:
    model, vectorizer = pickle.load(f)

def predict_answer(text):
    X = vectorizer.transform([text])
    pred = model.predict_proba(X)

    if max(pred[0]) < 0.6:
        return None

    return model.classes_[pred.argmax()]
