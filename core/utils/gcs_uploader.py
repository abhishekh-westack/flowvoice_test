# core/utils/gcs_uploader.py
"""
Google Cloud Storage uploader for test artifacts (videos, screenshots)
Uses Google Application Default Credentials (ADC) for authentication.

Setup:
1. Install gcloud CLI: https://cloud.google.com/sdk/docs/install
2. Authenticate: gcloud auth application-default login
3. Set GCS_BUCKET_NAME in .env file
"""
import os
from pathlib import Path
from typing import Optional
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

class GCSUploader:
    """Upload test artifacts to Google Cloud Storage using ADC"""
    
    def __init__(self):
        self.bucket_name = os.getenv("GCS_BUCKET_NAME")
        self.project_id = os.getenv("GCS_PROJECT_ID")
        
        self._client = None
        self._bucket = None
        
        # Check if GCS is enabled (only need bucket name)
        self.enabled = bool(self.bucket_name)
        
        if self.enabled:
            try:
                from google.cloud import storage
                from google.auth.exceptions import DefaultCredentialsError
                
                # Use ADC - no credentials file needed
                # This automatically picks up credentials from:
                # 1. GOOGLE_APPLICATION_CREDENTIALS env var (if set)
                # 2. gcloud auth application-default login
                # 3. GCE/GKE metadata service (when running in Google Cloud)
                try:
                    self._client = storage.Client(project=self.project_id)
                    self._bucket = self._client.bucket(self.bucket_name)
                    
                    # Test bucket access
                    self._bucket.exists()
                    
                    print(f"✓ GCS Upload enabled: bucket={self.bucket_name}")
                    if self.project_id:
                        print(f"  Project: {self.project_id}")
                    print(f"  Using Google Application Default Credentials")
                    
                except DefaultCredentialsError:
                    print("✗ Google ADC not found. Run: gcloud auth application-default login")
                    self.enabled = False
                except Exception as auth_error:
                    print(f"✗ GCS authentication failed: {auth_error}")
                    print("  Make sure you have run: gcloud auth application-default login")
                    self.enabled = False
                    
            except ImportError:
                print("✗ google-cloud-storage not installed. Run: pip install google-cloud-storage")
                self.enabled = False
            except Exception as e:
                print(f"⚠ GCS Upload disabled: {e}")
                self.enabled = False
        else:
            print("⚠ GCS Upload disabled: GCS_BUCKET_NAME not set in .env")
    
    def upload_file(
        self, 
        local_path: str, 
        blob_name: Optional[str] = None,
        folder: str = "test-artifacts",
        make_public: bool = False
    ) -> Optional[str]:
        """
        Upload a file to GCS using Application Default Credentials
        
        Args:
            local_path: Local file path
            blob_name: Name in GCS (defaults to filename with timestamp)
            folder: Folder prefix in bucket (creates if doesn't exist)
            make_public: Attempt to make file public (only works without uniform bucket-level access)
        
        Returns:
            URL of uploaded file (public URL or gs:// path), or None if upload failed
        """
        if not self.enabled:
            return None
        
        try:
            local_path = Path(local_path)
            
            if not local_path.exists():
                print(f"✗ File not found: {local_path}")
                return None
            
            # Generate blob name if not provided
            if blob_name is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                blob_name = f"{timestamp}_{local_path.name}"
            
            # Add folder prefix (GCS automatically creates "folders")
            if folder:
                blob_name = f"{folder}/{blob_name}"
            
            # Upload file
            blob = self._bucket.blob(blob_name)
            blob.upload_from_filename(str(local_path))
            
            # Try to make public if requested (only works with legacy ACL)
            if make_public:
                try:
                    blob.make_public()
                    public_url = blob.public_url
                    print(f"✓ Uploaded to GCS (public): {public_url}")
                    return public_url
                except Exception:
                    # Uniform bucket-level access is enabled, can't use legacy ACLs
                    pass
            
            # Return gs:// URL for uniform bucket-level access buckets
            # Users with proper IAM permissions can access via console or gsutil
            gs_url = f"gs://{self.bucket_name}/{blob_name}"
            public_url = f"https://storage.googleapis.com/{self.bucket_name}/{blob_name}"
            
            print(f"✓ Uploaded to GCS: {gs_url}")
            print(f"  Console: https://console.cloud.google.com/storage/browser/{self.bucket_name}/{blob_name.split('/')[0]}")
            
            return public_url
            
        except Exception as e:
            print(f"✗ Failed to upload to GCS: {e}")
            return None
    
    def upload_screenshot(self, screenshot_path: str, test_name: str) -> Optional[str]:
        """Upload screenshot with test-specific naming"""
        blob_name = f"screenshots/{test_name}.png"
        return self.upload_file(screenshot_path, blob_name)
    
    def upload_video(self, video_path: str, test_name: str) -> Optional[str]:
        """Upload video with test-specific naming"""
        blob_name = f"videos/{test_name}.webm"
        return self.upload_file(video_path, blob_name)
    
    def upload_test_artifacts(
        self, 
        test_name: str,
        screenshot_path: Optional[str] = None,
        video_path: Optional[str] = None
    ) -> dict:
        """
        Upload both screenshot and video for a failed test
        
        Returns:
            dict with 'screenshot_url' and 'video_url'
        """
        result = {
            "screenshot_url": None,
            "video_url": None
        }
        
        if screenshot_path:
            result["screenshot_url"] = self.upload_screenshot(screenshot_path, test_name)
        
        if video_path:
            result["video_url"] = self.upload_video(video_path, test_name)
        
        return result


# Global singleton instance
_gcs_uploader = None

def get_gcs_uploader() -> GCSUploader:
    """Get or create GCS uploader singleton"""
    global _gcs_uploader
    if _gcs_uploader is None:
        _gcs_uploader = GCSUploader()
    return _gcs_uploader
