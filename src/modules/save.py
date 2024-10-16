import joblib

def save_model(model, path):
    joblib.dump(model, path)

def load_model(path):
    loaded_model = joblib.load(path)
    return loaded_model
