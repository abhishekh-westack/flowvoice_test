# config/env.py
import os
from dotenv import load_dotenv

load_dotenv()

# URLs
BASE_URL = os.getenv("BASE_URL", "https://app.dev.getflowvoice.com/en")
BASE_API = os.getenv("BASE_API", "https://api.dev.getflowvoice.com")
DEV_URL = os.getenv("DEV_URL", "https://app.dev.getflowvoice.com")
LOGIN_URL = os.getenv("LOGIN_URL", f"{DEV_URL}/en/login")
DASHBOARD_URL = os.getenv("DASHBOARD_URL", f"{DEV_URL}/dashboard")
GCS_BUCKET_NAME = os.getenv("GCS_BUCKET_NAME", "flowvoice-dev-playwright")
# Browser settings
HEADLESS = os.getenv("PLAYWRIGHT_HEADLESS", "true").lower() in ("1", "true", "yes")
SLOW_MO = int(os.getenv("PLAYWRIGHT_SLOW_MO", "0"))  # ms, 0 means disabled

# Artifacts paths (relative to repo root)
ARTIFACTS_DIR = os.getenv("ARTIFACTS_DIR", "artifacts")
SCREENSHOTS_DIR = os.path.join(ARTIFACTS_DIR, "screenshots")
VIDEOS_DIR = os.path.join(ARTIFACTS_DIR, "videos")

# Cleanup settings
# Delete local files after uploading to GCS (saves disk space)
DELETE_LOCAL_AFTER_GCS_UPLOAD = os.getenv("DELETE_LOCAL_AFTER_GCS_UPLOAD", "true").lower() in ("1", "true", "yes")
