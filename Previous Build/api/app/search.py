from opensearchpy import OpenSearch, RequestsHttpConnection
from .config import settings

_client = None

def client():
    global _client
    if _client is None:
        _client = OpenSearch(
            hosts=[{"host": settings.OPENSEARCH_HOST, "port": settings.OPENSEARCH_PORT}],
            http_compress=True,
            use_ssl=False,
            verify_certs=False,
            connection_class=RequestsHttpConnection,
        )
    return _client

def ensure_index():
    body = {
        "settings": {
            "index": {
                "number_of_shards": 1,
                "number_of_replicas": 0
            },
            "analysis": {
                "analyzer": {
                    "english_exact": {
                        "type": "standard",
                        "stopwords": "_english_"
                    }
                }
            }
        },
        "mappings": {
            "properties": {
                "id": {"type": "keyword"},
                "filename": {"type": "text"},
                "title": {"type": "text"},
                "content_type": {"type": "keyword"},
                "uploaded_at": {"type": "date"},
                "metadata": {"type": "object", "enabled": True},
                "text": {"type": "text", "analyzer": "english"},
            }
        }
    }
    c = client()
    if not c.indices.exists(settings.OPENSEARCH_INDEX):
        c.indices.create(index=settings.OPENSEARCH_INDEX, body=body)

def index_document(doc):
    body = {
        "id": str(doc["id"]),
        "filename": doc["filename"],
        "title": doc.get("title"),
        "content_type": doc.get("content_type"),
        "uploaded_at": doc.get("created_at"),
        "metadata": doc.get("metadata", {}),
        "text": doc.get("text", ""),
    }
    client().index(index=settings.OPENSEARCH_INDEX, id=str(doc["id"]), body=body, refresh=True)

def search(query: str, size: int = 25):
    dsl = {
        "size": size,
        "query": {
            "multi_match": {
                "query": query,
                "fields": ["text^3", "filename", "title", "metadata.*"]
            }
        },
        "highlight": {
            "fields": {"text": {}}
        }
    }
    return client().search(index=settings.OPENSEARCH_INDEX, body=dsl)
