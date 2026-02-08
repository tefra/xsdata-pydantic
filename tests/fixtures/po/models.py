from __future__ import annotations

from decimal import Decimal

from pydantic import BaseModel, ConfigDict
from xsdata.models.datatype import XmlDate

from xsdata_pydantic.fields import field

__NAMESPACE__ = "foo"


class Usaddress(BaseModel):
    class Meta:
        name = "USAddress"

    model_config = ConfigDict(defer_build=True)
    name: str = field(
        metadata={
            "type": "Element",
            "namespace": "foo",
        }
    )
    street: str = field(
        metadata={
            "type": "Element",
            "namespace": "foo",
        }
    )
    city: str = field(
        metadata={
            "type": "Element",
            "namespace": "foo",
        }
    )
    state: str = field(
        metadata={
            "type": "Element",
            "namespace": "foo",
        }
    )
    zip: Decimal = field(
        metadata={
            "type": "Element",
            "namespace": "foo",
        }
    )
    country: str = field(
        const=True,
        default="US",
        metadata={
            "type": "Attribute",
        },
    )


class Comment(BaseModel):
    class Meta:
        name = "comment"
        namespace = "foo"

    model_config = ConfigDict(defer_build=True)
    value: str = field(default="")


class Items(BaseModel):
    model_config = ConfigDict(defer_build=True)
    item: list[Items.Item] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "foo",
        },
    )

    class Item(BaseModel):
        model_config = ConfigDict(defer_build=True)
        product_name: str = field(
            metadata={
                "name": "productName",
                "type": "Element",
                "namespace": "foo",
            }
        )
        quantity: int = field(
            metadata={
                "type": "Element",
                "namespace": "foo",
                "max_exclusive": 100,
            }
        )
        usprice: Decimal = field(
            metadata={
                "name": "USPrice",
                "type": "Element",
                "namespace": "foo",
            }
        )
        comment: None | Comment = field(
            default=None,
            metadata={
                "type": "Element",
                "namespace": "foo",
            },
        )
        ship_date: None | XmlDate = field(
            default=None,
            metadata={
                "name": "shipDate",
                "type": "Element",
                "namespace": "foo",
            },
        )
        part_num: str = field(
            metadata={
                "name": "partNum",
                "type": "Attribute",
                "pattern": r"\d{3}-[A-Z]{2}",
            }
        )


class PurchaseOrderType(BaseModel):
    model_config = ConfigDict(defer_build=True)
    ship_to: Usaddress = field(
        metadata={
            "name": "shipTo",
            "type": "Element",
            "namespace": "foo",
        }
    )
    bill_to: Usaddress = field(
        metadata={
            "name": "billTo",
            "type": "Element",
            "namespace": "foo",
        }
    )
    comment: None | Comment = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "foo",
        },
    )
    items: Items = field(
        metadata={
            "type": "Element",
            "namespace": "foo",
        }
    )
    order_date: None | XmlDate = field(
        default=None,
        metadata={
            "name": "orderDate",
            "type": "Attribute",
        },
    )


class PurchaseOrder(PurchaseOrderType):
    class Meta:
        name = "purchaseOrder"
        namespace = "foo"

    model_config = ConfigDict(defer_build=True)
