# Google Cloud Storage Upload Setup

This guide explains how to set up Google Cloud Storage (GCS) for automatically uploading test artifacts (screenshots and videos) when tests fail.

## Prerequisites

1. Google Cloud account
2. A GCS bucket created
3. gcloud CLI installed

## Setup Steps

### 1. Install gcloud CLI

**macOS:**
```bash
brew install --cask google-cloud-sdk
```

**Linux:**
```bash
curl https://sdk.cloud.google.com | bash
exec -l $SHELL
```

**Windows:**
Download from: https://cloud.google.com/sdk/docs/install

### 2. Authenticate with Application Default Credentials (ADC)

```bash
# Login to Google Cloud
gcloud auth login

# Set up Application Default Credentials
gcloud auth application-default login

# Verify authentication
gcloud auth application-default print-access-token
```

### 3. Create a GCS Bucket

```bash
# Set your project
gcloud config set project YOUR_PROJECT_ID

# Create bucket
gcloud storage buckets create gs://your-test-artifacts-bucket \
    --location=us-central1 \
    --uniform-bucket-level-access

# Or create via Google Cloud Console:
# https://console.cloud.google.com/storage
```

### 4. Grant Required Permissions

Make sure your authenticated user has these permissions:
- `storage.objects.create`
- `storage.objects.delete`
- `storage.buckets.get`

```bash
# Grant yourself permissions (if needed)
gcloud storage buckets add-iam-policy-binding gs://your-test-artifacts-bucket \
    --member="user:your-email@example.com" \
    --role="roles/storage.objectAdmin"
```

### 5. Configure Environment Variables

Add to your `.env` file:

```bash
# Google Cloud Storage Configuration
GCS_BUCKET_NAME=your-test-artifacts-bucket
GCS_PROJECT_ID=your-project-id
```

**That's it!** No service account key file needed. ADC handles authentication automatically.

### 6. Install Google Cloud Storage Client

Already included in `requirements.txt`:

```bash
pip install google-cloud-storage
```

## How It Works

When a test fails:

1. ✅ Screenshot is saved locally to `screenshots/failures/`
2. ✅ Video is saved locally to `videos/`
3. ✅ Both are attached to Allure report
4. ✅ Both are uploaded to GCS (if configured)
5. ✅ GCS URLs are printed to console

**If GCS is not configured:** Tests will continue to work normally, artifacts will only be saved locally.

## GCS Access

### With Uniform Bucket-Level Access (Recommended)

Your bucket likely has uniform bucket-level access enabled. Files are uploaded but require IAM permissions to view:

```
✓ Uploaded to GCS: gs://your-bucket/test/file.txt
  Console: https://console.cloud.google.com/storage/browser/your-bucket/test
```

**To view files:** Users need the `Storage Object Viewer` role on the bucket.

### Without Uniform Bucket-Level Access (Legacy)

If your bucket uses legacy ACLs, files can be made public:

```python
# In conftest.py or gcs_uploader.py
uploader.upload_file(path, make_public=True)
```

## Folder Structure in GCS

```
your-bucket/
├── screenshots/
│   ├── test_login_success.png
│   ├── test_login_invalid_email.png
│   └── ...
└── videos/
    ├── test_login_success.webm
    ├── test_login_invalid_email.webm
    └── ...
```

## Security Notes

### Uniform Bucket-Level Access (Default/Recommended)

Modern GCS buckets use uniform bucket-level access. Access is controlled via IAM:

```bash
# Grant someone access to view files
gcloud storage buckets add-iam-policy-binding gs://your-bucket \
    --member="user:teammate@example.com" \
    --role="roles/storage.objectViewer"
```

Files are accessible via:
- Google Cloud Console
- `gsutil` CLI
- Direct URL (with proper IAM permissions)

### Legacy ACL (Optional)

If you need public files and your bucket doesn't have uniform bucket-level access:

```python
# In your code
uploader.upload_file(path, make_public=True)
```

