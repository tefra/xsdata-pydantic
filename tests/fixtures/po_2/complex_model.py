from typing import Any, Optional

from pydantic import BaseModel, ConfigDict

from xsdata_pydantic.fields import field


class Code(BaseModel):
    """
    :ivar code: In diesem XML-Element wird der Code einer Codeliste
        übermittelt.
    :ivar name:
    :ivar list_uri:
    :ivar list_version_id:
    """

    class Meta:
        target_namespace = "http://xoev.de/schemata/code/1_0"

    model_config = ConfigDict(defer_build=True)
    code: str = field(
        metadata={
            "type": "Element",
            "namespace": "",
            "required": True,
        }
    )
    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "",
        },
    )
    list_uri: Optional[str] = field(
        default=None,
        metadata={
            "name": "listURI",
            "type": "Attribute",
        },
    )
    list_version_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "listVersionID",
            "type": "Attribute",
        },
    )


class CodeFehlerTyp4(Code):
    class Meta:
        name = "Code.Fehler.Typ4"
        target_namespace = "http://www.xjustiz.de"

    model_config = ConfigDict(defer_build=True)
    name: Any = field(
        exclude=True,
        default=None,
        metadata={
            "type": "Ignore",
        },
    )
    list_uri: str = field(
        metadata={
            "name": "listURI",
            "type": "Attribute",
            "required": True,
        }
    )
    list_version_id: str = field(
        metadata={
            "name": "listVersionID",
            "type": "Attribute",
            "required": True,
        }
    )
