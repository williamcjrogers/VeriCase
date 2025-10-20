import { fileURLToPath } from 'node:url';
import { VeriCaseDocsClient } from '../sdk-ts/dist/index.js';

const baseUrl = 'http://localhost:8010';
const client = new VeriCaseDocsClient(baseUrl);

const email = `auto-share-${Date.now()}@example.com`;
const password = 'StrongPass!234';

const sharePassword = 'SharePass!123';
const watermarkText = 'Verified Recipient';

const pdfPath = fileURLToPath(new URL('../docs/share-demo.pdf', import.meta.url));

async function main() {
  console.log('Signing up test user', email);
  await client.signup(email, password);

  console.log('Uploading PDF for share test:', pdfPath);
  const documentId = await client.uploadFileFromPath(pdfPath, {
    path: 'projects/share-demo',
    title: 'Share Demo PDF',
  });
  console.log('Uploaded document id', documentId);

  console.log('Creating password-protected share link…');
  const shareRes = await client.createShare(documentId, { hours: 2, password: sharePassword });
  console.log('Share token', shareRes.token, 'requires password?', shareRes.requires_password);

  const shareUrl = `${baseUrl}/shares/${shareRes.token}`;

  console.log('Verifying share without password (should 401)…');
  const unauth = await fetch(shareUrl);
  if (unauth.status !== 401) {
    throw new Error(`Expected 401 without password, got ${unauth.status}`);
  }
  console.log('Unauthorised as expected.');

  console.log('Resolving share with correct password and watermark…');
  const params = new URLSearchParams({ password: sharePassword, watermark: watermarkText });
  const resolved = await fetch(`${shareUrl}?${params.toString()}`);
  if (!resolved.ok) {
    throw new Error(`Expected 200, got ${resolved.status}`);
  }
  const payload = await resolved.json();
  if (!payload.url || !payload.url.includes('X-Amz-Algorithm')) {
    throw new Error('Signed URL missing expected parameters');
  }
  console.log('Received signed URL:', payload.url.substring(0, 80), '…');
  console.log('Content type:', payload.content_type);

  console.log('Share flow verified successfully.');
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
