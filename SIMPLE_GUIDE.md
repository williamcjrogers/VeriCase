# VeriCase Docs - Simple Guide
**What Works Now & How to Use It**

---

## 🚀 Quick Start

1. **Open the app:** http://localhost:8010/ui/index.html
2. **Click "Log In"** (credentials auto-fill)
3. **Upload files** with the Upload button
4. **That's it** - everything else is optional

---

## ✅ What Actually Works

### Basic Stuff (Ready to Use)
- ✓ Upload documents
- ✓ Create folders  
- ✓ Search documents
- ✓ Preview files
- ✓ Generate share links
- ✓ Drag documents to folders

### User Management (Just Added)
- ✓ Account Settings link (top-right) - change password, edit profile
- ✓ Admin Dashboard link (top-right, admins only) - manage users
- ✓ Click "Share" button → enter email → done

### Sharing (Just Added)
- ✓ Select document → Share button → enter user email → share
- ✓ Click "📩 Shared With Me" tab to see what others shared

---

## 🛠️ Common Tasks

### Share a Document with Someone
1. Select a document
2. Click "Share" in toolbar
3. Enter their email address
4. Choose "View Only" or "Can Edit"
5. Click "Share"
6. They can now click "📩 Shared With Me" to see it

### Make Yourself Admin
```bash
docker-compose exec api python -c "from app.db import SessionLocal; from app.models import User, UserRole; db = SessionLocal(); user = db.query(User).first(); user.role = UserRole.ADMIN; db
