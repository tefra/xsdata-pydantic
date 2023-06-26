from dataclasses import MISSING
from dataclasses import Field
from dataclasses import field
from typing import Any
from typing import Tuple
from typing import cast

from pydantic import BaseModel
from pydantic.fields import Undefined
from pydantic.fields import ModelField
from xsdata.formats.dataclass.compat import class_types

from xsdata_pydantic.compat import Pydantic


def pydantic_field_to_dataclass_field(pydantic_field: ModelField) -> Field:
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

    dataclass_field: Field = field(
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


class PydanticBaseModel(Pydantic):
    def is_model(self, obj: Any) -> bool:
        clazz = obj if isinstance(obj, type) else type(obj)
        if issubclass(clazz, BaseModel):
            clazz.update_forward_refs()
            return True

        return False

    def get_fields(self, obj: Any) -> Tuple[Any, ...]:
        _fields = cast("BaseModel", obj).__fields__.values()
        return [pydantic_field_to_dataclass_field(field) for field in _fields]


class_types.register("pydantic_base_model", PydanticBaseModel())
