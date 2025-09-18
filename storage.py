# space_pong/storage.py
import os, json

DEFAULT_SCORES = [
    {"name": "SPACE ACE", "score": 10},
    {"name": "COSMIC PLAYER", "score": 8},
    {"name": "STAR WARRIOR", "score": 6},
    {"name": "GALAXY HERO", "score": 4},
    {"name": "NEBULA NOVICE", "score": 2},
]

SCORES_FILE = "high_scores.json"  # or os.path.join("data","high_scores.json")

def load_high_scores():
    try:
        if os.path.exists(SCORES_FILE):
            with open(SCORES_FILE, "r") as f:
                return json.load(f)
    except:
        pass
    return DEFAULT_SCORES.copy()

def save_high_scores(high_scores):
    try:
        with open(SCORES_FILE, "w") as f:
            json.dump(high_scores, f)
    except:
        pass
