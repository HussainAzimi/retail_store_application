from __future__ import annotations
from abc import ABC, abstractmethod
from decimal import Decimal
from .basket import Basket
from .store import Store

class Promotion(ABC):
    @abstractmethod
    def eligible(self, customer_id: str) -> bool: ...
    @abstractmethod
    def apply(self, basket: Basket) -> Basket: ...

class EmployeeDiscount(Promotion):
    """Apply a percentage discount for employee IDs (start with 'EMP')."""
    def __init__(self, pct: Decimal):
        self.pct = pct
    def eligible(self, customer_id: str) -> bool:
        # TODO
        return customer_id.startswith("EMP")
        
    def apply(self, basket: Basket) -> Basket:
        # TODO: reduce price for priced lines by pct
        new_price = []
        for sku, qty, price in basket.data:
            if price > Decimal("0"):
                price = price * (Decimal("1") - self.pct)
            new_price.append((sku, qty, price))

        basket.data[:] = new_price

class BOGO(Promotion):
    """Buy-one-get-one for a single SKU: if >=2 in basket, add one free unit."""
    def __init__(self, sku: str):
        self.sku = sku
    def eligible(self, customer_id: str) -> bool:
        return True
    def apply(self, basket: Basket) -> Basket:
        # TODO: inspect basket; if sku qty>=2, add (sku, 1, Decimal('0.00'))
         total_qty = sum(qty for s, qty, _ in basket.data if s == self.sku)

         if total_qty >= 2:
             basket.add_line(self.sku, 1, Decimal("0.00"))    
         

def checkout(store: Store, basket: Basket, promos: list[Promotion], customer_id: str) -> Decimal:
    """Apply eligible promotions (polymorphic) then sell via store."""
    # TODO: loop promos with no isinstance chains
    for promo in promos:
        if promo.eligible(customer_id):
            promo.apply(basket)

    return store.sell(basket)


