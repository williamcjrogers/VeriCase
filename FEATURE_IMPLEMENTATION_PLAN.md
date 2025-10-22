# VeriCase Docs - Complete Feature Implementation Plan

## Phase 1: Folder Navigation Fixes ✅ (In Progress)

### Backend Changes ✅
- [x] Enhanced `/documents` endpoint with improved path filtering
- [x] Added `exact_folder` parameter for precise folder filtering
- [x] Fixed root folder handling (empty path = documents with no folder)
- [x] Added `/documents/{doc_id}` PATCH endpoint for moving documents
- [x] Improved folder rename to support full path changes

### Frontend Changes (Next)
- [ ] Verify folder click events properly call API with path_prefix
- [ ] Ensure breadcrumb navigation works correctly
- [ ] Add visual feedback when folder is selected/active
- [ ] Test drag-and-drop document moving to folders
- [ ] Improve subfolder creation modal with examples

### Testing
- [ ] Test clicking root "All documents" shows all docs
- [ ] Test clicking folder filters to only that folder's contents
- [ ] Test clicking nested folder shows nested contents
- [ ] Test drag-drop moves documents correctly
- [ ] Test breadcrumb navigation

---

## Phase 2: User Management System 🔨 (Next Priority)

### Database Schema
```sql
-- User roles and permissions
CREATE TYPE user_role AS ENUM ('admin', 'editor', 'viewer');

-- Add role to existing users table
ALTER TABLE users ADD COLUMN role user_role DEFAULT 'editor';
ALTER TABLE users ADD COLUMN is_active BOOLEAN DEFAULT true;
ALTER TABLE users ADD COLUMN last_login_at TIMESTAMP;

-- User invitations
CREATE TABLE user_invitations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) NOT NULL,
    invited_by UUID REFERENCES users(id) ON DELETE CASCADE,
    role user_role NOT NULL DEFAULT 'viewer',
    token VARCHAR(255) UNIQUE NOT NULL,
    expires_at TIMESTAMP NOT NULL,
    accepted_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_invitations_token ON user_invitations(token);
CREATE INDEX idx_invitations_email ON user_invitations(email);
```

### Backend API Endpoints

#### Account Management
```
GET /users/me - Get current user profile
PATCH /users/me - Update current user profile (name, email, password)
GET /users - List all users (admin only)
PATCH /users/{user_id} - Update user (admin only)
DELETE /users/{user_id} - Deactivate user (admin only)
```

#### User Invitations
```
POST /invitations - Send invitation email (admin only)
GET /invitations - List pending invitations (admin only)
DELETE /invitations/{id} - Cancel invitation (admin only)
GET /invitations/{token} - Validate invitation token
POST /invitations/{token}/accept - Accept invitation & create account
```

### Frontend Pages

#### Account Management Page (`ui/account.html`)
- User profile section
  - Display name
  - Email
  - Change password
  - Profile picture (future)
- Activity log
  - Recent logins
  - Recent uploads
  - Recent shares

#### User Management Page (`ui/admin/users.html`) - Admin Only
- User list table
  - Email
  - Role (admin/editor/viewer)
  - Status (active/inactive)
  - Last login
  - Actions (edit role, deactivate)
- Invite new user button
- Pending invitations list

#### Invitation Flow
1. Admin enters email + role
2. System generates unique token
3. Email sent with signup link
4. User clicks link → lands on signup page with token
5. User creates password
6. Account created with specified role

### Email System Integration
```python
# api/app/email.py
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

def send_invitation_email(to_email, token, invited_by):
    """Send invitation email with signup link"""
    signup_url = f"{FRONTEND_URL}/signup?token={token}"
    
    html = f"""
    <p>You've been invited to join VeriCase Docs by {invited_by}.</p>
    <p><a href="{signup_url}">Click here to accept and create your account</a></p>
    <p>This invitation will expire in 7 days.</p>
    """
    
    message = Mail(
        from_email='noreply@vericase.com',
        to_emails=to_email,
        subject='Invitation to VeriCase Docs',
        html_content=html
    )
    
    sg = SendGridAPIClient(SENDGRID_API_KEY)
    sg.send(message)
```

---

## Phase 3: Document Sharing System 🔨

### Database Schema
```sql
-- Document shares with users
CREATE TABLE document_shares (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    document_id UUID REFERENCES documents(id) ON DELETE CASCADE,
    shared_by UUID REFERENCES users(id) ON DELETE CASCADE,
    shared_with UUID REFERENCES users(id) ON DELETE CASCADE,
    permission VARCHAR(20) NOT NULL DEFAULT 'view', -- 'view' or 'edit'
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(document_id, shared_with)
);

CREATE INDEX idx_shares_document ON document_shares(document_id);
CREATE INDEX idx_shares_user ON document_shares(shared_with);

-- Shared folders
CREATE TABLE folder_shares (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    folder_path VARCHAR(500) NOT NULL,
    owner_id UUID REFERENCES users(id) ON DELETE CASCADE,
    shared_by UUID REFERENCES users(id) ON DELETE CASCADE,
    shared_with UUID REFERENCES users(id) ON DELETE CASCADE,
    permission VARCHAR(20) NOT NULL DEFAULT 'view',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(folder_path, owner_id, shared_with)
);

CREATE INDEX idx_folder_shares_path ON folder_shares(folder_path, owner_id);
CREATE INDEX idx_folder_shares_user ON folder_shares(shared_with);
```