**Note:** Google recommends using uniform bucket-level access for better security.

## Disable GCS Upload

To disable GCS upload, simply don't set the environment variables or remove them from `.env`:

```bash
# .env - GCS disabled
BASE_URL=https://app.dev.getflowvoice.com/en
# GCS_BUCKET_NAME=  # Leave commented out
```

## Testing the Setup

Run a test that you know will fail:

```bash
pytest tests/login/test_login_pom.py::test_login_invalid_email -v
```

Check the console output for:
```
✓ GCS Upload enabled: bucket=your-bucket-name
  Project: your-project-id
  Using Google Application Default Credentials
✓ Screenshot attached: screenshots/failures/test_login_invalid_email.png
✓ Uploaded to GCS (public): https://storage.googleapis.com/...
✓ Attached video: /path/to/video.webm (498334 bytes)
✓ Uploaded to GCS (public): https://storage.googleapis.com/...
```

## Troubleshooting

### "Google ADC not found"

**Error:**
```
✗ Google ADC not found. Run: gcloud auth application-default login
```

**Solution:**
```bash
gcloud auth application-default login
```

### "GCS Upload disabled: Missing configuration"

**Solution:** Check that `GCS_BUCKET_NAME` is set in your `.env` file.

### "403 Forbidden" Error

**Solution:** Grant your user the required permissions:
```bash
gcloud storage buckets add-iam-policy-binding gs://your-bucket \
    --member="user:your-email@example.com" \
    --role="roles/storage.objectAdmin"
```

### "Could not find google-cloud-storage"

**Solution:** Install the package:
```bash
pip install google-cloud-storage
```

### ADC Expired

If your ADC credentials expire:
```bash
gcloud auth application-default login
```

## Docker Support

To use GCS with Docker, mount your ADC credentials:

```yaml
# docker-compose.yml
services:
  tests:
    volumes:
      - ~/.config/gcloud:/root/.config/gcloud:ro
    environment:
      - GCS_BUCKET_NAME=${GCS_BUCKET_NAME}
      - GCS_PROJECT_ID=${GCS_PROJECT_ID}
```

Or use a service account key in Docker:

```yaml
services:
  tests:
    volumes:
      - ./gcs-key.json:/app/gcs-key.json:ro
    environment:
      - GOOGLE_APPLICATION_CREDENTIALS=/app/gcs-key.json
```

## CI/CD Integration

### GitHub Actions Example

```yaml
- name: Authenticate to Google Cloud
  uses: google-github-actions/auth@v1
  with:
    credentials_json: ${{ secrets.GCP_SA_KEY }}

- name: Run Tests
  env:
    GCS_BUCKET_NAME: ${{ secrets.GCS_BUCKET_NAME }}
    GCS_PROJECT_ID: ${{ secrets.GCS_PROJECT_ID }}
    GOOGLE_APPLICATION_CREDENTIALS: ${{ github.workspace }}/gcs-key.json
  run: |
    echo "${{ secrets.GCS_SERVICE_ACCOUNT_KEY }}" > gcs-key.json
    pytest
```

### Docker Example

```dockerfile
# Copy service account key
COPY gcs-key.json /app/gcs-key.json

# Set environment variables
ENV GOOGLE_APPLICATION_CREDENTIALS=/app/gcs-key.json
ENV GCS_BUCKET_NAME=your-bucket-name
```

## Cost Considerations

- **Storage:** ~$0.020 per GB per month (Standard storage)
- **Operations:** Class A operations (uploads) ~$0.05 per 10,000 operations
- **Bandwidth:** Egress charges apply for downloads

**Estimated cost for 1000 test failures/month:**
- 1000 screenshots (1 MB each) = 1 GB storage = $0.02/month
- 1000 videos (500 KB each) = 500 MB storage = $0.01/month
- Upload operations = $0.01/month

**Total: ~$0.04/month** (negligible)
