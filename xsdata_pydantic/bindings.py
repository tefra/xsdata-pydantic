from dataclasses import dataclass
from dataclasses import field
from typing import Callable, Optional

from xsdata.formats.dataclass import context
from xsdata.formats.dataclass import parsers
from xsdata.formats.dataclass import serializers
from xsdata.utils.constants import return_input


class XmlContext(context.XmlContext):
    """The models context class.

    The context is responsible to provide binding metadata
    for models and their fields.

    Args:
        element_name_generator: Default element name generator
        attribute_name_generator: Default attribute name generator
        models_package: Restrict auto locate to a specific package

    Attributes:
        cache: Internal cache for binding metadata instances
        xsi_cache: Internal cache for xsi types to class locations
        sys_modules: The number of loaded sys modules
    """

    def __init__(
        self,
        element_name_generator: Callable = return_input,
        attribute_name_generator: Callable = return_input,
        models_package: Optional[str] = None,
    ):
        super().__init__(
            element_name_generator, attribute_name_generator, "pydantic", models_package
        )


@dataclass
class XmlParser(parsers.XmlParser):
    """Default Xml parser for attrs.

    Args:
        config: The parser config instance
        context: The xml context instance
        handler: The xml handler class

    Attributes:
        ns_map: The parsed namespace prefix-URI map
    """

    context: XmlContext = field(default_factory=XmlContext)


@dataclass
class XmlSerializer(serializers.XmlSerializer):
    """Xml serializer for attrs.

    Args:
        config: The serializer config instance
        context: The models context instance
        writer: The xml writer class
    """

    context: XmlContext = field(default_factory=XmlContext)


@dataclass
class JsonParser(parsers.JsonParser):
    """Json parser for attrs.

    Args:
        config: Parser configuration
        context: The models context instance
        load_factory: Json loader factory
    """

    context: XmlContext = field(default_factory=XmlContext)


@dataclass
class DictDecoder(parsers.DictDecoder):
    """Bind a dictionary or a list of dictionaries to attrs.

    Args:
        config: Parser configuration
        context: The models context instance
    """

    context: XmlContext = field(default_factory=XmlContext)


@dataclass
class DictEncoder(serializers.DictEncoder):
    """Bind a dictionary or a list of dictionaries to attrs.

    Args:
        config: Parser configuration
        context: The models context instance
    """

    context: XmlContext = field(default_factory=XmlContext)


@dataclass
class JsonSerializer(serializers.JsonSerializer):
    """Json serializer for attrs.

    Args:
        config: The serializer config instance
        context: The models context instance
        dict_factory: Dictionary factory
        dump_factory: Json dump factory e.g. json.dump
    """

    context: XmlContext = field(default_factory=XmlContext)


@dataclass
class UserXmlParser(parsers.UserXmlParser):
    """Xml parser for attrs with hooks to events.

    The event hooks allow custom parsers to inject custom
    logic between the start/end element events.

    Args:
        config: The parser config instance
        context: The xml context instance
        handler: The xml handler class

    Attributes:
        ns_map: The parsed namespace prefix-URI map
        hooks_cache: The hooks cache is used to avoid
            inspecting the class for custom methods
            on duplicate events.
    """

    context: XmlContext = field(default_factory=XmlContext)


@dataclass
class TreeParser(parsers.TreeParser):
    """Bind xml nodes to a tree of AnyElement objects."""

    context: XmlContext = field(default_factory=XmlContext)


@dataclass
class PycodeSerializer(serializers.PycodeSerializer):
    """Pycode serializer for data class instances.

    Generate python pretty representation code from a model instance.

    Args:
        context: The models context instance
    """

    context: XmlContext = field(default_factory=XmlContext)
