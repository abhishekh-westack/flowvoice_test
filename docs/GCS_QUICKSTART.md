# GCS Quick Start Guide

## Setup (One Time)

```bash
# 1. Authenticate with Google Cloud
gcloud auth application-default login

# 2. Configure .env file
echo "GCS_BUCKET_NAME=your-bucket-name" >> .env
echo "GCS_PROJECT_ID=your-project-id" >> .env

# 3. Test the connection
python scripts/test_gcs_connection.py
```

## What Changed

✅ **No more service account JSON files needed**
✅ **Uses Application Default Credentials (ADC)**
✅ **Works on local machine and Docker**
✅ **Better error messages**

## Authentication Methods

ADC automatically uses credentials in this order:

1. `GOOGLE_APPLICATION_CREDENTIALS` env var (if set) → Service account key file
2. `gcloud auth application-default login` → Your personal credentials
3. GCE/GKE metadata → When running in Google Cloud

## For Local Development

```bash
gcloud auth application-default login
```

## For Docker

Mount your ADC credentials:

```yaml
volumes:
  - ~/.config/gcloud:/root/.config/gcloud:ro
```

## For CI/CD

Use service account key:

```yaml
env:
  GOOGLE_APPLICATION_CREDENTIALS: ./gcs-key.json
```

## Disable GCS

Remove or comment out in `.env`:

```bash
# GCS_BUCKET_NAME=
```

## Status Messages

### ✅ Success
```
✓ GCS Upload enabled: bucket=your-bucket
  Project: your-project
  Using Google Application Default Credentials
```

### ❌ Not Configured
```
⚠ GCS Upload disabled: GCS_BUCKET_NAME not set in .env
```

### ❌ Not Authenticated
```
✗ Google ADC not found. Run: gcloud auth application-default login
```

## Files Modified

- `core/utils/gcs_uploader.py` - Removed credentials file requirement
- `.env.example` - Updated to show ADC setup
- `docs/GCS_SETUP.md` - Complete setup guide
- `scripts/test_gcs_connection.py` - New test script
