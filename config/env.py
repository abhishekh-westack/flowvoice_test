# config/env.py
import os
from dotenv import load_dotenv

load_dotenv()

# URLs
BASE_URL = os.getenv("BASE_URL")
BASE_API = os.getenv("BASE_API")
DEV_URL = os.getenv("DEV_URL")
LOGIN_URL = os.getenv("LOGIN_URL")
DASHBOARD_URL = os.getenv("DASHBOARD_URL")
GCS_BUCKET_NAME = os.getenv("GCS_BUCKET_NAME")
HEADLESS = os.getenv("PLAYWRIGHT_HEADLESS", "true").lower() in ("1", "true", "yes")
SLOW_MO = int(os.getenv("PLAYWRIGHT_SLOW_MO", "0"))
ARTIFACTS_DIR = os.getenv("ARTIFACTS_DIR")
SCREENSHOTS_DIR = os.getenv("SCREENSHOTS_DIR")
VIDEOS_DIR = os.getenv("VIDEOS_DIR")
DELETE_LOCAL_AFTER_GCS_UPLOAD = os.getenv("DELETE_LOCAL_AFTER_GCS_UPLOAD", "true").lower() in ("1", "true", "yes")


LOGIN_EMAIL = os.getenv("LOGIN_EMAIL")
LOGIN_CODE = os.getenv("LOGIN_CODE")
LOGIN_COMPANY_ID = os.getenv("LOGIN_COMPANY_ID")

DOMAIN = os.getenv("DOMAIN")

ASSISTANT_VOICE_ID = os.getenv("ASSISTANT_VOICE_ID")
ASSISTANT_NAME = os.getenv("ASSISTANT_NAME")
ASSISTANT_TYPE_VOICE_ID = os.getenv("ASSISTANT_TYPE_VOICE_ID")
ASSISTANT_KNOWHOW_NAME = os.getenv("ASSISTANT_KNOWHOW_NAME")

CALENDAR_SECONDARY_ID_1 = os.getenv("CALENDAR_SECONDARY_ID_1")
CALENDAR_SECONDARY_ID_2 = os.getenv("CALENDAR_SECONDARY_ID_2")
PRIMARY_CAL_ID = os.getenv("PRIMARY_CAL_ID")
DOCTENA_CALENDAR_ID = os.getenv("DOCTENA_CALENDAR_ID")