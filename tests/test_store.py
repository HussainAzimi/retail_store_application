from decimal import Decimal
from northstar.store import Store, FlagshipStore, OutletEligible, PopUp, HolidayPopUp
from northstar.basket import Basket

class DummyBasket:
    def total(self): return Decimal('12.34')

def test_flagship_calls_super_and_adds_vip():
    fs = FlagshipStore(store_id='F1', name='Downtown')
    steps = fs.return_item('R-001', 'SKU1')
    assert steps[:2] == ['ID check', 'fraud screen']
    assert steps[-1] == 'VIP grace window'
    assert fs.sell(DummyBasket()) == Decimal('12.34')

def test_holiday_popup_mro_and_outlet_block():
    hp = HolidayPopUp(store_id='HP1', name='Holiday', lease_ends='2025-12-31')
    hp.mark_final_sale('SCARF')
    mro = [c.__name__ for c in HolidayPopUp.mro()[:4]]
    assert mro == ['HolidayPopUp','OutletEligible','PopUp','FlagshipStore']
    steps = hp.return_item('R-002','SCARF')
    assert steps[:2] == ['ID check', 'fraud screen']
    assert 'VIP grace window' in steps
    assert steps[-1].startswith('final sale'), steps
