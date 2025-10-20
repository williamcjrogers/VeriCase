export interface AuthResponse {
    token: string;
    user: {
        id: string;
        email: string;
    };
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
export declare class VeriCaseDocsClient {
    private base;
    private token?;
    private fetchImpl;
    constructor(baseUrl: string, opts?: {
        token?: string;
        fetchImpl?: FetchType;
    });
    setToken(token: string): void;
    private headers;
    signup(email: string, password: string): Promise<AuthResponse>;
    login(email: string, password: string): Promise<AuthResponse>;
    presignUpload(filename: string, contentType?: string, path?: string): Promise<PresignResponse>;
    completeUpload(params: {
        key: string;
        filename: string;
        size: number;
        contentType?: string;
        path?: string;
        title?: string;
    }): Promise<CompleteUploadResponse>;
    /** Upload a browser File/Blob using a pre-signed URL. Returns the new document id. */
    uploadFile(file: File | Blob, opts?: UploadOptions): Promise<string>;
    /** Node.js helper: upload from a file path. */
    uploadFileFromPath(filePath: string, opts?: UploadOptions): Promise<string>;
    search(q: string, pathPrefix?: string): Promise<SearchResponse>;
    listDocuments(opts?: ListDocumentsOptions): Promise<DocumentListResponse>;
    getDocument(id: string): Promise<DocumentInfo>;
    getSignedUrl(id: string): Promise<string>;
    createShare(id: string, opts?: {
        hours?: number;
        password?: string;
    }): Promise<{
        token: string;
        expires_at: string;
        requires_password: boolean;
    }>;
    deleteDocument(id: string): Promise<void>;
}
export default VeriCaseDocsClient;
