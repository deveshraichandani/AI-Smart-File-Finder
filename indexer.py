import pickle

def save_index(data, path="index.pkl"):
    with open(path, "wb") as f:
        pickle.dump(data, f)

def load_index(path="index.pkl"):
    with open(path, "rb") as f:
        return pickle.load(f)