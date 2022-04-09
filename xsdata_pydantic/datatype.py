import xml.etree.ElementTree
from typing import Any
from typing import Callable
from typing import Generator

from xsdata.models import datatype


class ValidatorMixin:
    @classmethod
    def __get_validators__(cls) -> Generator[Callable, None, None]:
        yield cls.validate

    @classmethod
    def validate(cls, value: Any) -> Any:
        if isinstance(value, cls):
            return value

        if isinstance(value, str):
            return getattr(cls, "from_string", cls)(value)  # type: ignore

        raise ValueError()


class XmlDate(datatype.XmlDate, ValidatorMixin):
    pass


class XmlDateTime(datatype.XmlDateTime, ValidatorMixin):
    pass


class XmlTime(datatype.XmlTime, ValidatorMixin):
    pass


class XmlDuration(datatype.XmlDuration, ValidatorMixin):
    pass


class XmlPeriod(datatype.XmlPeriod, ValidatorMixin):
    pass


class QName(xml.etree.ElementTree.QName, ValidatorMixin):
    pass
