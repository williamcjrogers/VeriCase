# PST File Support - Current Status & Solution

## 🎯 Quick Answer

**YES, PST files ARE supported for upload!** They just aren't processed for text extraction.

## What Works Now ✅

1. **Upload**: PST files can be uploaded via the UI
2. **Storage**: Files are stored securely in S3/MinIO
3. **Download**: Can be downloaded via secure share links
4. **Organization**: Can be placed in folders
5. **Metadata**: Filename, size, upload date are all tracked
6. **Sharing**: Can create secure share links with password protection

## What Doesn't Work ⚠️

1. **Text Extraction**: Cannot extract email content from PST files
2. **Preview**: Cannot preview PST files in browser
3. **Search**: Only searchable by filename, not by email content
4. **Status**: Will be marked as `READY` but with empty text

## Current Processing Flow

```
PST File Upload
    ↓
Stored in S3/MinIO ✅
    ↓
Worker tries Tika extraction ❌ (PST not supported by Tika)
    ↓
Worker tries OCR ❌ (Not a PDF/image)
    ↓
Document marked READY with no text ✅
    ↓
Indexed with filename only ✅
```

## File Types Currently Supported for Text Extraction

The worker (`worker/worker_app/worker.py`) uses:
- **Apache Tika**: MS Office (DOC, DOCX, XLS, XLSX, PPT, PPTX), PDF, TXT, HTML, XML, RTF
- **OCRmyPDF**: PDFs with embedded images (scanned documents)
- **Tesseract OCR**: JPG, PNG, TIFF, BMP images

### File Types NOT Supported for Text Extraction:
- ❌ **PST** (Outlook data files)
- ❌ **OST** (Outlook offline files)
- ❌ **MSG** (Individual Outlook emails)
- ❌ **EML** (Email message files)
- ❌ **MBOX** (Mail archive format)
- ❌ **ZIP/RAR** (Compressed archives)

But they **CAN still be uploaded and stored!**

## Solution Options

### Option 1: Add PST Email Extraction (Recommended for Legal Use)

This would make your system **extremely powerful for legal discovery**:

**Install pypff library:**
```bash
# In worker/Dockerfile, add:
RUN apt-get update && apt-get install -y libpff-dev python3-pypff
RUN pip install pypff
```

**Add PST processor to worker:**
```python
# In worker/worker_app/worker.py
import pypff

def _extract_pst_emails(file_bytes: bytes) -> str:
    """Extract all email text from PST file"""
    with tempfile.NamedTemporaryFile(suffix=".pst", delete=False) as tmp:
        tmp.write(file_bytes)
        tmp.flush()
        
        try:
            pst = pypff.file()
            pst.open(tmp.name)
            
            emails = []
            root = pst.get_root_folder()
            
            def process_folder(folder):
                # Process messages in this folder
                for i in range(folder.get_number_of_sub_messages()):
                    try:
                        msg = folder.get_sub_message(i)
                        email_text = f"""
Subject: {msg.get_subject() or '(no subject)'}
From: {msg.get_sender_name() or 'Unknown'} <{msg.get_sender_email_address() or ''}>
To: {msg.get_display_to() or ''}
Date: {msg.get_delivery_time() or ''}

{msg.get_plain_text_body() or msg.get_html_body() or '(no body)'}
---
"""
                        emails.append(email_text)
                    except:
                        continue
                
                # Process subfolders recursively
                for i in range(folder.get_number_of_sub_folders()):
                    try:
                        process_folder(folder.get_sub_folder(i))
                    except:
                        continue
            
            process_folder(root)
            pst.close()
            
            return "\n\n".join(emails)
        finally:
            os.remove(tmp.name)
    
    return ""

# Update the ocr_and_index task:
@celery_app.task(name="worker_app.worker.ocr_and_index", queue=settings.CELERY_QUEUE)
def ocr_and_index(doc_id: str):
    doc=_fetch_doc(doc_id)
    if not doc:
        return
    _update_status(doc_id,"PROCESSING",None)
    obj=s3.get_object(Bucket=doc["bucket"], Key=doc["s3_key"]); fb=obj["Body"].read()
    
    # Check for PST files
    name=(doc["filename"] or "").lower()
    if name.endswith(".pst"):
        text = _extract_pst_emails(fb)
    else:
        text=_tika_extract(fb)
        if not text or len(text.strip())<50:
            if name.endswith(".pdf"):
                with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
                    tmp.write(fb); tmp.flush()
                    text=_ocr_pdf_sidecar(tmp.name) or ""
                    try: os.remove(tmp.name + ".ocr.pdf")
                    except Exception: pass
                    os.remove(tmp.name)
            else:
                text=_ocr_image_bytes(fb) or ""
    
    excerpt=(text.strip()[:1000]) if text else ""
    _index_document(doc_id, doc["filename"], doc["created_at"], doc.get("content_type") or "application/octet-stream", doc.get("metadata"), text or "", doc.get("path"), doc.get("owner_user_id"))
    _update_status(doc_id,"READY",excerpt)
    return {"id": doc_id, "chars": len(text or "")}
```

### Option 2: Add MSG and EML Support Too

```python
# For MSG files
import extract_msg

def _extract_msg_email(file_bytes: bytes) -> str:
    with tempfile.NamedTemporaryFile(suffix=".msg", delete=False) as tmp:
        tmp.write(file_bytes)
        tmp.flush()
        try:
            msg = extract_msg.Message(tmp.name)
            return f"""
Subject: {msg.subject}
From: {msg.sender}
To: {msg.to}
Date: {msg.date}

{msg.body}
"""
        finally:
            os.remove(tmp.name)
```

### Option 3: Simple Documentation (Quick Fix)

Just add a tooltip in the UI explaining what works:

```html
<!-- In ui/index.html upload modal -->
<div style="margin-top: 1rem; padding: 0.75rem; background: #f0f9ff; border-left: 3px solid #0ea5e9; border-radius: 4px;">
  <strong>📧 Email Files (PST, MSG, EML):</strong> 
  <span style="color: #64748b;">
    Can be uploaded and stored but email content won't be searchable. 
    Download to view in Outlook.
  </span>
</div>
```

## Impact on Legal Discovery

If you implement PST extraction, VeriCase would:

✅ Extract all emails from PST archives  
✅ Make email content fully searchable  
✅ Support date-range filtering on emails  
✅ Enable keyword search across all correspondence  
✅ Compete with enterprise e-discovery tools  

**This is a HUGE competitive advantage for legal firms!**

## Recommendation

**Implement Option 1 (PST extraction)** because:
1. Legal professionals heavily use PST files for e-discovery
2. It's a major differentiator vs. competitors
3. The implementation is straightforward with pypff
4. It makes your "AI-powered" marketing claim even stronger

## Testing

To test PST upload right now:
1. Go to http://localhost:3000 (or your deployed URL)
2. Click "Upload"
3. Select a PST file
4. It WILL upload successfully
5. Check the database - document record will exist
6. Check S3/MinIO - file will be stored
7. Status will be "READY"
8. Text excerpt will be empty (no emails extracted yet)

---

**Question**: Do you want me to implement PST email extraction now? This would take about 10-15 minutes and make your system much more powerful for legal use cases.
