from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel

from xsdata_pydantic.fields import field


class TypeA(BaseModel):
    one: str
    two: float


class TypeB(TypeA):
    one: str
    three: bool = field(default=True)


class TypeC(TypeB):
    four: List[datetime] = field(default_factory=list, metadata={"format": "%d %B %Y %H:%M"})
    any: Optional[object] = field(default=None, metadata={"type": "Wildcard"})
