import pickle
import json


def save_pickle(fname, obj):
    with open(fname, "wb") as f:
        pickle.dump(obj, f)


def load_pickle(fname):
    with open(fname, "rb") as f:
        return pickle.load(f)


def save_json(fname, obj):
    with open(fname, "w") as f:
        json.dump(obj, f)


def load_json(fname):
    with open(fname, "r") as f:
        return json.load(f)
