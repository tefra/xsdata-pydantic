from dataclasses import MISSING
from typing import Any, NamedTuple
from typing import Callable
from typing import Dict
from typing import Generic
from typing import Iterator
from typing import List
from typing import Optional
from typing import Type
from typing import TypeVar
from xml.etree.ElementTree import QName

from pydantic import BaseModel
from pydantic import Field
from pydantic_core import core_schema
from pydantic_core import PydanticUndefined
from xsdata.formats.converter import converter
from xsdata.formats.dataclass.compat import class_types
from xsdata.formats.dataclass.compat import Dataclasses
from xsdata.formats.dataclass.models.elements import XmlType
from xsdata.models.datatype import XmlDate
from xsdata.models.datatype import XmlDateTime
from xsdata.models.datatype import XmlDuration
from xsdata.models.datatype import XmlPeriod
from xsdata.models.datatype import XmlTime

T = TypeVar("T", bound=object)
EMPTY_DICT: Dict = {}


class FieldInfo(NamedTuple):
    name: str
    init: bool
    metadata: Dict[Any, Any]
    default: Any
    default_factory: Any


class Config:
    arbitrary_types_allowed = True


class AnyElement(BaseModel):
    """
    Generic model to bind xml document data to wildcard fields.

    :param qname: The element's qualified name
    :param text: The element's text content
    :param tail: The element's tail content
    :param children: The element's list of child elements.
    :param attributes: The element's key-value attribute mappings.
    """

    qname: Optional[str] = Field(default=None)
    text: Optional[str] = Field(default=None)
    tail: Optional[str] = Field(default=None)
    children: List[object] = Field(
        default_factory=list, json_schema_extra={"type": XmlType.WILDCARD}
    )
    attributes: Dict[str, str] = Field(
        default_factory=dict, json_schema_extra={"type": XmlType.ATTRIBUTES}
    )


class DerivedElement(BaseModel, Generic[T]):
    """
    Generic model wrapper for type substituted elements.

    Example: eg. <b xsi:type="a">...</b>

    :param qname: The element's qualified name
    :param value: The wrapped value
    :param type: The real xsi:type
    """

    qname: str
    value: T
    type: Optional[str] = None


class Pydantic(Dataclasses):
    @property
    def any_element(self) -> Type:
        return AnyElement

    @property
    def derived_element(self) -> Type:
        return DerivedElement

    def is_model(self, obj: Any) -> bool:
        clazz = obj if isinstance(obj, type) else type(obj)

        return issubclass(clazz, BaseModel)

    def get_fields(self, obj: Any) -> Iterator[FieldInfo]:
        for name, info in obj.model_fields.items():
            yield FieldInfo(
                name=name,
                init=False if info.init_var is False else True,
                metadata=info.json_schema_extra or EMPTY_DICT,
                default=info.default
                if info.default is not PydanticUndefined
                else MISSING,
                default_factory=info.default_factory
                if info.default_factory
                else MISSING,
            )


class_types.register("pydantic", Pydantic())


def set_validator(data_type: Any):
    def validator(
        cls: Any,
        _source_type: Any,
        _handler: Callable[[Any], core_schema.CoreSchema],
    ) -> core_schema.CoreSchema:
        return core_schema.json_or_python_schema(
            json_schema=core_schema.no_info_plain_validator_function(
                converter.deserialize
            ),
            python_schema=core_schema.is_instance_schema(data_type),
            serialization=core_schema.plain_serializer_function_ser_schema(
                converter.serialize
            ),
        )

    setattr(data_type, "__get_pydantic_core_schema__", classmethod(validator))  # noqa


types = [XmlDate, XmlDateTime, XmlTime, XmlDuration, XmlPeriod, QName]
for tp in types:
    set_validator(tp)