### Backend API Endpoints

#### Document Sharing
```
POST /documents/{doc_id}/share - Share document with user
GET /documents/{doc_id}/shares - List who document is shared with
DELETE /documents/{doc_id}/shares/{user_id} - Revoke access
GET /documents/shared-with-me - List documents shared with current user
```

#### Folder Sharing
```
POST /folders/{path}/share - Share entire folder
GET /folders/{path}/shares - List folder sharing
DELETE /folders/{path}/shares/{user_id} - Revoke folder access
```

#### Permissions Middleware
```python
def check_document_access(doc_id, user, required_permission='view'):
    """Check if user has access to document"""
    doc = get_document(doc_id)
    
    # Owner always has access
    if doc.owner_user_id == user.id:
        return True
    
    # Check direct share
    share = db.query(DocumentShare).filter(
        DocumentShare.document_id == doc_id,
        DocumentShare.shared_with == user.id
    ).first()
    
    if share:
        if required_permission == 'edit':
            return share.permission == 'edit'
        return True
    
    # Check folder share
    if doc.path:
        folder_share = db.query(FolderShare).filter(
            FolderShare.folder_path == doc.path,
            FolderShare.owner_id == doc.owner_user_id,
            FolderShare.shared_with == user.id
        ).first()
        
        if folder_share:
            if required_permission == 'edit':
                return folder_share.permission == 'edit'
            return True
    
    return False
```

### Frontend Features

#### Share Document Modal
- Search users by email
- Select permission level (view/edit)
- List current shares
- Revoke button for each share

#### "Shared with Me" View
- Separate navigation item
- Shows all documents shared with current user
- Grouped by owner
- Indicate permission level (view/edit)
- Filter by permission type

#### Collaborative Folders
- Share entire folder with team
- All documents in folder inherit permissions
- Nested folders inherit parent permissions
- Visual indicator for shared folders in tree

---

## Phase 4: Advanced Features (Future)

### Real-time Collaboration
- WebSocket connections
- Live document updates
- Presence indicators
- Comments and annotations

### Advanced Permissions
- Custom permission sets
- Team/group management
- Department hierarchies
- Audit logs for access

### Notifications
- Email notifications for shares
- In-app notifications
- Activity feed
- Mentions and @tags

---

## Implementation Timeline

### Week 1: Folder Navigation
- Day 1-2: Fix backend filtering
- Day 3-4: Update frontend UI
- Day 5: Testing and refinements

### Week 2: User Management
- Day 1-2: Database schema + migrations
- Day 3-4: Backend API endpoints
- Day 5: Frontend account page

### Week 3: User Invitations
- Day 1-2: Invitation system backend
- Day 3: Email integration
- Day 4-5: Frontend invitation flow + testing

### Week 4: Document Sharing
- Day 1-2: Sharing database schema
- Day 3-4: Backend API + permissions
- Day 5: Frontend sharing UI

### Week 5: Collaborative Folders
- Day 1-2: Folder sharing backend
- Day 3-4: Shared with me view
- Day 5: Testing and refinements

---

## Security Considerations

1. **Role-Based Access Control**
   - Validate user roles on every request
   - Separate admin routes with middleware
   - Log all permission changes

2. **Invitation Security**
   - Tokens expire after 7 days
   - One-time use tokens
   - Rate limit invitation sending
   - Validate email domains

3. **Document Sharing**
   - Verify ownership before sharing
   - Audit trail for all shares
   - Ability to revoke access instantly
   - No cascading permissions without explicit grant

4. **Data Privacy**
   - Users can only see documents they own or have access to
   - Search respects permissions
   - Folder navigation filtered by access rights
   - Audit logs for sensitive operations

---

## Testing Checklist

### Folder Navigation
- [ ] Click folder filters documents correctly
- [ ] Breadcrumbs work
- [ ] Drag-drop moves documents
- [ ] Subfolder creation works
- [ ] Context menu operations work

### User Management
- [ ] Admin can invite users
- [ ] Invitation email sends
- [ ] User can accept invitation
- [ ] User roles work correctly
- [ ] Admin can manage users

### Document Sharing
- [ ] Share document with user
- [ ] Recipient sees in "Shared with Me"
- [ ] View/edit permissions work
- [ ] Revoke access works
- [ ] Cannot share documents you don't own

### Folder Sharing
- [ ] Share folder with user
- [ ] All documents in folder accessible
- [ ] Nested folders inherit permissions
- [ ] Revoke folder access works
- [ ] New documents added to shared folder are automatically shared
