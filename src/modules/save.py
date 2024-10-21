import joblib

def save_model(models, path):
    joblib.dump(models, path)

def load_model(path):
    loaded_model = joblib.load(path)
    return loaded_model
