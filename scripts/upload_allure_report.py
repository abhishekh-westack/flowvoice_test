#!/usr/bin/env python3
"""
Upload Allure report to Google Cloud Storage
Run after generating allure report with: allure generate allure-results -o allure-report
"""
import sys
import os
from pathlib import Path
from datetime import datetime

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.utils.gcs_uploader import get_gcs_uploader


def upload_allure_report(report_dir: str = "allure-report"):
    """
    Upload entire Allure report directory to GCS
    
    Args:
        report_dir: Path to allure-report directory
    """
    report_path = Path(report_dir)
    
    if not report_path.exists():
        print(f"❌ Report directory not found: {report_path}")
        print()
        print("Generate report first:")
        print("  allure generate allure-results -o allure-report")
        return 1
    
    print("=" * 60)
    print("Uploading Allure Report to Google Cloud Storage")
    print("=" * 60)
    print()
    
    # Initialize GCS uploader
    gcs = get_gcs_uploader()
    
    if not gcs.enabled:
        print("❌ GCS is not configured. Cannot upload report.")
        print()
        print("To enable GCS:")
        print("1. Set GCS_BUCKET_NAME in .env")
        print("2. Run: gcloud auth application-default login")
        return 1
    
    # Create timestamped folder for this report
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_folder = f"allure-reports/{timestamp}"
    
    print(f"Uploading to: gs://{gcs.bucket_name}/{report_folder}/")
    print()
    
    # Upload all files in the report directory
    uploaded_files = []
    failed_files = []
    
    for file_path in report_path.rglob("*"):
        if file_path.is_file():
            # Get relative path from report_dir
            relative_path = file_path.relative_to(report_path)
            blob_name = f"{report_folder}/{relative_path}"
            
            print(f"Uploading: {relative_path}...", end=" ")
            
            url = gcs.upload_file(
                str(file_path),
                blob_name=blob_name,
                folder="",  # Don't add extra folder, we have full path in blob_name
                make_public=False
            )
            
            if url:
                uploaded_files.append(str(relative_path))
                print("✓")
            else:
                failed_files.append(str(relative_path))
                print("✗")
    
    print()
    print("=" * 60)
    print(f"✅ Upload Complete!")
    print(f"   Uploaded: {len(uploaded_files)} files")
    if failed_files:
        print(f"   Failed: {len(failed_files)} files")
    print("=" * 60)
    print()
    
    # Show access instructions
    print("📊 View Report:")
    print(f"   Console: https://console.cloud.google.com/storage/browser/{gcs.bucket_name}/{report_folder}")
    print()
    print(f"   Download index.html and open in browser, or use gsutil:")
    print(f"   gsutil cp -r gs://{gcs.bucket_name}/{report_folder} .")
    print(f"   open {timestamp}/index.html")
    print()
    
    # Optional: Create a public index.html URL if bucket allows
    index_url = f"https://storage.googleapis.com/{gcs.bucket_name}/{report_folder}/index.html"
    print("   Direct URL (if bucket is public):")
    print(f"   {index_url}")
    print()
    
    return 0 if not failed_files else 1


if __name__ == "__main__":
    report_dir = sys.argv[1] if len(sys.argv) > 1 else "allure-report"
    sys.exit(upload_allure_report(report_dir))
