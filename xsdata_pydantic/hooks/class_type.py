from xsdata.formats.converter import converter
from xsdata.formats.converter import ProxyConverter
from xsdata.formats.dataclass.compat import class_types

from xsdata_pydantic.compat import Pydantic
from xsdata_pydantic.datatype import XmlDate
from xsdata_pydantic.datatype import XmlDateTime
from xsdata_pydantic.datatype import XmlDuration
from xsdata_pydantic.datatype import XmlPeriod
from xsdata_pydantic.datatype import XmlTime

class_types.register("pydantic", Pydantic())

converter.register_converter(XmlTime, ProxyConverter(XmlTime.from_string))
converter.register_converter(XmlDate, ProxyConverter(XmlDate.from_string))
converter.register_converter(XmlDateTime, ProxyConverter(XmlDateTime.from_string))
converter.register_converter(XmlDuration, ProxyConverter(XmlDuration))
converter.register_converter(XmlPeriod, ProxyConverter(XmlPeriod))
