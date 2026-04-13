from dataclasses import dataclass
from typing import List, Dict, Any

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