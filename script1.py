import pickle
with open("ml/model.pkl", "wb") as f:
    pickle.dump((model, vectorizer), f)