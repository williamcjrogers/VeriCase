# Folder Management API Documentation

## Overview

The VeriCase Docs system now supports full folder management, allowing users to create, rename, and delete folders independently of document uploads. Folders can be empty or contain documents, and all operations maintain referential integrity.

## Features

- **Create Empty Folders**: Create folders without needing to upload documents
- **Rename Folders**: Rename folders and automatically update all document paths
- **Delete Folders**: Delete empty folders or recursively delete folders with contents
- **Virtual + Explicit Folders**: Folders are derived from document paths (virtual) plus explicitly created empty folders
- **Path Validation**: Comprehensive validation prevents path traversal, invalid characters, and reserved names

## API Endpoints

### 1. Create Folder

**Endpoint:** `POST /folders`

**Description:** Creates a new empty folder

**Request Body:**
```json
{
  "path": "projects/acme/contracts"
}
```

**Response:**
```json
{
  "path": "projects/acme/contracts",
  "name": "contracts",
  "parent_path": "projects/acme",
  "created": true,
  "created_at": "2025-10-20T18:30:00Z"
}
```

**Error Codes:**
- `400`: Invalid path (contains invalid characters, reserved names, or path traversal)
- `409`: Folder already exists or path contains documents

### 2. List Folders

**Endpoint:** `GET /folders`

**Description:** Lists all folders (both virtual and empty) with metadata

**Response:**
```json
{
  "folders": [
    {
      "path": "projects",
      "name": "projects",
      "parent_path": null,
      "is_empty": false,
      "document_count": 5,
      "created_at": "2025-10-20T18:00:00Z"
    },
    {
      "path": "projects/acme",
      "name": "acme",
      "parent_path": "projects",
      "is_empty": false,
      "document_count": 3,
      "created_at": null
    },
    {
      "path": "projects/acme/drafts",
      "name": "drafts",
      "parent_path": "projects/acme",
      "is_empty": true,
      "document_count": 0,
      "created_at": "2025-10-20T18:30:00Z"
    }
  ]
}
```

**Field Descriptions:**
- `path`: Full folder path
- `name`: Folder name (last segment of path)
- `parent_path`: Parent folder path (null for root-level folders)
- `is_empty`: Whether folder contains no documents
- `document_count`: Number of documents directly in this folder (not including subfolders)
- `created_at`: When folder was explicitly created (null for virtual folders)

### 3. Rename Folder

**Endpoint:** `PATCH /folders`

**Description:** Renames a folder and updates all document paths

**Request Body:**
```json
{
  "old_path": "projects/acme",
  "new_name": "acme-corp"
}
```

**Response:**
```json
{
  "old_path": "projects/acme",
  "new_path": "projects/acme-corp",
  "documents_updated": 12,
  "success": true
}
```

**Behavior:**
- Updates folder record if it exists
- Updates all documents at the exact path
- Updates all documents in subfolders
- Updates all empty subfolders
- All operations are transactional (rolled back on error)

**Error Codes:**
- `400`: Invalid path or new name contains path separators
- `409`: Destination folder already exists or contains documents

### 4. Delete Folder

**Endpoint:** `DELETE /folders`

**Description:** Deletes a folder and optionally its contents

**Request Body:**
```json
{
  "path": "projects/acme/drafts",
  "recursive": false
}
```

**Non-Recursive Delete (recursive=false):**
- Only succeeds if folder is empty
- Returns error if folder contains documents

**Recursive Delete (recursive=true):**
- Deletes all documents in folder
- Deletes all documents in subfolders
- Deletes all empty subfolders
- Removes files from storage (MinIO)
- Removes documents from search index

**Response:**
```json
{
  "deleted": true,
  "path": "projects/acme/drafts",
  "documents_deleted": 0,
  "files_removed": 0
}
```

**Error Codes:**
- `400`: Invalid path or folder contains documents (when recursive=false)
- `500`: Failed to delete folder (with rollback)

## Path Validation Rules

The system enforces strict path validation:

### Allowed Characters
- Letters (a-z, A-Z)
- Numbers (0-9)
- Forward slash (/) for path separation
- Hyphen (-), underscore (_), period (.), space

