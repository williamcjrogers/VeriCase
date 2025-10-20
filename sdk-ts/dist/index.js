import _fetch from 'cross-fetch';
function pickFetch(custom) {
    if (custom)
        return custom;
    if (typeof globalThis !== 'undefined' && globalThis.fetch) {
        return globalThis.fetch.bind(globalThis);
    }
    return _fetch;
}
export class VeriCaseDocsClient {
    constructor(baseUrl, opts) {
        this.base = baseUrl.replace(/\/$/, '');
        this.token = opts?.token;
        this.fetchImpl = pickFetch(opts?.fetchImpl);
    }
    setToken(token) {
        this.token = token;
    }
    headers(contentType = 'application/json') {
        const h = { 'Content-Type': contentType };
        if (this.token)
            h['Authorization'] = `Bearer ${this.token}`;
        return h;
    }
    // ---------- Auth ----------
    async signup(email, password) {
        const r = await this.fetchImpl(`${this.base}/auth/signup`, {
            method: 'POST',
            headers: this.headers(),
            body: JSON.stringify({ email, password }),
        });
        if (!r.ok)
            throw new Error(await r.text());
        const j = (await r.json());
        this.token = j.token;
        return j;
    }
    async login(email, password) {
        const r = await this.fetchImpl(`${this.base}/auth/login`, {
            method: 'POST',
            headers: this.headers(),
            body: JSON.stringify({ email, password }),
        });
        if (!r.ok)
            throw new Error(await r.text());
        const j = (await r.json());
        this.token = j.token;
        return j;
    }
    // ---------- Uploads ----------
    async presignUpload(filename, contentType, path) {
        const r = await this.fetchImpl(`${this.base}/uploads/presign`, {
            method: 'POST',
            headers: this.headers(),
            body: JSON.stringify({ filename, content_type: contentType || 'application/octet-stream', path }),
        });
        if (!r.ok)
            throw new Error(await r.text());
        return (await r.json());
    }
    async completeUpload(params) {
        const payload = {
            key: params.key,
            filename: params.filename,
            size: params.size,
            content_type: params.contentType || 'application/octet-stream',
            path: params.path,
            title: params.title,
        };
        const r = await this.fetchImpl(`${this.base}/uploads/complete`, {
            method: 'POST',
            headers: this.headers(),
            body: JSON.stringify(payload),
        });
        if (!r.ok)
            throw new Error(await r.text());
        return (await r.json());
    }
    /** Upload a browser File/Blob using a pre-signed URL. Returns the new document id. */
    async uploadFile(file, opts = {}) {
        const filename = opts.filename || (file instanceof File ? file.name : 'upload.bin');
        const contentType = opts.contentType || (file instanceof File ? file.type : 'application/octet-stream');
        const pre = await this.presignUpload(filename, contentType, opts.path);
        const put = await this.fetchImpl(pre.url, {
            method: 'PUT',
            headers: { 'Content-Type': contentType },
            body: file,
        });
        if (!put.ok)
            throw new Error(`Upload failed: ${await put.text()}`);
        const fin = await this.completeUpload({
            key: pre.key, filename, size: file.size ?? 0, contentType, path: opts.path, title: opts.title,
        });
        return fin.id;
    }
    /** Node.js helper: upload from a file path. */
    async uploadFileFromPath(filePath, opts = {}) {
        const { default: fs } = await import('node:fs');
        const { default: pathMod } = await import('node:path');
        const filename = opts.filename || pathMod.basename(filePath);
        const contentType = opts.contentType || 'application/octet-stream';
        const size = (await (await import('node:fs/promises')).stat(filePath)).size;
        const pre = await this.presignUpload(filename, contentType, opts.path);
        const stream = fs.createReadStream(filePath);
        const isNode = typeof process !== 'undefined' && !!process.versions?.node;
        const put = await this.fetchImpl(pre.url, {
            method: 'PUT',
            headers: { 'Content-Type': contentType, 'Content-Length': String(size) },
            body: stream,
            ...(isNode ? { duplex: 'half' } : {}),
        });
        if (!put.ok)
            throw new Error(`Upload failed: ${await put.text()}`);
        const fin = await this.completeUpload({
            key: pre.key, filename, size, contentType, path: opts.path, title: opts.title,
        });
        return fin.id;
    }
    // ---------- Search & docs ----------
    async search(q, pathPrefix) {
        const u = new URL(`${this.base}/search`);
        u.searchParams.set('q', q);
        if (pathPrefix)
            u.searchParams.set('path_prefix', pathPrefix);
        const r = await this.fetchImpl(u.toString(), { headers: this.headers() });
        if (!r.ok)
            throw new Error(await r.text());
        return (await r.json());
    }
    async listDocuments(opts = {}) {
        const u = new URL(`${this.base}/documents`);
        if (opts.limit != null)
            u.searchParams.set('limit', String(opts.limit));
        if (opts.offset != null)
            u.searchParams.set('offset', String(opts.offset));
        if (opts.pathPrefix)
            u.searchParams.set('path_prefix', opts.pathPrefix);
        if (opts.status)
            u.searchParams.set('status', opts.status);
        const r = await this.fetchImpl(u.toString(), { headers: this.headers() });
        if (!r.ok)
            throw new Error(await r.text());
        return (await r.json());
    }
    async getDocument(id) {
        const r = await this.fetchImpl(`${this.base}/documents/${id}`, { headers: this.headers() });
        if (!r.ok)
            throw new Error(await r.text());
        return (await r.json());
    }
    async getSignedUrl(id) {
        const r = await this.fetchImpl(`${this.base}/documents/${id}/signed_url`, { headers: this.headers() });
        if (!r.ok)
            throw new Error(await r.text());
        const j = await r.json();
        return j.url;
    }
    async createShare(id, opts = {}) {
        const r = await this.fetchImpl(`${this.base}/shares`, {
            method: 'POST',
            headers: this.headers(),
            body: JSON.stringify({
                document_id: id,
                hours: opts.hours ?? 24,
                password: opts.password || undefined,
            }),
        });
        if (!r.ok)
            throw new Error(await r.text());
        return (await r.json());
    }
    async deleteDocument(id) {
        const r = await this.fetchImpl(`${this.base}/documents/${id}`, {
            method: 'DELETE',
            headers: this.headers(),
        });
        if (!r.ok)
            throw new Error(await r.text());
    }
}
export default VeriCaseDocsClient;
