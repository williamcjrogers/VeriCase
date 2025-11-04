-- Add missing email fields to evidence table
ALTER TABLE evidence ADD COLUMN IF NOT EXISTS email_cc VARCHAR(500);
ALTER TABLE evidence ADD COLUMN IF NOT EXISTS email_message_id VARCHAR(500);
ALTER TABLE evidence ADD COLUMN IF NOT EXISTS email_in_reply_to VARCHAR(500);
ALTER TABLE evidence ADD COLUMN IF NOT EXISTS email_thread_topic VARCHAR(500);
ALTER TABLE evidence ADD COLUMN IF NOT EXISTS email_conversation_index VARCHAR(500);
ALTER TABLE evidence ADD COLUMN IF NOT EXISTS thread_id VARCHAR(500);
ALTER TABLE evidence ADD COLUMN IF NOT EXISTS content TEXT;
ALTER TABLE evidence ADD COLUMN IF NOT EXISTS content_type VARCHAR(50);
ALTER TABLE evidence ADD COLUMN IF NOT EXISTS attachments JSON;

-- Create indexes for threading
CREATE INDEX IF NOT EXISTS idx_evidence_email_message_id ON evidence(email_message_id);
CREATE INDEX IF NOT EXISTS idx_evidence_email_in_reply_to ON evidence(email_in_reply_to);

SELECT 'Migration complete!' as status;
