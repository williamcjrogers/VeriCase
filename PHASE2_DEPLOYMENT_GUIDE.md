# Phase 2 Document Management System - Deployment Guide

## ✅ Completed Implementation

### Backend Features
1. **Database Migration** - `api/migrations/20251023_enhanced_features.sql`
   - Favorites table for starring documents
   - Document versions table for version history
   - Last accessed tracking on documents
   - Workspace type classification (private/shared)
   - Auto-create default folders for new users
   - Shared workspace folder structure

2. **New API Endpoints**
   - `/favorites/*` - Favorites/starring system (api/app/favorites.py)
   - `/versions/*` - Document versioning (api/app/versioning.py)
   - `/documents/recent` - Recently accessed files
   - Workspace type auto-detection on upload

3. **Updated Models** (api/app/models.py)
   - `Favorite` - User document favorites
   - `DocumentVersion` - Version history
   - Enhanced `Document` model with workspace fields

### Frontend Features
1. **Dashboard Landing Page**
   - Welcome banner with user greeting
   - Three stat cards (Total Docs, Shared With Me, Recent Uploads)
   - Three workspace tiles (My Private Files, Shared Workspace, Shared With Me)
   - Quick search integration
   - Recent activity feed (last 10 documents)

2. **New UI Styles**
   - Folder grid view with cards
   - Private/Shared badges
   - Star/favorite button styles
   - View toggle (Grid/List) button
   - Enhanced folder cards with hover effects

3. **Navigation Improvements**
   - Dashboard-first experience (no immediate file listing)
   - Logo click returns to dashboard
   - Workspace tile navigation
   - Smooth view transitions

## 🚀 Deployment Steps

### 1. Start Docker Services
```bash
docker-compose up -d
```

### 2. Apply Database Migration
```bash
# Option A: Using Python
cd api
python apply_migration.py migrations/20251023_enhanced_features.sql

# Option B: Using Docker
docker-compose exec api python apply_migration.py migrations/20251023_enhanced_features.sql
```

### 3. Restart Services
```bash
docker-compose restart api worker
```

### 4. Verify Deployment
1. Open http://localhost (or your deployment URL)
2. Login/Signup - should see dashboard
3. Click workspace tiles - should navigate to files
4. Check folder structure - default folders should exist for new users
5. Upload a file to `private/{user_id}/Documents` - should be marked as private
6. Upload a file to `shared/General` - should be marked as shared

## 📋 Migration Created Features

### Auto-Created Folder Structure

**For Each New User:**
```
private/{user_id}/
  ├── Documents/
  ├── Projects/
  └── Archive/
```

**Shared Workspace (One Time):**
```
shared/
  ├── General/
  ├── Legal/
  ├── HR/
  ├── Finance/
  └── Projects/
```

### New Database Tables

1. **favorites**
   - Tracks user-starred documents
   - Quick access to important files

2. **document_versions**
   - Version history for all document changes
   - Restore previous versions
   - Track who made changes and when

3. **Document enhancements**
   - `last_accessed_at` - Track recent file access
   - `last_accessed_by` - Who accessed the file
   - `workspace_type` - 'private' or 'shared'
   - `is_private` - Boolean flag for quick filtering

## 🔧 Configuration

### Environment Variables
No new environment variables required. Uses existing:
- `DATABASE_URL` - PostgreSQL connection
- `MINIO_*` - Object storage
- `JWT_SECRET` - Authentication

### Feature Flags
Current implementation is always-on. Optional flags could be:
- `ENABLE_VERSIONING=true` - Enable document versioning
- `ENABLE_FAVORITES=true` - Enable starring/favorites
- `AUTO_CREATE_FOLDERS=true` - Auto-create user folders

## 🎯 Usage Guide

### For End Users

**Dashboard View:**
1. Login to see dashboard with stats
2. Click "My Private Files" for personal documents
3. Click "Shared Workspace" for team documents
4. Click "Shared With Me" for documents others shared
5. Use Quick Search to find documents across all workspaces

**Workspace View:**
- Upload files to specific folders
- Private folder syntax: `private/{your-user-id}/Documents`
- Shared folder syntax: `shared/Legal`
- Files automatically tagged as private/shared based on location

**Favorites:**
- Click star icon on any document to favorite
- Access favorites via "⭐ Favorites" navigation

**Versioning:**
- Upload new version of existing file
- View version history
- Restore previous versions
- Each version is preserved in storage

### For Administrators

**Shared Folder Management:**
- Create new shared folders as needed
- Set permissions on shared folders
- Monitor usage across workspaces

**User Management:**
- Default folders created automatically on signup
- Each user gets isolated private workspace
- All users can access shared workspace

## 📊 API Endpoints Reference

### Favorites
```
POST   /favorites/{document_id}          - Star a document
DELETE /favorites/{document_id}          - Unstar a document
GET    /favorites                        - List starred documents
GET    /favorites/check/{document_id}    - Check if starred
```

### Versioning
```
GET    /versions/documents/{id}                    - List versions
POST   /versions/documents/{id}                    - Create new version
POST   /versions/documents/{id}/restore/{version}  - Restore version
GET    /versions/documents/{id}/{version}/download - Download version
```

### Documents
```
GET    /documents/recent                 - Recent documents
GET    /documents?path_prefix=private/   - Filter by workspace
GET    /documents?path_prefix=shared/    - Filter by workspace
```

## 🐛 Troubleshooting

### Migration Issues
- **Error: "could not translate host name 'postgres'"**
  - Solution: Start Docker services first with `docker-compose up -d`
  
- **Error: "relation already exists"**
  - Solution: Migration is idempotent, safe to re-run

### Feature Issues
- **Default folders not created**
  - Check trigger is active: `SELECT * FROM pg_trigger WHERE tgname = 'trigger_create_user_folders';`
  - Manually run migration again

- **Workspace type not set**
  - Old documents may not have workspace_type
  - Run update: `UPDATE documents SET workspace_type = 'shared', is_private = false WHERE workspace_type IS NULL;`

## 🔄 Rollback Plan

If issues occur, rollback with:
```sql
-- Rollback migration
DROP TABLE IF EXISTS document_versions CASCADE;
DROP TABLE IF EXISTS favorites CASCADE;
DROP TRIGGER IF EXISTS trigger_create_user_folders ON users;
DROP FUNCTION IF EXISTS create_default_user_folders();
ALTER TABLE documents DROP COLUMN IF EXISTS last_accessed_at;
ALTER TABLE documents DROP COLUMN IF EXISTS last_accessed_by;
ALTER TABLE documents DROP COLUMN IF EXISTS is_private;
ALTER TABLE documents DROP COLUMN IF EXISTS workspace_type;
```

Then restart services.

## 📈 Next Steps

After deployment, consider:
1. Migrate existing documents to appropriate workspaces
2. Set up folder permissions/sharing
3. Enable file versioning workflow
4. Train users on new interface
5. Monitor storage for version accumulation

## 🎉 Success Criteria

Deployment successful if:
- ✅ Dashboard appears on login (not file list)
- ✅ Workspace tiles navigate correctly
- ✅ New user gets default private folders
- ✅ Shared folders exist and accessible
- ✅ Files uploaded to private/* marked as private
- ✅ Files uploaded to shared/* marked as shared
- ✅ Star/favorite buttons functional
- ✅ Recent files view works
- ✅ Version history available
