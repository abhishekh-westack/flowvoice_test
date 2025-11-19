#!/usr/bin/env python3
"""
Test script to verify Google Cloud Storage connection using ADC
"""
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.utils.gcs_uploader import get_gcs_uploader


def main():
    print("=" * 60)
    print("Testing Google Cloud Storage Connection")
    print("=" * 60)
    print()
    
    # Initialize uploader
    uploader = get_gcs_uploader()
    
    print()
    print("-" * 60)
    
    if not uploader.enabled:
        print("❌ GCS is not enabled")
        print()
        print("To enable GCS:")
        print("1. Set GCS_BUCKET_NAME in your .env file")
        print("2. Run: gcloud auth application-default login")
        print()
        return 1
    
    print("✅ GCS is properly configured!")
    print()
    print("Configuration:")
    print(f"  Bucket: {uploader.bucket_name}")
    print(f"  Project: {uploader.project_id or 'Not specified'}")
    print()
    
    # Test upload with a dummy file
    print("Testing file upload...")
    test_file = Path(__file__).parent / "test_file.txt"
    
    try:
        # Create a test file
        test_file.write_text("This is a test file for GCS upload verification.")
        
        # Upload it
        url = uploader.upload_file(
            str(test_file),
            blob_name="test-connection.txt",
            folder="test"
        )
        
        if url:
            print(f"✅ Test upload successful!")
            print(f"   URL: {url}")
            print()
            print("You can now delete the test file from GCS:")
            print(f"   gcloud storage rm gs://{uploader.bucket_name}/test/test-connection.txt")
        else:
            print("❌ Test upload failed")
            return 1
            
    finally:
        # Clean up local test file
        if test_file.exists():
            test_file.unlink()
    
    print()
    print("=" * 60)
    print("✅ All checks passed! GCS is ready to use.")
    print("=" * 60)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
