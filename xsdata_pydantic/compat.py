from dataclasses import field
from typing import Any
from typing import Dict
from typing import Generic
from typing import List
from typing import Optional
from typing import Type
from typing import TypeVar

from pydantic.dataclasses import dataclass
from xsdata.formats.dataclass.compat import Dataclasses
from xsdata.formats.dataclass.models.elements import XmlType

T = TypeVar("T", bound=object)


class Config:
    arbitrary_types_allowed = True


@dataclass(config=Config)
class AnyElement:
    """
    Generic model to bind xml document data to wildcard fields.

    :param qname: The element's qualified name
    :param text: The element's text content
    :param tail: The element's tail content
    :param children: The element's list of child elements.
    :param attributes: The element's key-value attribute mappings.
    """

    qname: Optional[str] = field(default=None)
    text: Optional[str] = field(default=None)
    tail: Optional[str] = field(default=None)
    children: List[object] = field(
        default_factory=list, metadata={"type": XmlType.WILDCARD}
    )
    attributes: Dict[str, str] = field(
        default_factory=dict, metadata={"type": XmlType.ATTRIBUTES}
    )


@dataclass(config=Config)
class DerivedElement(Generic[T]):
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
        result = super().is_model(obj)
        if result and hasattr(obj, "__processed__"):
            obj.__pydantic_model__.update_forward_refs()

        return result and hasattr(obj, "__processed__")
