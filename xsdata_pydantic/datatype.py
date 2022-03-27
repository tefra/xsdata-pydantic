from typing import Union

from xsdata.models import datatype


class XmlDate(datatype.XmlDate):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, value: Union[str, "XmlDate"]) -> "XmlDate":
        if isinstance(value, cls):
            return value

        return cls.from_string(value)


class XmlDateTime(datatype.XmlDateTime):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, value: Union[str, "XmlDateTime"]) -> "XmlDateTime":
        if isinstance(value, cls):
            return value

        return cls.from_string(value)


class XmlTime(datatype.XmlTime):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, value: Union[str, "XmlTime"]) -> "XmlTime":
        if isinstance(value, cls):
            return value

        return cls.from_string(value)


class XmlDuration(datatype.XmlDuration):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, value: Union[str, "XmlDuration"]) -> "XmlDuration":
        if isinstance(value, cls):
            return value

        return cls(value)


class XmlPeriod(datatype.XmlPeriod):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, value: Union[str, "XmlPeriod"]) -> "XmlPeriod":
        if isinstance(value, cls):
            return value

        return cls(value)
