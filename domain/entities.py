from dataclasses import dataclass
from typing import List, Dict, Any, Optional

@dataclass
class RetrievedContext:
    text: str
    metadata: Dict[str, Any]
    similarity_score: float

@dataclass
class AgentResponse:
    question: str
    answer: str

    sources_used: List[RetrievedContext]
@dataclass
class KnowledgeDocument:
    """A pure domain entity representing a chunk of knowledge."""
    id: str
    text: str
    subreddit: str
    upvote_score: int
    content_flags: List[str]
    vector: Optional[List[float]] = None