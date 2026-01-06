import pickle

def predict_answer(text):
    with open("ml/model.pkl", "rb") as f:
        model, vectorizer = pickle.load(f)

    X = vectorizer.transform([text])
    pred = model.predict_proba(X)

    if max(pred[0]) < 0.6:
        return None

    return model.classes_[pred.argmax()]
