# @vericase/docs-sdk (TypeScript)

TypeScript/JS SDK for **VeriCase Docs** — upload via pre-signed URLs, complete ingestion, search, get signed preview URLs, and create share links.

## Install & Build
```bash
cd sdk-ts
npm install
npm run build
# import from ./dist in your app, or `npm pack` and install the tarball
```

## Usage (Browser / React)
```ts
import { VeriCaseDocsClient } from './dist/index.js';

const client = new VeriCaseDocsClient('http://localhost:8000');

await client.signup('you@example.com', 'StrongPass123'); // or client.login(...)

// upload a File from <input>
const id = await client.uploadFile(file, { path: 'projects/acme', title: 'Spec PDF' });

// search
const res = await client.search('warranty', 'projects/acme');

// browse the document library
const page = await client.listDocuments({ pathPrefix: 'projects/acme', limit: 20 });
if (page.items.length) {
  await client.deleteDocument(page.items[0].id);
}

// preview
const url = await client.getSignedUrl(id); // pass to PDF.js or an <iframe>
```

## Usage (Node.js)
```ts
import { VeriCaseDocsClient } from './dist/index.js';
const c = new VeriCaseDocsClient('http://localhost:8000');
await c.login('you@example.com','StrongPass123');
const id = await c.uploadFileFromPath('./docs/contract.pdf', { path: 'projects/demo' });
console.log('Uploaded id', id);
const hits = await c.search('payment terms', 'projects/demo');
console.log(hits.count, hits.hits.map(h => h.filename));
```

## Covered endpoints
- `signup`, `login`, `setToken`
- `presignUpload`, `completeUpload`
- `uploadFile` (browser) / `uploadFileFromPath` (Node)
- `search(q, pathPrefix?)`
- `listDocuments({ pathPrefix?, status?, limit?, offset? })`
- `getDocument(id)`
- `getSignedUrl(id)`
- `createShare(id, { hours?, password? })`
- `deleteDocument(id)`
