from decimal import Decimal
from typing import List, Optional

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
            "required": True,
        }
    )
    street: str = field(
        metadata={
            "type": "Element",
            "namespace": "foo",
            "required": True,
        }
    )
    city: str = field(
        metadata={
            "type": "Element",
            "namespace": "foo",
            "required": True,
        }
    )
    state: str = field(
        metadata={
            "type": "Element",
            "namespace": "foo",
            "required": True,
        }
    )
    zip: Decimal = field(
        metadata={
            "type": "Element",
            "namespace": "foo",
            "required": True,
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
    value: str = field(
        default="",
        metadata={
            "required": True,
        },
    )


class Items(BaseModel):
    model_config = ConfigDict(defer_build=True)
    item: List["Items.Item"] = field(
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
                "required": True,
            }
        )
        quantity: int = field(
            metadata={
                "type": "Element",
                "namespace": "foo",
                "required": True,
                "max_exclusive": 100,
            }
        )
        usprice: Decimal = field(
            metadata={
                "name": "USPrice",
                "type": "Element",
                "namespace": "foo",
                "required": True,
            }
        )
        comment: Optional[Comment] = field(
            default=None,
            metadata={
                "type": "Element",
                "namespace": "foo",
            },
        )
        ship_date: Optional[XmlDate] = field(
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
                "required": True,
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
            "required": True,
        }
    )
    bill_to: Usaddress = field(
        metadata={
            "name": "billTo",
            "type": "Element",
            "namespace": "foo",
            "required": True,
        }
    )
    comment: Optional[Comment] = field(
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
            "required": True,
        }
    )
    order_date: Optional[XmlDate] = field(
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
