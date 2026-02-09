from __future__ import annotations
from dataclasses import dataclass, field
from decimal import Decimal
from .basket import Basket

@dataclass(slots=True)
class Order:
    order_id: str
    channel: str
    basket: Basket
    total: Decimal = field(default=Decimal('0.00'))

    @classmethod
    def from_pos(cls, *, order_id: str, basket: Basket, cashier_id: str) -> 'Order':
        # TODO
        return cls(
            order_id = order_id,
            channel = "pos",
            basket = basket,
            total = basket.total()
        )

    @classmethod
    def from_web(cls, *, order_id: str, cart: Basket, user_id: str, address: str) -> 'Order':
        # TODO
        return cls(
            order_id = order_id,
            channel = "web",
            basket = cart,
            total = cart.total()
        )

    @classmethod
    def from_csv_row(cls, row: dict[str, str]) -> 'Order':
        """Parse row like {'order_id':'C001','channel':'csv','lines':'TEE:2:10.00;MUG:1:8.00'}"""
        # TODO
        try:
            order_id = row["order_id"].strip()

        except KeyError as e:
            raise ValueError(f"Missing required key in csv row: {e}")
        
        basket = Basket()
        lines_str = row.get("lines", "").strip()
        if lines_str:
            for part in lines_str.split(";"):
                part = part.strip()
                if not part:
                    continue

                try:

                    sku, qty_str, price_str = part.split(":")
                    sku = sku.strip()
                    qty = int(qty_str.strip())
                    price = Decimal(price_str.strip())
                except Exception as e:
                    raise ValueError(f"Malformed CSV line: {part!r}") from e
                
                basket.add_line(sku, qty, price)
        return cls(
            order_id = order_id,
            channel = "csv",
            basket = basket,
            total = basket.total()
        )

    
    def __repr__(self) -> str:
        return f"Order(id={self.order_id!r}, channel={self.channel!r}, lines={len(self.basket)}, total={self.total})"
