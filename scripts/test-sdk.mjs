import { VeriCaseDocsClient } from '../sdk-ts/dist/index.js';
import { fileURLToPath } from 'url';
import path from 'node:path';

const base = 'http://localhost:8010';
const email = `dev+${Date.now()}@example.com`;
const password = 'StrongPass123!';

async function main() {
  const c = new VeriCaseDocsClient(base);
  try {
    await c.signup(email, password);
    console.log('Signed up:', email);
  } catch (e) {
    console.log('Signup failed (likely exists), trying login...');
    await c.login(email, password);
    console.log('Logged in');
  }

  const pathPrefix = 'projects/demo';
  const filePath = path.join(path.dirname(fileURLToPath(import.meta.url)), '..', 'docs', 'demo.txt');
  const id = await c.uploadFileFromPath(filePath, { path: pathPrefix, title: 'Demo Text' });
  console.log('Uploaded id:', id);

  // wait briefly for indexing
  await new Promise(r => setTimeout(r, 3000));
  const res = await c.search('Demo', pathPrefix);
  console.log('Search count:', res.count);

  const url = await c.getSignedUrl(id);
  console.log('Signed URL:', url);

  const share = await c.createShare(id, 1);
  console.log('Share token:', share.token);
  console.log('Public viewer:', `http://localhost:8010/ui/public-viewer.html?token=${share.token}`);
}

main().catch((e) => { console.error(e); process.exit(1); });
