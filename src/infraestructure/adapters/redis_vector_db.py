import redis
import numpy as np
from typing import List
from redis.commands.search.field import TextField, VectorField, TagField, NumericField
from redis.commands.search.index_definition import IndexDefinition, IndexType
from redis.commands.search.query import Query
from src.domain.entities import KnowledgeDocument, RetrievedContext
from src.application.ports.output import VectorDatabaseRepo


class RedisVectorAdapter(VectorDatabaseRepo):
    def __init__(self, connection_string: str, index_name: str, prefix_name: str):
        self.client = redis.Redis.from_url(connection_string, decode_responses=False)
        self.index_name = index_name
        self.prefix_name = prefix_name
        self._ensure_index_exists()
        
    def _ensure_index_exists(self):
        schema = (
            TextField("text"),
            TagField("subreddit"),
            NumericField("upvote_score"),
            TagField("content_flags", separator=","),
            VectorField("vector", "HNSW", {"TYPE": "FLOAT32", "DIM": 1536, "DISTANCE_METRIC": "COSINE"})
        )
        try:
            self.client.ft(self.index_name).info()
        except redis.exceptions.ResponseError:
            self.client.ft(self.index_name).create_index(
                fields=schema,
                definition=IndexDefinition(prefix=[self.prefix_name], index_type=IndexType.HASH)
            )
    
    def add_text_database(self, document: List[KnowledgeDocument])-> None:
        vector_bytes = np.array(document.vector, dtype=np.float32).tobytes()
        
        flags_str = ",".join(document.content_flags)

        mapping = {
            "text": document.text.encode('utf-8'),
            "subreddit": document.subreddit.encode('utf-8'),
            "upvote_score": document.upvote_score,
            "content_flags": flags_str.encode('utf-8'),
            "vector": vector_bytes
        }

        self.client.hset(f"{self.prefix_name}:{document.id}", mapping=mapping)


    def search_by_vector(self, vector: List[float], subreddit: str) -> List[RetrievedContext]:
        """Translates Redis results back to Domain Entities."""
        vector_bytes = np.array(vector, dtype=np.float32).tobytes()
        
        query = (
            Query(f"(@subreddit:{{{subreddit}}})=>[KNN 3 @vector $query_vector]")
            .return_fields("text", "subreddit", "upvote_score", "content_flags")
            .dialect(2)
        )

        results = self.client.ft(self.index_name).search(query, query_params={"query_vector": vector_bytes})
        
    
        domain_docs = []
        for doc in results.docs:
            domain_docs.append(
                KnowledgeDocument(
                    id=doc.id.replace("doc:", ""),
                    text=doc.text,
                    subreddit=doc.subreddit,
                    upvote_score=int(doc.upvote_score),
                    content_flags=doc.content_flags.split(","),
                    vector=None
                )
            )
        return domain_docs