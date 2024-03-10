from decimal import Decimal
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field
from xsdata.models.datatype import XmlDate

__NAMESPACE__ = "foo"


class Usaddress(BaseModel):
    class Meta:
        name = "USAddress"

    model_config = ConfigDict(defer_build=True)
    name: str = Field(
        json_schema_extra={
            "type": "Element",
            "namespace": "foo",
            "required": True,
        }
    )
    street: str = Field(
        json_schema_extra={
            "type": "Element",
            "namespace": "foo",
            "required": True,
        }
    )
    city: str = Field(
        json_schema_extra={
            "type": "Element",
            "namespace": "foo",
            "required": True,
        }
    )
    state: str = Field(
        json_schema_extra={
            "type": "Element",
            "namespace": "foo",
            "required": True,
        }
    )
    zip: Decimal = Field(
        json_schema_extra={
            "type": "Element",
            "namespace": "foo",
            "required": True,
        }
    )
    country: str = Field(
        init=False,
        default="US",
        json_schema_extra={
            "type": "Attribute",
        },
    )


class Comment(BaseModel):
    class Meta:
        name = "comment"
        namespace = "foo"

    model_config = ConfigDict(defer_build=True)
    value: str = Field(
        default="",
        json_schema_extra={
            "required": True,
        },
    )


class Items(BaseModel):
    model_config = ConfigDict(defer_build=True)
    item: List["Items.Item"] = Field(
        default_factory=list,
        json_schema_extra={
            "type": "Element",
            "namespace": "foo",
        },
    )

    class Item(BaseModel):
        model_config = ConfigDict(defer_build=True)
        product_name: str = Field(
            json_schema_extra={
                "name": "productName",
                "type": "Element",
                "namespace": "foo",
                "required": True,
            }
        )
        quantity: int = Field(
            json_schema_extra={
                "type": "Element",
                "namespace": "foo",
                "required": True,
                "max_exclusive": 100,
            }
        )
        usprice: Decimal = Field(
            json_schema_extra={
                "name": "USPrice",
                "type": "Element",
                "namespace": "foo",
                "required": True,
            }
        )
        comment: Optional[Comment] = Field(
            default=None,
            json_schema_extra={
                "type": "Element",
                "namespace": "foo",
            },
        )
        ship_date: Optional[XmlDate] = Field(
            default=None,
            json_schema_extra={
                "name": "shipDate",
                "type": "Element",
                "namespace": "foo",
            },
        )
        part_num: str = Field(
            json_schema_extra={
                "name": "partNum",
                "type": "Attribute",
                "required": True,
                "pattern": r"\d{3}-[A-Z]{2}",
            }
        )


class PurchaseOrderType(BaseModel):
    model_config = ConfigDict(defer_build=True)
    ship_to: Usaddress = Field(
        json_schema_extra={
            "name": "shipTo",
            "type": "Element",
            "namespace": "foo",
            "required": True,
        }
    )
    bill_to: Usaddress = Field(
        json_schema_extra={
            "name": "billTo",
            "type": "Element",
            "namespace": "foo",
            "required": True,
        }
    )
    comment: Optional[Comment] = Field(
        default=None,
        json_schema_extra={
            "type": "Element",
            "namespace": "foo",
        },
    )
    items: Items = Field(
        json_schema_extra={
            "type": "Element",
            "namespace": "foo",
            "required": True,
        }
    )
    order_date: Optional[XmlDate] = Field(
        default=None,
        json_schema_extra={
            "name": "orderDate",
            "type": "Attribute",
        },
    )


class PurchaseOrder(PurchaseOrderType):
    class Meta:
        name = "purchaseOrder"
        namespace = "foo"

    model_config = ConfigDict(defer_build=True)
