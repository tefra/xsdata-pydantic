from decimal import Decimal
from typing import List, Optional

from pydantic_xml import BaseXmlModel, attr, element
from xsdata.models.datatype import XmlDate

from xsdata_pydantic.fields import field

__NAMESPACE__ = "foo"


class Usaddress(BaseXmlModel):
    class Meta:
        name = "USAddress"

    name: str = element(
        tag="name",
        ns="foo",
    )
    street: str = element(
        tag="street",
        ns="foo",
    )
    city: str = element(
        tag="city",
        ns="foo",
    )
    state: str = element(
        tag="state",
        ns="foo",
    )
    zip: Decimal = element(
        tag="zip",
        ns="foo",
    )
    country: str = attr(
        name="country",
        ns="foo",
        default="US",
    )


class Comment(BaseXmlModel):
    class Meta:
        name = "comment"
        namespace = "foo"

    value: str = attr(
        name="value",
        default="",
    )


class Items(BaseXmlModel):
    item: List["Items.Item"] = element(
        tag="item",
        ns="foo",
        default_factory=list,
    )

    class Item(BaseModel):
        product_name: str = element(
            tag="productName",
            ns="foo",
        )
        quantity: int = element(
            tag="quantity",
            ns="foo",
            max_exclusive=100,
        )
        usprice: Decimal = element(
            tag="USPrice",
            ns="foo",
        )
        comment: Optional[Comment] = element(
            tag="comment",
            ns="foo",
            default=None,
        )
        ship_date: Optional[XmlDate] = element(
            tag="shipDate",
            ns="foo",
            default=None,
        )
        part_num: str = attr(
            name="partNum",
            pattern= r"\d{3}-[A-Z]{2}",
        )


class PurchaseOrderType(BaseModel):
    ship_to: Usaddress = element(
        tag="shipTo",
        ns="foo",
    )
    bill_to: Usaddress = element(
        tag="billTo",
        ns="foo",
    )
    comment: Optional[Comment] = element(
        tag="comment",
        ns="foo",
        default=None,
    )
    items: Items = element(
        tag="items",
        ns="foo",
    )
    order_date: Optional[XmlDate] = attr(
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
