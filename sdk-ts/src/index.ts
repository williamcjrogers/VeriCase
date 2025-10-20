import _fetch from 'cross-fetch';

export interface AuthResponse {
  token: string;
  user: { id: string; email: string };
}

export interface PresignResponse {
  key: string;
  url: string;
}

export interface CompleteUploadResponse {
  id: string;
  status: string;
}

export interface SearchHit {
  id: string;
  filename: string;
  title?: string;
  path?: string;
  content_type?: string;
  score: number;
  snippet?: string;
}

export interface SearchResponse {
  count: number;
  hits: SearchHit[];
}

export interface DocumentInfo {
  id: string;
  filename: string;
  path?: string;
  status: string;
  content_type?: string;
  size?: number;
  bucket?: string;
  s3_key?: string;
  title?: string;
  metadata?: Record<string, any>;
  text_excerpt?: string;
  created_at?: string;
  updated_at?: string;
}

export interface DocumentSummary {
  id: string;
  filename: string;
  path?: string;
  status: string;
  size: number;
  content_type?: string;
  title?: string;
  created_at: string;
  updated_at?: string;
}

export interface DocumentListResponse {
  total: number;
  items: DocumentSummary[];
}

export interface ListDocumentsOptions {
  pathPrefix?: string;
  status?: string;
  limit?: number;
  offset?: number;
}

export interface UploadOptions {
  path?: string;
  title?: string;
  contentType?: string;
  filename?: string;
}

type FetchType = typeof fetch;

function pickFetch(custom?: FetchType): FetchType {
  if (custom) return custom;
  if (typeof globalThis !== 'undefined' && (globalThis as any).fetch) {
    return (globalThis as any).fetch.bind(globalThis) as FetchType;
  }
  return (_fetch as unknown as FetchType);
}

export class VeriCaseDocsClient {
  private base: string;
  private token?: string;
  private fetchImpl: FetchType;

  constructor(baseUrl: string, opts?: { token?: string; fetchImpl?: FetchType }) {
    this.base = baseUrl.replace(/\/$/, '');
    this.token = opts?.token;
    this.fetchImpl = pickFetch(opts?.fetchImpl);
  }

  setToken(token: string) {
    this.token = token;
  }

  private headers(contentType = 'application/json'): Record<string, string> {
    const h: Record<string, string> = { 'Content-Type': contentType };
    if (this.token) h['Authorization'] = `Bearer ${this.token}`;
    return h;
  }

  // ---------- Auth ----------
  async signup(email: string, password: string): Promise<AuthResponse> {
    const r = await this.fetchImpl(`${this.base}/auth/signup`, {
      method: 'POST',
      headers: this.headers(),
      body: JSON.stringify({ email, password }),
    });
    if (!r.ok) throw new Error(await r.text());
    const j = (await r.json()) as AuthResponse;
    this.token = j.token;
    return j;
  }

  async login(email: string, password: string): Promise<AuthResponse> {
    const r = await this.fetchImpl(`${this.base}/auth/login`, {
      method: 'POST',
      headers: this.headers(),
      body: JSON.stringify({ email, password }),
    });
    if (!r.ok) throw new Error(await r.text());
    const j = (await r.json()) as AuthResponse;
    this.token = j.token;
    return j;
  }

  // ---------- Uploads ----------
  async presignUpload(filename: string, contentType?: string, path?: string): Promise<PresignResponse> {
    const r = await this.fetchImpl(`${this.base}/uploads/presign`, {
      method: 'POST',
      headers: this.headers(),
      body: JSON.stringify({ filename, content_type: contentType || 'application/octet-stream', path }),
    });
    if (!r.ok) throw new Error(await r.text());
    return (await r.json()) as PresignResponse;
  }

  async completeUpload(params: {
    key: string;
    filename: string;
    size: number;
    contentType?: string;
    path?: string;
    title?: string;
  }): Promise<CompleteUploadResponse> {
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
    if (!r.ok) throw new Error(await r.text());
    return (await r.json()) as CompleteUploadResponse;
  }

