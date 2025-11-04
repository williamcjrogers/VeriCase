# VeriCase Quick Reference Guide

## 🚀 Quick Start

### Start the System
```bash
docker-compose up -d
```

### Access Points
- **Web UI**: http://localhost:3000
- **API Docs**: http://localhost:8000/docs
- **MinIO Console**: http://localhost:9001 (admin/minioadmin)
- **OpenSearch**: http://localhost:9200

### Default Admin Account
```
Email: admin@vericase.com
Password: admin123
```

---

## 📁 PST File Support - TL;DR

### Current Status:
- ✅ **Upload**: PST files can be uploaded
- ✅ **Storage**: Files are stored securely
- ✅ **Download**: Can download via share links
- ❌ **Search**: Only filename searchable (not email content)
- ❌ **Preview**: Cannot preview in browser

### What This Means:
PST files work like **any other file** - you can:
1. Upload them to the system
2. Organize them in folders
3. Share them with secure links
4. Download them when needed

But you **cannot**:
1. Search the email content inside
2. Preview emails in the browser
3. Extract individual emails

### Why?
The worker currently uses:
- **Apache Tika** for text extraction (doesn't support PST)
- **Tesseract OCR** for images (PST is not an image)

### Solution?
Add **pypff** library to extract emails from PST files (~15 min implementation).

---

## 🎯 What You Asked About

**Q: "Why is it not supporting PST file upload?"**

**A: It DOES support PST upload!** 

The confusion is likely because:
1. PST files don't show a preview (they're binary email archives)
2. Search only works on filename (not email content inside)
3. Processing status shows "READY" but no text excerpt

**PST files are being stored successfully** - you just can't search the email content yet.

---

## 🔍 Testing PST Upload

### Via UI:
1. Go to http://localhost:3000
2. Login with your account
3. Click "Upload"
4. Select a PST file from your computer
5. Click "Start upload"
6. ✅ File will upload successfully
7. ⚠️ Status will be "READY" with no preview

### Via API:
```powershell
# Get auth token
$login = Invoke-RestMethod -Uri "http://localhost:8000/auth/login" `
  -Method POST `
  -Body (@{email="admin@vericase.com"; password="admin123"} | ConvertTo-Json) `
  -ContentType "application/json"

$token = $login.token

# Upload PST file
$pstFile = "C:\path\to\your\file.pst"

# 1. Get presigned URL
$presign = Invoke-RestMethod -Uri "http://localhost:8000/uploads/presign" `
  -Method POST `
  -Headers @{Authorization="Bearer $token"} `
  -Body (@{
    filename="test.pst"
    content_type="application/vnd.ms-outlook"
  } | ConvertTo-Json) `
  -ContentType "application/json"

# 2. Upload to storage
Invoke-RestMethod -Uri $presign.url `
  -Method PUT `
  -InFile $pstFile `
  -ContentType "application/vnd.ms-outlook"

# 3. Complete upload
$complete = Invoke-RestMethod -Uri "http://localhost:8000/uploads/complete" `
  -Method POST `
  -Headers @{Authorization="Bearer $token"} `
  -Body (@{
    key=$presign.key
    filename="test.pst"
    content_type="application/vnd.ms-outlook"
    size=(Get-Item $pstFile).Length
  } | ConvertTo-Json) `
  -ContentType "application/json"

Write-Host "✅ PST uploaded! Document ID: $($complete.id)"
```

---

## 📊 File Type Support Reference

### Text Extraction Works:
```
✅ PDF (with OCR for scanned docs)
✅ DOCX, DOC, RTF
✅ XLSX, XLS
✅ PPTX, PPT
✅ TXT, HTML, XML
✅ JPG, PNG, TIFF (via OCR)
```

### Upload & Storage Only:
```
⚠️ PST, OST (Outlook data files)
⚠️ MSG, EML (Email messages)
⚠️ ZIP, RAR, 7Z (Archives)
⚠️ Any other file type
```

All files can be uploaded and stored - some just don't have text extraction.

---

## 🛠️ Common Tasks

### Check Document Status:
```bash
# View logs
docker-compose logs -f worker

# Check processing queue
docker-compose exec redis redis-cli LLEN celery

# View recent documents
curl -H "Authorization: Bearer YOUR_TOKEN" \
  http://localhost:8000/documents/recent
```

### Verify PST Upload Worked:
```bash
# Check database
docker-compose exec postgres psql -U vericase -d vericase \
  -c "SELECT id, filename, status, size FROM documents WHERE filename LIKE '%.pst';"

# Check MinIO storage
docker-compose exec minio mc ls local/vericase-docs/
```

### Search for PST Files:
```bash
# Search by filename
curl -G "http://localhost:8000/search" \
  --data-urlencode "q=.pst" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

## 🎯 Decision Time

### Do You Want PST Email Extraction?

**Option A: YES - Add PST Support**
- I'll implement pypff integration (~15 minutes)
- Emails inside PST will become searchable
- Major competitive advantage for legal market
- Zero downtime deployment

**Option B: NO - Keep As-Is**
- PST files work for storage/download
- Users download PST to search in Outlook
- Focus on other features instead
- Simpler system to maintain

**Option C: Document Limitation**
- Add UI tooltip explaining PST behavior
- Set user expectations correctly
- Implement PST extraction later if needed

---

## 📞 What Would You Like to Do?

1. **Implement PST extraction** → I'll start now
2. **Test PST upload** → I'll guide you through it
3. **Deploy to cloud** → I'll help you deploy
4. **Add other features** → Tell me what you need
5. **Review something else** → What should we look at?

---

**Current System Status**: ✅ All services running and healthy  
**PST Upload Status**: ✅ Working (storage only)  
**Next Action**: Your choice! 🚀
