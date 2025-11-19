#!/bin/bash
# Generate Allure report and upload to GCS

set -e

echo "=================================="
echo "Allure Report: Generate & Upload"
echo "=================================="
echo

# Step 1: Generate report
echo "📊 Step 1: Generating Allure report..."
allure generate allure-results --clean -o allure-report

echo
echo "✓ Report generated"
echo

# Step 2: Upload to GCS
echo "☁️  Step 2: Uploading to Google Cloud Storage..."
python scripts/upload_allure_report.py allure-report

echo
echo "✅ Done!"
