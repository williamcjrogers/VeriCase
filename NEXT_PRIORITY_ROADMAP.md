# VeriCase Docs - Next Priority Roadmap
**Date:** October 22, 2025  
**Current Status:** Core system operational, UI improvements needed

---

## 🎯 Priority 1: User Console & Account Management (URGENT)

### What's Missing
The system currently has NO user management interface. Users can't:
- View their profile
- Change their password  
- See their account details
- Manage settings
- View activity logs

### Implementation Plan

#### 1. Create Account Settings Page (`ui/account.html`)
**Priority:** HIGH  
**Estimated Time:** 2-3 hours

Features needed:
- User profile display (email, display name, role)
- Change password form
- Update display name
- View account created date
- Last login timestamp
- Account activity log

#### 2. Create Admin Dashboard (`ui/admin.html`)
**Priority:** HIGH  
**Estimated Time:** 3-4 hours

Features needed:
- User list table with:
  - Email, role, status, last login
  - Edit role button
  - Activate/deactivate toggle
- Invite new user button
- Pending invitations list with:
  - Email, role, expires date
  - Resend/revoke options
- System stats dashboard:
  - Total users
  - Total documents
  - Storage used
  - Recent activity

#### 3. Add User Management API Endpoints (`api/app/users.py`)
**Priority:** HIGH  
**Estimated Time:** 2-3 hours

New endpoints needed:
```python
GET    /users/me              # Get current user profile
PATCH  /users/me              # Update profile
POST   /users/me/password     # Change password
GET    /users                 # List all users (admin only)
PATCH  /users/{user_id}       # Update user (admin only)
POST   /invitations           # Send invitation (admin only)
GET    /invitations           # List invitations (admin only)
DELETE /invitations/{token}   # Revoke invitation (admin only)
POST   /invitations/{token}/accept  # Accept invitation
```

#### 4. Update Navigation (`ui/index.html`)
**Priority:** MEDIUM  
**Estimated Time:** 1 hour

Add to navigation:
- User dropdown menu in top-right with:
  - Display name / email
  - "Account Settings" link
  - "Admin Panel" link (if admin)
  - "Logout" button

---

## 🎯 Priority 2: Document Sharing UI (HIGH VALUE)

### What's Missing
Backend is ready but NO UI for:
- Sharing documents with other users
- Managing who has access
- Viewing documents shared with you
- Setting permissions (view/edit)

### Implementation Plan

#### 1. Share Modal Component
**Priority:** HIGH  
**Estimated Time:** 2-3 hours

Features:
- User search/select dropdown
- Permission level selector (view/edit)
- Expiration date picker (optional)
- Current shares list with revoke button
- Share via link option (existing feature)

#### 2. "Shared With Me" View
**Priority:** HIGH  
**Estimated Time:** 1-2 hours

Features:
- Separate tab/view in main UI
- List of documents shared with user
- Show who shared it
- Show permission level
- Filter by sharer

#### 3. Add Sharing API Endpoints (`api/app/sharing.py`)
**Priority:** HIGH  
**Estimated Time:** 2-3 hours

New endpoints needed:
```python
POST   /documents/{doc_id}/share       # Share with user
GET    /documents/{doc_id}/shares      # List shares
DELETE /documents/{doc_id}/shares/{user_id}  # Revoke
GET    /documents/shared-with-me       # List shared docs
POST   /folders/{path}/share           # Share folder
GET    /folders/{path}/shares          # List folder shares
```

---

## 🎯 Priority 3: UI/UX Improvements (MEDIUM)

### Current UI Limitations
1. No user feedback on actions (loading states, success/error messages)
2. No drag-and-drop for file upload
3. No bulk operations (select multiple documents)
4. No document preview thumbnails
5. No sorting options
6. No advanced filters

### Implementation Plan

#### 1. Add Toast Notifications
**Priority:** MEDIUM  
**Estimated Time:** 1 hour

Features:
- Success messages (document uploaded, folder created, etc.)
- Error messages (upload failed, permission denied, etc.)
- Loading indicators
- Auto-dismiss after 3-5 seconds

#### 2. Improve File Upload UX
**Priority:** MEDIUM  
**Estimated Time:** 2 hours

Features:
- Drag-and-drop zone
- Upload progress bars
- Multiple file selection
- Upload queue management
- Cancel upload option

#### 3. Add Bulk Actions
**Priority:** MEDIUM  
**Estimated Time:** 2 hours

Features:
- Select multiple documents (already partially implemented)
- Bulk move to folder
- Bulk delete
- Bulk download (as zip)
- Bulk share

#### 4. Document Grid View
**Priority:** LOW  
**Estimated Time:** 3 hours

Features:
- Toggle between list and grid view
- Thumbnail previews for PDFs/images
- Hover preview
- Quick actions on hover

---

## 🎯 Priority 4: Email & Notifications (MEDIUM)

### What's Missing
Email service is stubbed but not implemented:
- User invitations just log to console
- No password reset emails
- No share notifications
- No activity notifications

### Implementation Plan

#### 1. Configure Email Service
**Priority:** MEDIUM  
**Estimated Time:** 1-2 hours

Options:
- **SendGrid** (recommended - free tier available)
- **AWS SES** (if using AWS)
- **SMTP** (Gmail, Outlook, etc.)

