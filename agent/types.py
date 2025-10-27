# agent/types.py
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Citation:
    title: str
    url: str

@dataclass
class LLMResponse:
    text: str
    citations: List[Citation]
    finish_reason: Optional[str] = None