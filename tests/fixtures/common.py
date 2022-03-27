from dataclasses import field
from datetime import datetime
from typing import List, Optional

from pydantic.dataclasses import dataclass



@dataclass
class TypeA:
    one: str
    two: float


@dataclass
class TypeB(TypeA):
    one: str
    three: bool = field(default=True)


@dataclass
class TypeC(TypeB):
    four: List[datetime] = field(default_factory=list, metadata={"format": "%d %B %Y %H:%M"})
    any: Optional[object] = field(default=None, metadata={"type": "Wildcard"})