#### 2. Implement Email Templates
**Priority:** MEDIUM  
**Estimated Time:** 2 hours

Templates needed:
- User invitation email
- Password reset email
- Document shared notification
- Welcome email

#### 3. Add Email Queue
**Priority:** LOW  
**Estimated Time:** 2 hours

Features:
- Queue emails via Celery
- Retry failed sends
- Email delivery status tracking

---

## 🎯 Priority 5: Security Enhancements (IMPORTANT)

### Current Security Gaps
1. No rate limiting
2. Default credentials in use
3. No audit logging
4. No 2FA option
5. No session management

### Implementation Plan

#### 1. Add Rate Limiting
**Priority:** HIGH  
**Estimated Time:** 1 hour

Features:
- Limit login attempts (5 per 15 min)
- Limit API requests per user (100 per min)
- Limit upload size/frequency

#### 2. Implement Audit Logging
**Priority:** MEDIUM  
**Estimated Time:** 2-3 hours

Log events:
- User login/logout
- Document upload/delete
- Share link creation
- Admin actions
- Failed login attempts
- Permission changes

#### 3. Add Session Management
**Priority:** MEDIUM  
**Estimated Time:** 2 hours

Features:
- View active sessions
- Revoke sessions
- Session expiration
- "Remember me" option

---

## 🎯 Priority 6: Advanced Features (FUTURE)

### Nice-to-Have Features
1. **Document Versioning** - Track changes over time
2. **Document Comments** - Add notes/comments to documents
3. **Document Tags** - Categorize documents with tags
4. **Advanced Search** - Filter by date, type, size, tags
5. **Workflows** - Document approval workflows
6. **Analytics Dashboard** - Usage statistics and insights
7. **Mobile App** - iOS/Android apps
8. **Desktop App** - Electron-based desktop client

---

## Quick Start Guide - What to Build First?

### Recommended Order (4-6 weeks of work)

#### Week 1: User Console (Most Important)
1. ✅ Day 1-2: Create `api/app/users.py` with all user management endpoints
2. ✅ Day 3: Create `ui/account.html` - User profile and settings
3. ✅ Day 4-5: Create `ui/admin.html` - Admin dashboard

#### Week 2: Document Sharing
1. ✅ Day 1-2: Create `api/app/sharing.py` with sharing endpoints
2. ✅ Day 3-4: Add share modal to main UI
3. ✅ Day 5: Add "Shared With Me" view

#### Week 3: UI/UX Improvements
1. ✅ Day 1: Add toast notifications
2. ✅ Day 2-3: Improve file upload (drag-drop, progress)
3. ✅ Day 4-5: Add bulk actions

#### Week 4: Email & Security
1. ✅ Day 1-2: Configure email service
2. ✅ Day 3: Create email templates
3. ✅ Day 4: Add rate limiting
4. ✅ Day 5: Implement audit logging

---

## Immediate Next Steps (Choose One)

### Option A: Start with User Console (Recommended)
**Why:** Users need to manage their accounts and admins need to manage users

**Steps:**
1. Create `api/app/users.py` with user management endpoints
2. Create `ui/account.html` for user settings
3. Create `ui/admin.html` for admin dashboard
4. Update navigation to link to these pages

**Impact:** HIGH - Makes the system actually usable for teams

### Option B: Start with Document Sharing
**Why:** Core feature that's expected in document management

**Steps:**
1. Create `api/app/sharing.py` with sharing endpoints
2. Add share button to document list
3. Create share modal component
4. Add "Shared With Me" view

**Impact:** HIGH - Enables collaboration

### Option C: Start with UI/UX Improvements
**Why:** Make existing features more polished and user-friendly

**Steps:**
1. Add toast notifications system
2. Improve file upload with drag-drop
3. Add bulk operations
4. Polish the interface

**Impact:** MEDIUM - Better user experience

---

## Resource Requirements

### Development Time Estimates
- **Priority 1 (User Console):** 8-10 hours
- **Priority 2 (Document Sharing):** 7-9 hours
- **Priority 3 (UI/UX):** 8-10 hours
- **Priority 4 (Email):** 5-6 hours
- **Priority 5 (Security):** 5-7 hours

**Total:** ~40-50 hours of development work

### Skills Needed
- Backend: Python/FastAPI, SQLAlchemy
- Frontend: HTML/CSS/JavaScript
- UI/UX: Basic design skills
- Email: SMTP/SendGrid integration

---

## Success Metrics

After implementing Priority 1-3, the system will have:
- ✅ Complete user management system
- ✅ Admin dashboard for user administration
- ✅ Document sharing with permissions
- ✅ Professional UI with feedback
- ✅ Polished user experience

**This will make VeriCase Docs production-ready for team use.**

---

## Questions to Answer

1. **Who will use this system?**
   - Internal team only?
   - External clients?
   - Both?

2. **What's the priority?**
   - User management (teams need this)
   - Document sharing (collaboration)
   - Better UI (polish)

3. **Timeline?**
   - Rush job (1-2 weeks)?
   - Normal pace (4-6 weeks)?
   - No rush (2-3 months)?

4. **Email service?**
   - Use SendGrid (easy)?
   - Use AWS SES (if on AWS)?
   - Use Gmail SMTP (quick test)?

---

**Recommendation:** Start with Priority 1 (User Console). It's the most critical missing piece for making this a real multi-user system.
