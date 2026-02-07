from decimal import Decimal
from northstar.basket import Basket

def test_basket_add_and_total_and_guardrails():
    b = Basket()
    b.add_line('HAT', 2, Decimal('10.00'))
    b.add_line('SOCK', 3, Decimal('2.50'))
    assert len(b) == 2
    assert b.total() == Decimal('20.00') + Decimal('7.50')
    try:
        b[0] = ('BAD', 1, Decimal('1.00'))
        assert False, 'should not allow setitem'
    except TypeError:
        pass
