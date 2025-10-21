import os
from datetime import datetime
import json

HISTORY_FILE = "generation_history.json"

def save_images(images, folder=None):
    if folder is None:
        folder = os.path.join("generated_images", datetime.now().strftime("%Y%m%d_%H%M%S"))
    os.makedirs(folder, exist_ok=True)
    paths = []
    for img in images:
        filename = datetime.now().strftime("%Y%m%d_%H%M%S_%f") + ".png"
        path = os.path.join(folder, filename)
        img.save(path)
        paths.append(path)
    return paths

def load_gallery(limit=12):
    base_dir = "generated_images"
    files = []
    if os.path.exists(base_dir):
        files = sorted(
            [os.path.join(base_dir, f) for f in os.listdir(base_dir) if f.endswith(".png")],
            key=os.path.getmtime,
            reverse=True
        )
    return files[:limit]

# --- 1日5枚制限用 ---
def get_today_count():
    today = datetime.now().strftime("%Y-%m-%d")
    try:
        with open(HISTORY_FILE, "r") as f:
            history = json.load(f)
    except FileNotFoundError:
        return 0

    return sum(1 for h in history if h["date"] == today)

def add_today_count(num):
    today = datetime.now().strftime("%Y-%m-%d")
    try:
        with open(HISTORY_FILE, "r") as f:
            history = json.load(f)
    except FileNotFoundError:
        history = []

    for _ in range(num):
        history.append({"date": today})
    
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f)