  /** Upload a browser File/Blob using a pre-signed URL. Returns the new document id. */
  async uploadFile(file: File | Blob, opts: UploadOptions = {}): Promise<string> {
    const filename = opts.filename || (file instanceof File ? file.name : 'upload.bin');
    const contentType = opts.contentType || (file instanceof File ? file.type : 'application/octet-stream');
    const pre = await this.presignUpload(filename, contentType, opts.path);
    const put = await this.fetchImpl(pre.url, {
      method: 'PUT',
      headers: { 'Content-Type': contentType },
      body: file as any,
    });
    if (!put.ok) throw new Error(`Upload failed: ${await put.text()}`);
    const fin = await this.completeUpload({
      key: pre.key, filename, size: (file as any).size ?? 0, contentType, path: opts.path, title: opts.title,
    });
    return fin.id;
  }

  /** Node.js helper: upload from a file path. */
  async uploadFileFromPath(filePath: string, opts: UploadOptions = {}): Promise<string> {
    const { default: fs } = await import('node:fs');
    const { default: pathMod } = await import('node:path');
    const filename = opts.filename || pathMod.basename(filePath);
    const contentType = opts.contentType || 'application/octet-stream';
    const size = (await (await import('node:fs/promises')).stat(filePath)).size;
    const pre = await this.presignUpload(filename, contentType, opts.path);
    const stream = fs.createReadStream(filePath);
    const isNode = typeof process !== 'undefined' && !!(process as any).versions?.node;
    const put = await this.fetchImpl(pre.url, {
      method: 'PUT',
      headers: { 'Content-Type': contentType, 'Content-Length': String(size) },
      body: stream as any,
      ...(isNode ? { duplex: 'half' as any } : {}),
    } as any);
    if (!put.ok) throw new Error(`Upload failed: ${await put.text()}`);
    const fin = await this.completeUpload({
      key: pre.key, filename, size, contentType, path: opts.path, title: opts.title,
    });
    return fin.id;
  }

  // ---------- Search & docs ----------
  async search(q: string, pathPrefix?: string): Promise<SearchResponse> {
    const u = new URL(`${this.base}/search`);
    u.searchParams.set('q', q);
    if (pathPrefix) u.searchParams.set('path_prefix', pathPrefix);
    const r = await this.fetchImpl(u.toString(), { headers: this.headers() });
    if (!r.ok) throw new Error(await r.text());
    return (await r.json()) as SearchResponse;
  }

  async listDocuments(opts: ListDocumentsOptions = {}): Promise<DocumentListResponse> {
    const u = new URL(`${this.base}/documents`);
    if (opts.limit != null) u.searchParams.set('limit', String(opts.limit));
    if (opts.offset != null) u.searchParams.set('offset', String(opts.offset));
    if (opts.pathPrefix) u.searchParams.set('path_prefix', opts.pathPrefix);
    if (opts.status) u.searchParams.set('status', opts.status);
    const r = await this.fetchImpl(u.toString(), { headers: this.headers() });
    if (!r.ok) throw new Error(await r.text());
    return (await r.json()) as DocumentListResponse;
  }

  async getDocument(id: string): Promise<DocumentInfo> {
    const r = await this.fetchImpl(`${this.base}/documents/${id}`, { headers: this.headers() });
    if (!r.ok) throw new Error(await r.text());
    return (await r.json()) as DocumentInfo;
  }

  async getSignedUrl(id: string): Promise<string> {
    const r = await this.fetchImpl(`${this.base}/documents/${id}/signed_url`, { headers: this.headers() });
    if (!r.ok) throw new Error(await r.text());
    const j = await r.json();
    return j.url as string;
  }

  async createShare(
    id: string,
    opts: { hours?: number; password?: string } = {},
  ): Promise<{ token: string; expires_at: string; requires_password: boolean }> {
    const r = await this.fetchImpl(`${this.base}/shares`, {
      method: 'POST',
      headers: this.headers(),
      body: JSON.stringify({
        document_id: id,
        hours: opts.hours ?? 24,
        password: opts.password || undefined,
      }),
    });
    if (!r.ok) throw new Error(await r.text());
    return (await r.json()) as any;
  }

  async deleteDocument(id: string): Promise<void> {
    const r = await this.fetchImpl(`${this.base}/documents/${id}`, {
      method: 'DELETE',
      headers: this.headers(),
    });
    if (!r.ok) throw new Error(await r.text());
  }
}

export default VeriCaseDocsClient;
