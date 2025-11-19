# Upload Allure Reports to GCS

## Quick Start

```bash
# Run tests
pytest

# Generate and upload report to GCS
./scripts/generate_and_upload_report.sh
```

## Manual Steps

### 1. Generate Allure Report

```bash
allure generate allure-results --clean -o allure-report
```

### 2. Upload to GCS

```bash
python scripts/upload_allure_report.py
```

## What Gets Uploaded

The entire Allure report directory is uploaded with a timestamp:

```
gs://your-bucket/allure-reports/
├── 20251117_140530/          # Timestamp folder
│   ├── index.html
│   ├── data/
│   ├── history/
│   └── ... (all report files)
├── 20251117_150230/          # Another run
│   └── ...
```

## Accessing Reports

### Option 1: Google Cloud Console

```
https://console.cloud.google.com/storage/browser/your-bucket/allure-reports
```

Click on timestamp folder → Download `index.html` and associated files → Open in browser

### Option 2: gsutil Download

```bash
# List available reports
gsutil ls gs://your-bucket/allure-reports/

# Download specific report
gsutil -m cp -r gs://your-bucket/allure-reports/20251117_140530 ./

# Open in browser
open 20251117_140530/index.html
```

### Option 3: Direct URL (if bucket is public)

```
https://storage.googleapis.com/your-bucket/allure-reports/20251117_140530/index.html
```

**Note:** This only works if your bucket has public access enabled.

## Make Reports Public (Optional)

If you want reports accessible via direct URL:

### Option A: Make Bucket Public

```bash
# Allow public read access to all objects
gsutil iam ch allUsers:objectViewer gs://your-bucket
```

### Option B: Make Specific Report Public

```bash
# Make a specific report folder public
gsutil -m acl set -r public-read gs://your-bucket/allure-reports/20251117_140530
```

**Security Note:** Only do this for non-sensitive test reports.

## CI/CD Integration

### GitHub Actions

```yaml
- name: Run Tests
  run: pytest

- name: Generate Allure Report
  if: always()
  run: allure generate allure-results --clean -o allure-report

- name: Upload Report to GCS
  if: always()
  run: python scripts/upload_allure_report.py
```

### GitLab CI

```yaml
after_script:
  - allure generate allure-results --clean -o allure-report
  - python scripts/upload_allure_report.py
```

## Cleanup Old Reports

To save storage costs, delete old reports:

```bash
# List reports older than 30 days
gsutil ls -l gs://your-bucket/allure-reports/ | grep "20251017"

# Delete specific report
gsutil -m rm -r gs://your-bucket/allure-reports/20251017_140530

# Delete all reports older than 30 days (be careful!)
# This requires a lifecycle policy or manual cleanup
```

## Storage Lifecycle Policy (Auto-delete old reports)

Create a lifecycle policy to auto-delete reports after 30 days:

```json
{
  "lifecycle": {
    "rule": [
      {
        "action": {"type": "Delete"},
        "condition": {
          "age": 30,
          "matchesPrefix": ["allure-reports/"]
        }
      }
    ]
  }
}
```

Apply it:

```bash
# Save above JSON to lifecycle.json
gsutil lifecycle set lifecycle.json gs://your-bucket
```

## Report Size

Typical Allure report:
- Small test suite (10 tests): ~2-5 MB
- Medium test suite (100 tests): ~10-20 MB
- Large test suite (1000 tests): ~50-100 MB

With history and screenshots, reports can grow larger.

## Troubleshooting

### "allure: command not found"

Install Allure:

```bash
# macOS
brew install allure

# Linux
sudo apt-add-repository ppa:qameta/allure
sudo apt-get update
sudo apt-get install allure
```

### Upload fails

Check:
1. GCS_BUCKET_NAME is set in .env
2. ADC is configured: `gcloud auth application-default login`
3. Bucket exists and you have write permissions

### Report doesn't render properly

Make sure to download the entire folder structure, not just `index.html`.

## Sharing Reports with Team

### Temporary Share (Signed URL)

If bucket is private, generate a signed URL (requires service account):

```python
from google.cloud import storage
from datetime import timedelta

client = storage.Client()
bucket = client.bucket('your-bucket')
blob = bucket.blob('allure-reports/20251117_140530/index.html')

url = blob.generate_signed_url(expiration=timedelta(hours=24))
print(url)
```

### Permanent Share

Make the report folder public:

```bash
gsutil -m acl set -r public-read gs://your-bucket/allure-reports/20251117_140530
```

Then share: `https://storage.googleapis.com/your-bucket/allure-reports/20251117_140530/index.html`
