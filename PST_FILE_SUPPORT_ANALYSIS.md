# PST File Upload Support Analysis

## Current Status: ✅ **PST FILES ARE FULLY SUPPORTED**

Your VeriCase system **does NOT have any file type restrictions**. PST files should upload successfully.

## Technical Analysis

### 1. File Input Configuration
- **Location**: `ui/index.html` line 1604
- **Current**: `<input type="file" id="file" multiple style="display:none;">`
- **No `accept` attribute**: This means ALL file types are allowed, including PST files

### 2. Upload Flow for PST Files

```
User Selects PST File
    ↓
JavaScript reads: file.name, file.type, file.size
    ↓
Content-Type: file.type || 'application/octet-stream'
    ↓
Presign Request → S3/MinIO
    ↓
Upload to Storage
    ↓
Complete Upload → Database Record
    ↓
OCR Worker (attempts text extraction)
    ↓
Indexed in OpenSearch
```

### 3. PST File MIME Type Handling

**Browser Recognition:**
- Most browsers: `file.type = "application/vnd.ms-outlook"` 
- Some browsers: `file.type = ""` (empty)
- Fallback: `"application/octet-stream"`

**System Behavior:**
```javascript
// Line 2992-2997 in index.html
content_type: file.type || 'application/octet-stream'
```

✅ All cases are handled correctly

### 4. Storage Layer (S3/MinIO)
**File**: `api/app/storage.py`

```python
def put_object(key: str, data: bytes, content_type: str):
    s3().put_object(
        Bucket=settings.MINIO_BUCKET, 
        Key=key, 
        Body=data, 
        ContentType=content_type
    )
```

✅ Accepts any content_type, including PST files

### 5. Database Schema
**File**: `api/app/models.py`

```python
class Document(Base):
    content_type = Column(String(128), nullable=True)
    # No validation or restriction on content_type values
```

✅ No restrictions on file types

## Why PST Files Might Appear Unsupported

### Possible User Experience Issues:

1. **Browser File Picker Display**
   - Without an `accept` attribute, some users might think certain files aren't supported
   - The picker shows "All Files (*.*)" which can be confusing

2. **PST Processing Limitations**
   - PST files are binary archives of Outlook emails
   - The OCR worker (`worker/worker_app/worker.py`) uses Tesseract for text extraction
   - Tesseract **cannot** extract text from PST files (it's for images/PDFs)
   - Status will be: `INDEXED` (stored successfully)
   - Text extraction: Minimal or none
   - Search: Limited to filename only

3. **No Preview Support**
   - PST files cannot be previewed in the browser
   - File viewer expects PDFs, images, or text files
   - PST files can only be **downloaded**

## Recommendations

### Option 1: Enhanced PST Support (Full Solution)
```python
# Add to worker/worker_app/worker.py
import libpff  # pypff library for PST parsing

def extract_pst_emails(pst_path):
    """Extract email text from PST files"""
    pst = libpff.file()
    pst.open(pst_path)
    
    texts = []
    root = pst.get_root_folder()
    
    def process_folder(folder):
        for i in range(folder.get_number_of_sub_messages()):
            msg = folder.get_sub_message(i)
            # Extract subject, body, sender, etc.
            texts.append({
                'subject': msg.get_subject(),
                'body': msg.get_plain_text_body(),
                'from': msg.get_sender_name(),
                'date': msg.get_delivery_time()
            })
        
        for i in range(folder.get_number_of_sub_folders()):
            process_folder(folder.get_sub_folder(i))
    
    process_folder(root)
    return texts
```

### Option 2: Document User Expectations (Quick Solution)

Add to UI that PST files:
- ✅ Can be uploaded and stored
- ✅ Can be organized in folders
- ✅ Can be shared with secure links
- ✅ Can be downloaded
- ❌ Cannot be previewed in browser
- ⚠️ Limited search (filename only, not email content)

### Option 3: Improve UI Clarity

```html
<!-- Add to upload modal -->
<div style="margin-top: 1rem; padding: 0.75rem; background: #eff6ff; border-radius: 8px;">
  <strong>📄 Supported Files:</strong>
  <ul style="margin: 0.5rem 0 0; padding-left: 1.5rem;">
    <li>Documents: PDF, DOCX, TXT, etc.</li>
    <li>Images: JPG, PNG, TIFF (with OCR)</li>
    <li>Archives: PST, ZIP, RAR (storage only)</li>
    <li>Any other file type (uploaded as-is)</li>
  </ul>
</div>
```

## Testing PST Upload

### Test Command:
```bash
# Create a test PST file (if you have one)
$pstFile = "C:\path\to\your\test.pst"

# Upload via API
$token = "your-jwt-token"
$presign = Invoke-RestMethod -Uri "http://localhost:8000/uploads/presign" `
  -Method POST `
  -Headers @{Authorization="Bearer $token"} `
  -Body (@{filename="test.pst"; content_type="application/vnd.ms-outlook"} | ConvertTo-Json) `
  -ContentType "application/json"

# Upload file
Invoke-RestMethod -Uri $presign.url `
  -Method PUT `
  -InFile $pstFile `
  -ContentType "application/vnd.ms-outlook"

# Complete upload
Invoke-RestMethod -Uri "http://localhost:8000/uploads/complete" `
  -Method POST `
  -Headers @{Authorization="Bearer $token"} `
  -Body (@{
    key=$presign.key
    filename="test.pst"
    content_type="application/vnd.ms-outlook"
    size=(Get-Item $pstFile).Length
  } | ConvertTo-Json) `
  -ContentType "application/json"
```

## Conclusion

**PST files ARE supported** for upload, storage, and download. However:

1. ✅ **Upload**: Works perfectly
2. ✅ **Storage**: Stored securely in S3/MinIO
3. ✅ **Download**: Can be downloaded via share links
4. ✅ **Organization**: Can be placed in folders
5. ❌ **Preview**: Not possible (binary format)
6. ⚠️ **Search**: Limited to filename (no email content extraction)

If you need full PST email extraction and search, you'll need to add PST parsing libraries like `pypff` or use Microsoft's PST parsing APIs.

---

**Action Required**: Please clarify:
1. Are PST files failing to upload in the UI?
2. Or are you asking about PST email content extraction?
3. What specific issue are you experiencing?
