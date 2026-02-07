from decimal import Decimal
from northstar.promotions import EmployeeDiscount, BOGO, checkout
from northstar.store import FlagshipStore
from northstar.basket import Basket

def test_promotions_pipeline():
    b = Basket(); b.add_line('TEE', 2, Decimal('10.00'))
    promos = [BOGO('TEE'), EmployeeDiscount(Decimal('0.10'))]
    fs = FlagshipStore(store_id='F2', name='Main')
    total_emp = checkout(fs, b, promos, customer_id='EMP007')
    total_guest = checkout(fs, b, promos, customer_id='GUEST')
    assert total_emp == Decimal('18.00')
    assert total_guest == Decimal('20.00')
