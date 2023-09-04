from dataclasses import field
from datetime import datetime
from typing import List, Optional

from pydantic.dataclasses import dataclass
from pydantic import BaseModel
from pydantic import Field



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


class BTypeA(BaseModel):
    one: str
    two: float
    
class BTypeB(BTypeA):
    one: str
    three: bool = Field(default=True)

class BTypeC(BTypeB):
    four: List[datetime] = Field(default_factory=list, metadata={"format": "%d %B %Y %H:%M"})
    any: Optional[object] = Field(default=None, metadata={"type": "Wildcard"})