### Prohibited Characters
- `< > : " | ? *`
- Backslash `\`
- Double dots `..` (path traversal)

### Reserved Names (Windows Compatibility)
The following names cannot be used as folder names:
- `CON`, `PRN`, `AUX`, `NUL`
- `COM1` through `COM9`
- `LPT1` through `LPT9`

### Limits
- **Maximum path length**: 1024 characters
- **Maximum depth**: 10 levels
- **Minimum path length**: 1 character (after normalization)

### Path Normalization
- Leading/trailing slashes are stripped
- Leading/trailing whitespace is stripped
- Paths are case-sensitive

## Database Schema

### Folders Table

```sql
CREATE TABLE folders (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    path VARCHAR(1024) NOT NULL,
    name VARCHAR(255) NOT NULL,
    parent_path VARCHAR(1024),
    owner_user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE,
    UNIQUE(owner_user_id, path)
);

CREATE INDEX idx_folders_owner ON folders(owner_user_id);
CREATE INDEX idx_folders_path ON folders(path);
CREATE INDEX idx_folders_parent_path ON folders(parent_path);
```

### Virtual Folders

Folders are **virtual by default** - they're derived from document paths. The `folders` table only tracks **explicitly created empty folders**. When documents are added to an empty folder, the folder record can optionally be removed (it becomes virtual).

## Usage Examples

### Example 1: Create Project Structure

```bash
# Create main project folder
curl -X POST http://localhost:8010/folders \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"path": "projects/client-abc"}'

# Create subfolders
curl -X POST http://localhost:8010/folders \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"path": "projects/client-abc/contracts"}'

curl -X POST http://localhost:8010/folders \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"path": "projects/client-abc/invoices"}'
```

### Example 2: Rename Client Folder

```bash
# Rename client-abc to client-abc-corp
# This automatically updates all document paths
curl -X PATCH http://localhost:8010/folders \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "old_path": "projects/client-abc",
    "new_name": "client-abc-corp"
  }'
```

### Example 3: Delete Empty Folder

```bash
# Delete empty drafts folder
curl -X DELETE http://localhost:8010/folders \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "path": "projects/client-abc/drafts",
    "recursive": false
  }'
```

### Example 4: Delete Folder with Contents

```bash
# Delete completed project and all documents
curl -X DELETE http://localhost:8010/folders \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "path": "projects/completed-project",
    "recursive": true
  }'
```

### Example 5: List All Folders

```bash
curl -X GET http://localhost:8010/folders \
  -H "Authorization: Bearer $TOKEN"
```

## Security Considerations

1. **User Isolation**: All folder operations are scoped to the authenticated user's `owner_user_id`
2. **Path Traversal Prevention**: Paths containing `..` are rejected
3. **Reserved Name Protection**: Windows reserved names are blocked
4. **Transaction Safety**: All multi-step operations use database transactions
5. **Storage Cleanup**: Deleted documents are removed from both storage and search index

## Error Handling

All endpoints return appropriate HTTP status codes:

- `200`: Success
- `400`: Bad request (invalid parameters)
- `401`: Unauthorized (missing or invalid token)
- `404`: Not found
- `409`: Conflict (folder exists, path contains documents)
- `500`: Internal server error (with rollback)

Error responses include descriptive messages:

```json
{
  "detail": "invalid path: path traversal not allowed"
}
```

## Integration with Document Upload

When uploading documents, you can specify a folder path:

```bash
# Upload to existing or new folder
curl -X POST http://localhost:8010/uploads/presign \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "filename": "contract.pdf",
    "content_type": "application/pdf",
    "path": "projects/client-abc/contracts"
  }'
```

If the folder doesn't exist, it will be created virtually when the document is uploaded.

## Future Enhancements

Potential future additions to folder management:

1. **Folder Metadata**: Add description, color, or icon fields
2. **Folder Permissions**: Per-folder access control
3. **Folder Templates**: Create folder structures from templates
4. **Folder Move**: Move folders between locations
5. **Bulk Operations**: Move multiple documents between folders
6. **Folder Search**: Search for folders by name or metadata
7. **Folder Tags**: Tag folders for organization
8. **Folder Statistics**: Track folder size, document count, last modified

## Testing

The folder management system has been implemented with:

- Path validation unit tests
- Transaction rollback on errors
- Comprehensive error messages
- Logging for debugging

To test the endpoints, use the provided examples or integrate with the UI.
