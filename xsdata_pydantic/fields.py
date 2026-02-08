from collections.abc import Callable
from typing import Any

from pydantic import fields
from pydantic_core import PydanticUndefined


class FieldInfo(fields.FieldInfo):
    """Pydantic FieldInfo subclass carrying xsdata metadata."""

    __slots__ = ("xsdata_metadata",)

    def __init__(self, metadata: dict[str, Any] | None, **kwargs: Any):
        """Initialize with xsdata metadata and pydantic field kwargs."""
        super().__init__(**kwargs)
        self.xsdata_metadata = metadata


def field(
    metadata: dict[str, Any] | None = None,
    *,
    default: Any = PydanticUndefined,
    default_factory: Callable[[], Any] | None = PydanticUndefined,
    **kwargs: Any,
) -> Any:
    """Create a pydantic FieldInfo with optional xsdata metadata."""
    return FieldInfo(
        metadata=metadata, default=default, default_factory=default_factory, **kwargs
    )
