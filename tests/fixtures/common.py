from dataclasses import field
from datetime import datetime
from typing import List

from pydantic.dataclasses import dataclass


class Config:
    arbitrary_types_allowed = True


@dataclass(config=Config)
class TypeA:
    one: str
    two: float


@dataclass(config=Config)
class TypeB(TypeA):
    one: str
    three: bool = field(default=True)


@dataclass(config=Config)
class TypeC(TypeB):
    four: List[datetime] = field(default_factory=list, metadata={"format": "%d %B %Y %H:%M"})
    any: object = field(default_factory=None, metadata={"type": "Wildcard"})
