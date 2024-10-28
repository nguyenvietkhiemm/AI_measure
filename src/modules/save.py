import joblib
import pickle

def save_model(models, path):
    with open(path, "wb") as file:
        pickle.dump(models, file)

def load_model(path):
    with open(path, "rb") as file:
        loaded_model = pickle.load(file)
    return loaded_model
