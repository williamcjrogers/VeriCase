# Document Management System - Phase 2 Implementation Plan

## Overview
This document outlines the implementation plan for transforming the VeriCase Docs system into a full-featured document management system with private/shared folder structures, enhanced UI, and advanced features.

## Phase 2 Features

### 1. Private/Shared Folder Structure ⭐ HIGH PRIORITY

#### Backend Changes
- [ ] Add migration to create default folder structure for users
- [ ] Implement `/private/{user_id}/` path prefix for private files
- [ ] Implement `/shared/` path prefix for shared workspace
- [ ] Auto-create default folders on user registration:
  - `/private/{user_id}/Documents`
  - `/private/{user_id}/Projects`
  - `/private/{user_id}/Archive`
  - `/shared/General`
  - `/shared/Legal`
  - `/shared/HR`

#### Frontend Changes
- [ ] Update workspace tiles to navigate to correct path prefixes
- [ ] Add visual badges (🔒 Private, 🏢 Shared) on files and folders
- [ ] Filter folder tree by workspace type
- [ ] Update breadcrumbs to show workspace context

### 2. Folder Tiles View ⭐ HIGH PRIORITY

#### UI Components
- [ ] Create folder card/tile component with:
  - Folder icon/thumbnail
  - Folder name
  - Document count
  - Last modified date
  - Size indicator
- [ ] Implement grid layout for folder tiles
- [ ] Add view toggle (Grid/List) button
- [ ] Store user's view preference in localStorage
- [ ] Responsive grid (1-4 columns based on screen size)

#### Styling
- [ ] Card hover effects with shadow
- [ ] Folder color coding (private=blue, shared=green)
- [ ] Document type icons within folders
- [ ] Empty folder state

### 3. Enhanced Features

#### 3.1 Bulk Operations
- [ ] Multi-select with Ctrl/Shift (✅ Already implemented)
- [ ] Bulk move to folder
- [ ] Bulk delete
- [ ] Bulk download (zip)
- [ ] Bulk share
- [ ] Selection toolbar at bottom

#### 3.2 Favorites/Starring System
- [ ] Add `favorites` table to database
- [ ] Star/unstar button on files and folders
- [ ] "Starred" navigation item in sidebar
- [ ] Filter to show only starred items
- [ ] Star count in file metadata

#### 3.3 Recent Files View
- [ ] "Recent" navigation item (⏱ icon already in UI)
- [ ] Show files accessed in last 7 days
- [ ] Sort by last accessed time
- [ ] Include preview thumbnails
- [ ] Quick access shortcuts

#### 3.4 File Versioning
- [ ] Add `document_versions` table
- [ ] Track version history on file updates
- [ ] Version list in file details
- [ ] Restore previous version
- [ ] Compare versions (diff view)
- [ ] Version comments/notes

## Implementation Priority

### Sprint 1 (Current)
1. ✅ Dashboard landing page (COMPLETE)
2. Private/Shared folder structure (backend)
3. Folder tiles view (frontend)

### Sprint 2
1. View toggle (grid/list)
2. Favorites/starring system
3. Recent files view

### Sprint 3
1. Bulk operations enhancement
2. File versioning system
3. Advanced search filters

## Technical Considerations

### Database Schema Changes
```sql
-- Favorites table
CREATE TABLE favorites (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    document_id UUID REFERENCES documents(id) ON DELETE CASCADE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(user_id, document_id)
);

-- Document versions table
CREATE TABLE document_versions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    document_id UUID REFERENCES documents(id) ON DELETE CASCADE,
    version_number INTEGER NOT NULL,
    s3_key VARCHAR(2048) NOT NULL,
    size INTEGER,
    created_by UUID REFERENCES users(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    comment TEXT
);

-- Last accessed tracking
ALTER TABLE documents ADD COLUMN last_accessed_at TIMESTAMP WITH TIME ZONE;
ALTER TABLE documents ADD COLUMN last_accessed_by UUID REFERENCES users(id);
```

### API Endpoints Needed

```
POST   /api/favorites/{document_id}          # Star a file
DELETE /api/favorites/{document_id}          # Unstar a file
GET    /api/favorites                        # Get starred files

GET    /api/documents/recent                 # Get recent files

POST   /api/documents/{id}/versions          # Create new version
GET    /api/documents/{id}/versions          # List versions
POST   /api/documents/{id}/versions/{v}/restore  # Restore version

POST   /api/documents/bulk/move              # Bulk move
POST   /api/documents/bulk/delete            # Bulk delete
POST   /api/documents/bulk/share             # Bulk share
```

## Success Metrics

- Users can easily distinguish private vs shared content
- Folder navigation is intuitive with visual folder cards
- Bulk operations reduce time for managing multiple files
- Favorites provide quick access to important files
- Version history prevents data loss

## Notes

- Maintain backward compatibility with existing file paths
- Existing files can remain at root or be migrated to /shared/
- Private folders are user-specific and isolated
- Shared workspace is visible to all users in organization
