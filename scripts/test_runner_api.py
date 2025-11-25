from fastapi import FastAPI
from subprocess import Popen, run
from pathlib import Path
import shutil
import os
from google.cloud import storage
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()

TEST_PATHS = {
    "test-login": "tests/login/test_login.py",
    "test-signup": "tests/signup/test_signup.py",  # Update path as needed
    "test-dashboard": "tests/dashboard/test_dashboard.py",  # Update path as needed
    "test-assistant-creation": "tests/assistants/test_create_assistant.py",
    "test-voice-type": "tests/assistants/updates/voice/"
}
# Endpoint to run all voice assistant tab tests
@app.post("/test-voice-type")
def test_voice_type():
    run_pytest(TEST_PATHS["test-voice-type"])
    return {"test_started": True}

RESULTS_DIR = "allure-results"
REPORT_DIR = "allure-report"
GCS_BUCKET = os.getenv("GCS_BUCKET_NAME")  # Set in your .env
GCS_REPORT_PREFIX = os.getenv("GCS_REPORT_PREFIX", "allure-report/")  # Optional prefix

# Helper to start pytest for a given file
def run_pytest(test_file: str):
    # Ensure results directory exists
    Path(RESULTS_DIR).mkdir(exist_ok=True)
    # Start pytest in background
    Popen([
        "pytest", test_file, f"--alluredir={RESULTS_DIR}"
    ])

# Helper to delete local report folders
def delete_local_reports():
    for folder in [RESULTS_DIR, REPORT_DIR]:
        if Path(folder).exists():
            shutil.rmtree(folder)

# Helper to delete previous report from GCS
def delete_gcs_report_folder(report_folder):
    """Delete a specific timestamped report folder in GCS."""
    print(report_folder)
    if not GCS_BUCKET or not report_folder:
        return False
    try:
        client = storage.Client()
        bucket = client.bucket(GCS_BUCKET)
        blobs = bucket.list_blobs(prefix=report_folder)
        for blob in blobs:
            blob.delete()
        return True
    except Exception as e:
        print(f"GCS delete error: {e}")
        return False

# Helper to generate allure report
def generate_allure_report():
    result = run([
        "allure", "generate", RESULTS_DIR, "-o", REPORT_DIR, "--clean"
    ], capture_output=True)
    return result.returncode == 0

# Helper to upload allure report to GCS
def upload_report_to_gcs(report_folder):
    """Upload Allure report to a timestamped folder in GCS."""
    if not GCS_BUCKET or not report_folder:
        return False
    try:
        client = storage.Client()
        bucket = client.bucket(GCS_BUCKET)
        for root, _, files in os.walk(REPORT_DIR):
            for file in files:
                local_path = os.path.join(root, file)
                rel_path = os.path.relpath(local_path, REPORT_DIR)
                blob = bucket.blob(f"{report_folder}/{rel_path}")
                blob.upload_from_filename(local_path)
        return True
    except Exception as e:
        print(f"GCS upload error: {e}")
        return False

def delete_all_previous_reports():
    if not GCS_BUCKET:
        return False
    try:
        client = storage.Client()
        bucket = client.bucket(GCS_BUCKET)

        # Prefix for all reports (based on your structure)
        prefix = "allure-reports/"
        blobs = bucket.list_blobs(prefix=prefix)

        deleted_any = False
        for blob in blobs:
            blob.delete()
            deleted_any = True

        return deleted_any
    except Exception as e:
        print(f"GCS delete ALL reports error: {e}")
        return False


@app.post("/test-login")
def test_login():
    run_pytest(TEST_PATHS["test-login"])
    return {"test_started": True}

@app.post("/test-assistant-creation")
def test_assistant_creation():
    run_pytest(TEST_PATHS["test-assistant-creation"])
    return {"test_started": True}

@app.post("/test-dashboard")
def test_dashboard():
    run_pytest(TEST_PATHS["test-dashboard"])
    return {"test_started": True}

# Endpoint to generate, upload, and clean up Allure report
@app.post("/upload-report")
def upload_report():
    from datetime import datetime
    # Generate timestamped folder name
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_folder = f"allure-reports/{timestamp}"
    delete_all_previous_reports()
    # Optionally: delete previous report folder in GCS (not implemented here, can be added)

    # Generate new report
    if not generate_allure_report():
        return {"success": False, "error": "Allure report generation failed"}

    # Upload to GCS (timestamped folder)
    if not upload_report_to_gcs(report_folder):
        return {"success": False, "error": "GCS upload failed"}

    # Clean up local reports
    delete_local_reports()

    # Return GCS URL for the uploaded report
    gcs_url = f"https://console.cloud.google.com/storage/browser/{GCS_BUCKET}/{report_folder}"
    public_url = f"https://storage.googleapis.com/{GCS_BUCKET}/{report_folder}/index.html"
    return {
        "success": True,
        "message": "Report uploaded and cleaned up",
        "gcs_console_url": gcs_url,
        "public_url": public_url,
        "report_folder": report_folder
    }
