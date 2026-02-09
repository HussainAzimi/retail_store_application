from decimal import Decimal
from northstar.order import Order
from northstar.basket import Basket

def test_order_constructors():
    b = Basket(); b.add_line('CAP', 1, Decimal('15.00'))
    o1 = Order.from_pos(order_id='P001', basket=b, cashier_id='C9')
    assert o1.channel == 'pos' and o1.total == Decimal('15.00')
    o2 = Order.from_web(order_id='W001', cart=b, user_id='U1', address='123 Main')
    assert o2.channel == 'web' and o2.total == Decimal('15.00')
    row = {'order_id':'C001', 'channel':'csv', 'lines':'TEE:2:10.00;MUG:1:8.00'}
    o3 = Order.from_csv_row(row)
    assert o3.total == Decimal('28.00')

    # Test CSV channel empty lines

def test_csv_empty_lines():

    row = {'order_id':'C003', 'channel':'csv', 'lines':'TTEE:1:10.00;; ;MUG:2:5.00'}
    o1 = Order.from_csv_row(row)
    assert len(o1.basket) == 2
    assert o1.total == Decimal('20.00')