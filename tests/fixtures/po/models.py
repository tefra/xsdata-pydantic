from dataclasses import field
from decimal import Decimal
from pydantic.dataclasses import dataclass
from typing import List, Optional
from xsdata.models.datatype import XmlDate

__NAMESPACE__ = "foo"


@dataclass(slots=True, kw_only=True)
class Items:
    item: List["Items.Item"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "foo",
        }
    )

    @dataclass(slots=True, kw_only=True)
    class Item:
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
        comment: Optional[str] = field(
            default=None,
            metadata={
                "type": "Element",
                "namespace": "foo",
            }
        )
        ship_date: Optional[XmlDate] = field(
            default=None,
            metadata={
                "name": "shipDate",
                "type": "Element",
                "namespace": "foo",
            }
        )
        part_num: str = field(
            metadata={
                "name": "partNum",
                "type": "Attribute",
                "required": True,
                "pattern": r"\d{3}-[A-Z]{2}",
            }
        )


@dataclass(slots=True, kw_only=True)
class Usaddress:
    class Meta:
        name = "USAddress"

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
        init=False,
        default="US",
        metadata={
            "type": "Attribute",
        }
    )


@dataclass(slots=True, kw_only=True)
class Comment:
    class Meta:
        name = "comment"
        namespace = "foo"

    value: str = field(
        default="",
        metadata={
            "required": True,
        }
    )


@dataclass(slots=True, kw_only=True)
class PurchaseOrderType:
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
    comment: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "foo",
        }
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
        }
    )


@dataclass(slots=True, kw_only=True)
class PurchaseOrder(PurchaseOrderType):
    class Meta:
        name = "purchaseOrder"
        namespace = "foo"
