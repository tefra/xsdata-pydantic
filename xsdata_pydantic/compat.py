from collections.abc import Callable, Iterator
from dataclasses import MISSING
from typing import (
    Any,
    Generic,
    NamedTuple,
    TypeVar,
)
from xml.etree.ElementTree import QName

from pydantic import BaseModel
from pydantic_core import PydanticUndefined, core_schema
from xsdata.formats.converter import converter
from xsdata.formats.dataclass.compat import Dataclasses
from xsdata.formats.dataclass.models.elements import XmlType
from xsdata.models.datatype import XmlDate, XmlDateTime, XmlDuration, XmlPeriod, XmlTime

from xsdata_pydantic.fields import field

T = TypeVar("T", bound=object)
EMPTY_DICT: dict = {}


class FieldInfo(NamedTuple):
    """A wrapper for pydantic model field information."""

    name: str
    init: bool
    metadata: dict[Any, Any]
    default: Any
    default_factory: Any


class AnyElement(BaseModel):
    """Generic model to bind xml document data to wildcard fields.

    :param qname: The element's qualified name
    :param text: The element's text content
    :param tail: The element's tail content
    :param children: The element's list of child elements.
    :param attributes: The element's key-value attribute mappings.
    """

    qname: str | None = field(default=None)
    text: str | None = field(default=None)
    tail: str | None = field(default=None)
    children: list[object] = field(
        default_factory=list, metadata={"type": XmlType.WILDCARD}
    )
    attributes: dict[str, str] = field(
        default_factory=dict, metadata={"type": XmlType.ATTRIBUTES}
    )


class DerivedElement(BaseModel, Generic[T]):
    """Generic model wrapper for type substituted elements.

    Example: eg. <b xsi:type="a">...</b>

    :param qname: The element's qualified name
    :param value: The wrapped value
    :param type: The real xsi:type
    """

    qname: str
    value: T
    type: str | None = None


class Pydantic(Dataclasses):
    """Pydantic class type for xsdata."""

    @property
    def any_element(self) -> type:
        """Return the AnyElement class."""
        return AnyElement

    @property
    def derived_element(self) -> type:
        """Return the DerivedElement class."""
        return DerivedElement

    def is_model(self, obj: Any) -> bool:
        """Return whether the given value is a pydantic model."""
        clazz = obj if isinstance(obj, type) else type(obj)
        return issubclass(clazz, BaseModel)

    def verify_model(self, obj: Any) -> None:
        """Verify the given value is a pydantic model."""
        if not self.is_model(obj):
            from xsdata.exceptions import XmlContextError

            raise XmlContextError(f"Type '{obj}' is not a pydantic model.")

    def get_fields(self, obj: Any) -> Iterator[FieldInfo]:
        """Return the model's fields as FieldInfo instances."""
        clazz = obj if isinstance(obj, type) else type(obj)
        for name, info in clazz.model_fields.items():
            metadata = getattr(info, "xsdata_metadata", None) or EMPTY_DICT

            yield FieldInfo(
                name=name,
                init=info.init_var is not False,
                metadata=metadata,
                default=info.default
                if info.default is not PydanticUndefined
                else MISSING,
                default_factory=info.default_factory
                if info.default_factory
                else MISSING,
            )


def set_validator(data_type: Any) -> None:
    """Monkey-patch __get_pydantic_core_schema__ onto an xsdata type."""

    def validator(
        cls: Any,
        _source_type: Any,
        _handler: Callable[[Any], core_schema.CoreSchema],
    ) -> core_schema.CoreSchema:
        conv = converter.type_converter(data_type)
        return core_schema.json_or_python_schema(
            json_schema=core_schema.no_info_plain_validator_function(conv.deserialize),
            python_schema=core_schema.is_instance_schema(data_type),
            serialization=core_schema.plain_serializer_function_ser_schema(
                conv.serialize
            ),
        )

    setattr(data_type, "__get_pydantic_core_schema__", classmethod(validator))  # noqa


types = [XmlDate, XmlDateTime, XmlTime, XmlDuration, XmlPeriod, QName]
for tp in types:
    set_validator(tp)
