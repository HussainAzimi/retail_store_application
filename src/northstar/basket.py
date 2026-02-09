from __future__ import annotations
from collections import UserList
from decimal import Decimal

class Basket(UserList):
    """A list-like cart with guardrails.

    Only add via add_line(sku, qty, price). Uses Decimal for money.

    >>> b = Basket(); b.add_line('TEE', 2, Decimal('10.00')); b.total()
    Decimal('20.00')
    """
    def add_line(self, sku: str, qty: int, price: Decimal) -> None:
        # TODO: validate sku non-empty, qty>0, price>=0 then append tuple
        if not isinstance(sku, str) or not sku:
            raise ValueError("sku must be a non-empty string")
        
        if not isinstance(qty, int) or qty <= 0:
            raise ValueError("Quantity must be an integer greater than 0")
        
        if not isinstance(price, Decimal) or price < Decimal("0"):
            raise ValueError("Price must be a Decimal greater than 0 ")
        
        self.data.append((sku, qty, price))


    def total(self) -> Decimal:
        # TODO: sum qty*price as Decimal
        total = Decimal("0.00")
        for _, qty, price in self.data:
            total += price * qty

        return total

    def __setitem__(self, i, item):
        raise TypeError('use add_line()')

    def insert(self, i, item):
        raise TypeError('use add_line()')
