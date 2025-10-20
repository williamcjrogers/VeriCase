import logging
import time
from opensearchpy import OpenSearch, RequestsHttpConnection
from opensearchpy.exceptions import NotFoundError
from .config import settings
_client=None

logger = logging.getLogger(__name__)
def client():
    global _client
    if _client is None:
        _client = OpenSearch(hosts=[{"host": settings.OPENSEARCH_HOST, "port": settings.OPENSEARCH_PORT}],
                             http_compress=True, use_ssl=False, verify_certs=False,
                             connection_class=RequestsHttpConnection)
    return _client
def ensure_index():
    body={"settings":{"index":{"number_of_shards":1,"number_of_replicas":0}},
          "mappings":{"properties":{
              "id":{"type":"keyword"},
              "filename":{"type":"text"},
              "title":{"type":"text"},
              "path":{"type":"keyword"},
              "owner":{"type":"keyword"},
              "content_type":{"type":"keyword"},
              "uploaded_at":{"type":"date"},
              "metadata":{"type":"object","enabled":True},
              "text":{"type":"text","analyzer":"english"}
          }}}
    # Wait for OpenSearch to be reachable and ensure index
    deadline = time.time() + 60
    last_err = None
    while time.time() < deadline:
        try:
            c = client()
            if not c.indices.exists(settings.OPENSEARCH_INDEX):
                c.indices.create(index=settings.OPENSEARCH_INDEX, body=body)
            return
        except Exception as e:
            last_err = e
            time.sleep(2)
    if last_err:
        raise last_err
def index_document(doc):
    body={"id":str(doc["id"]),"filename":doc["filename"],"title":doc.get("title"),
          "path":doc.get("path"),"owner":doc.get("owner_user_id"),
          "content_type":doc.get("content_type"),"uploaded_at":doc.get("created_at"),
          "metadata":doc.get("metadata",{}),"text":doc.get("text","")}
    client().index(index=settings.OPENSEARCH_INDEX, id=str(doc["id"]), body=body, refresh=True)
def search(query: str, size: int=25, path_prefix: str|None=None):
    must=[{"multi_match":{"query":query,"fields":["text^3","filename","title","metadata.*"]}}]
    if path_prefix: must.append({"prefix":{"path": path_prefix}})
    dsl={"size":size,"query":{"bool":{"must":must}},"highlight":{"fields":{"text":{}}}}
    return client().search(index=settings.OPENSEARCH_INDEX, body=dsl)

def delete_document(doc_id: str):
    try:
        client().delete(index=settings.OPENSEARCH_INDEX, id=doc_id, ignore=[404])
    except NotFoundError:
        return
    except Exception:
        logger.exception("Failed to delete document %s from OpenSearch", doc_id)
