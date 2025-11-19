# config/settings.py
import os

def screenshot_path(name, subfolder=None):
    base_dir = os.path.join(os.getcwd(), "screenshots")
    if subfolder:
        base_dir = os.path.join(base_dir, subfolder)
    os.makedirs(base_dir, exist_ok=True)
    return os.path.join(base_dir, f"{name}.png")
