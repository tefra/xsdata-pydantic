from dataclasses import field
from dataclasses import is_dataclass
from typing import Any
from typing import Callable
from typing import Dict
from typing import Generic
from typing import List
from typing import Optional
from typing import Type
from typing import TypeVar
from xml.etree.ElementTree import QName

from pydantic.dataclasses import dataclass
from pydantic.validators import _VALIDATORS
from xsdata.formats.dataclass.compat import class_types
from xsdata.formats.dataclass.compat import Dataclasses
from xsdata.formats.dataclass.models.elements import XmlType
from xsdata.models.datatype import XmlDate
from xsdata.models.datatype import XmlDateTime
from xsdata.models.datatype import XmlDuration
from xsdata.models.datatype import XmlPeriod
from xsdata.models.datatype import XmlTime


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
        clazz = obj if isinstance(obj, type) else type(obj)
        if is_dataclass(clazz) and hasattr(clazz, "__pydantic_model__"):
            clazz.__pydantic_model__.update_forward_refs()  # type: ignore
            return True

        return False


class_types.register("pydantic", Pydantic())


def make_validators(tp: Type, factory: Callable) -> List[Callable]:
    def validator(value: Any) -> Any:

        if isinstance(value, tp):
            return value

        if isinstance(value, str):
            return factory(value)

        raise ValueError

    return [validator]


_VALIDATORS.extend(
    [
        (XmlDate, make_validators(XmlDate, XmlDate.from_string)),
        (XmlDateTime, make_validators(XmlDateTime, XmlDateTime.from_string)),
        (XmlTime, make_validators(XmlTime, XmlTime.from_string)),
        (XmlDuration, make_validators(XmlDuration, XmlDuration)),
        (XmlPeriod, make_validators(XmlPeriod, XmlPeriod)),
        (QName, make_validators(QName, QName)),
    ]
)
