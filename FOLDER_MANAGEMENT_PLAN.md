# Folder Management System Implementation Plan

## Overview
Add comprehensive folder management to allow users to create, rename, and delete folders independently of file uploads.

## Backend API Endpoints to Add

### 1. Create Folder
`POST /folders`
```json
{
  "path": "projects/acme",
  "name": "contracts"
}
```
- Creates folder at specified path
- Returns: `{ "path": "projects/acme/contracts", "created": true }`

### 2. Rename Folder
`PATCH /folders`
```json
{
  "old_path": "projects/acme",
  "new_name": "acme-corp"
}
```
- Renames folder and updates all document paths
- Returns: `{ "old_path": "...", "new_path": "...", "documents_updated": 5 }`

### 3. Delete Folder
`DELETE /folders/{encoded_path}`
Query param: `?recursive=true`
- Deletes folder and optionally all documents within
- Returns: `{ "deleted": true, "documents_deleted": 3, "files_removed": 3 }`

### 4. List Folders (Enhanced)
`GET /folders`
- Returns hierarchical folder structure with metadata
- Shows empty folders (folders without documents)
- Returns: `{ "folders": [...] }`

## UI Enhancements

### Folder Tree
- Right-click context menu:
  - New Folder
  - Rename
  - Delete (with confirmation)
  - Refresh
- Visual indicators for:
  - Empty folders (different icon)
  - Folder with documents (document count badge)

### Toolbar
- "New Folder" button in main toolbar
- Breadcrumb improvements:
  - Each segment clickable
  - "New Subfolder" option

### Modal Dialogs
- Create Folder dialog
- Rename Folder dialog
- Delete confirmation with options:
  - Delete folder only (if empty)
  - Delete folder and all contents

## Data Model

### Option 1: Virtual Folders (Recommended)
- No separate table needed
- Folders are derived from document paths
- Store empty folders as simple records or in-memory

### Option 2: Folders Table
```sql
CREATE TABLE folders (
  id UUID PRIMARY KEY,
  path TEXT NOT NULL UNIQUE,
  name TEXT NOT NULL,
  parent_path TEXT,
  owner_user_id UUID REFERENCES users(id),
  created_at TIMESTAMP,
  UNIQUE(owner_user_id, path)
);
```

## Implementation Steps

1. ✅ Create API endpoints
2. ✅ Add folder operations to storage layer
3. ✅ Update UI with folder management
4. ✅ Add context menus
5. ✅ Test all operations
6. ✅ Document usage

## Benefits

- Better organization
- Easier bulk operations
- Clearer folder hierarchy
- Professional folder management like Dropbox/Google Drive
