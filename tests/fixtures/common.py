from datetime import datetime

from pydantic import BaseModel

from xsdata_pydantic.fields import field


class TypeA(BaseModel):
    one: str
    two: float


class TypeB(TypeA):
    one: str
    three: bool = field(default=True)


class TypeC(TypeB):
    four: list[datetime] = field(default_factory=list, metadata={"format": "%d %B %Y %H:%M"})
    any: object | None = field(default=None, metadata={"type": "Wildcard"})
