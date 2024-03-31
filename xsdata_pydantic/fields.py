from typing import Any, Dict, Optional, Callable

from pydantic import fields
from pydantic_core import PydanticUndefined


class FieldInfo(fields.FieldInfo):
    __slots__ = ("xsdata_metadata",)

    def __init__(self, metadata: Optional[Dict[str, Any]], **kwargs: Any):
        super().__init__(**kwargs)
        self.xsdata_metadata = metadata


def field(
    metadata: Optional[Dict[str, Any]] = None,
    *,
    default: Any = PydanticUndefined,
    default_factory: Optional[Callable[[], Any]] = PydanticUndefined,
    **kwargs: Any,
):
    return FieldInfo(
        metadata=metadata, default=default, default_factory=default_factory, **kwargs
    )
