from dataclasses import MISSING
from dataclasses import field
from typing import Any
from typing import Dict
from typing import Generic
from typing import Optional
from typing import List
from typing import Tuple
from typing import Type
from typing import TypeVar
from typing import cast

from pydantic import BaseModel
from pydantic.fields import Undefined
from pydantic.fields import ModelField
from pydantic.fields import Field
from xsdata.formats.dataclass.compat import class_types
from xsdata.formats.dataclass.compat import Dataclasses
from xsdata.formats.dataclass.models.elements import XmlType


T = TypeVar("T", bound=object)


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
        default_factory=list, metadata={"type": XmlType.WILDCARD}
    )
    attributes: Dict[str, str] = Field(
        default_factory=dict, metadata={"type": XmlType.ATTRIBUTES}
    )

    class Config:
        arbitrary_types_allowed = True


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

    class Config:
        arbitrary_types_allowed = True


class PydanticBaseModel(Dataclasses):
    @property
    def any_element(self) -> Type:
        return AnyElement

    @property
    def derived_element(self) -> Type:
        return DerivedElement

    def is_model(self, obj: Any) -> bool:
        clazz = obj if isinstance(obj, type) else type(obj)
        if issubclass(clazz, BaseModel):
            clazz.update_forward_refs()
            return True

        return False

    def get_fields(self, obj: Any) -> Tuple[Any, ...]:
        _fields = cast("BaseModel", obj).__fields__.values()
        return tuple(_pydantic_field_to_dataclass_field(field) for field in _fields)


def _pydantic_field_to_dataclass_field(pydantic_field: ModelField) -> Any:
    if pydantic_field.default_factory is not None:
        default_factory: Any = pydantic_field.default_factory
        default = MISSING
    else:
        default_factory = MISSING
        default = (
            MISSING
            if pydantic_field.default in (Undefined, Ellipsis)
            else pydantic_field.default
        )

    dataclass_field = field(  # type: ignore
        default=default,
        default_factory=default_factory,
        # init=True,
        # hash=None,
        # compare=True,
        metadata=pydantic_field.field_info.extra.get("metadata", {}),
        kw_only=MISSING,
    )
    dataclass_field.name = pydantic_field.name
    dataclass_field.type = pydantic_field.type_
    return dataclass_field


class_types.register("pydantic-base-model", PydanticBaseModel())
