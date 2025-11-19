# Local File Cleanup & GCS URL Links in Allure

## Smart Allure Integration

Instead of embedding large video/screenshot files in Allure reports, we attach **GCS URLs as clickable links** when GCS is enabled. This makes Allure reports lightweight and fast.

## Configuration

```bash
# In .env file

# Enable GCS upload (attach URLs to Allure)
GCS_BUCKET_NAME=your-bucket-name

# Delete local files after GCS upload (default: true)
DELETE_LOCAL_AFTER_GCS_UPLOAD=true
```

## Behavior

### With GCS Enabled (Recommended - Default)

1. ✅ Screenshot captured
2. ✅ Video recorded
3. ✅ Both uploaded to GCS
4. ✅ **GCS URLs attached to Allure** (clickable links)
5. ✅ Local files deleted (saves disk space)

**Allure Report:**
- 📎 "Screenshot (GCS)" → clickable link to GCS
- 📎 "Video (GCS)" → clickable link to GCS
- ⚡ Fast & lightweight (no large files embedded)

**Result:** 
- Allure report: ~50 KB (just links)
- Files in GCS: accessible via links
- No local storage used

### With GCS Disabled (Fallback)

1. ✅ Screenshot captured
2. ✅ Video recorded
3. ✅ **Files embedded in Allure report**
4. ⚠️ Local files kept

**Allure Report:**
- 📷 Screenshot embedded (~150 KB)
- 🎥 Video embedded (~500 KB)
- 🐌 Larger report size

**Result:**
- Allure report: ~650 KB per failure
- Local files: kept in directories

## Benefits

### 🚀 Performance
- **Allure reports 10-20x smaller** (links vs embedded files)
- Faster report generation
- Faster report loading in browser
- Can handle 100+ test failures without slowdown

### 💾 Storage Savings
- **No duplicate storage** (not in local + Allure + GCS)
- Only stored in GCS (centralized)
- Allure reports stay lightweight even with many failures

### 🔗 Access
- Click link in Allure → opens file in browser
- Files accessible to entire team via GCS
- Persistent storage (won't lose files when cleaning workspace)

### 📊 Comparison

**Without GCS (embedding files):**
- 100 failed tests = ~65 MB Allure report
- Slow to generate and load
- Files lost if workspace cleaned

**With GCS (URL links):**
- 100 failed tests = ~5 MB Allure report (13x smaller!)
- Fast to generate and load
- Files persist in GCS
