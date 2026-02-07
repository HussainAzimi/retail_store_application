
# PA3 Student Guide — When Objects Are Alike (Inheritance & Polymorphism)

**Course:** Foundations of OOP in Python  
**Assignment Window:** 1 week (suggested) — *Instructor sets exact dates*  
**Time Budget:** 3–5 hours (typical)  
**Environment:** Python 3.10+; `pytest` recommended

---

## What You Will Build
A tiny **NorthStar Retail** domain that demonstrates safe inheritance, cooperative `super()`, multiple inheritance with C3 MRO, mixins, polymorphism, and diagnostics.

Your code lives in `src/northstar/` (fill in the TODOs). **Do not** change test expectations.

---

## Step‑by‑Step Checklist (with Acceptance Criteria)

### 1) Corporate contract + simple override
**Files:** `store.py`  
- Implement `Store.return_item(...)` to return **exactly** `["ID check", "fraud screen"]`.  
  - *Acceptance:* `FlagshipStore` tests expect these as the **first two steps**, in this order.
- Implement `FlagshipStore.return_item(...)` to call `super().return_item(...)` **first**, then append `"VIP grace window"`.  
  - *Acceptance:* The final list ends with `"VIP grace window"`.

**Why:** Practice LSP and cooperative overrides (no skipping corporate logic).

---

### 2) Guardrailed Basket (extend built‑ins safely)
**Files:** `basket.py`  
- Base the class on `collections.UserList` (already done for you).
- Implement `add_line(sku, qty, price)` with validations:  
  - `sku` nonempty `str`, `qty` > 0 (int), `price` ≥ 0 (`Decimal`).  
  - Append a tuple `(sku, qty, price)` on success; raise `ValueError` on invalid input.
- Implement `total()` that returns a `Decimal` sum of `qty * price` across lines.  
- Forbid direct mutation: `__setitem__` and `insert` already raise `TypeError`. Keep it.

**Acceptance:** `test_basket.py` passes; doctest in docstring may help verify.

**Tip:** Use `Decimal("0.00")` as the summation start to avoid float drift.

---

### 3) Capabilities via MI: `OutletEligible` + `PopUp` → `HolidayPopUp`
**Files:** `store.py`  
- `OutletEligible.__init__` and `PopUp.__init__` already call `super()`; keep cooperating.
- `OutletEligible.return_item(...)` must call `super()` *then* append `"final sale — blocked"` if SKU is in `final_sale_skus`.
- `PopUp.open_doors(...)` calls `super()` (you can leave as no‑op or add a comment).
- `HolidayPopUp(OutletEligible, PopUp, FlagshipStore)` relies on **C3 MRO**; do not hard‑wire parent names.

**Acceptance:** `test_store.py::test_holiday_popup_mro_and_outlet_block` enforces MRO and step ordering.

**Gotcha:** Hard‑calling `Base.return_item(self, ...)` breaks the chain in MI. Always use `super()`.

---

### 4) Mixins: `Auditable` and `Cacheable`
**Files:** (You won’t edit these classes in the assignment starter; you will **use** them in the lab.)
- If you extend later: keep mixins small and call `super().__init__`.
- To make an LRU cache key from a `Basket`, turn each line into **hashable** pieces:  
  - **Recommended snapshot:** `tuple((sku, int(qty), str(price)) for sku, qty, price in basket.data)`  
  - Rationale: `Decimal` is hashable in modern Python, but `str(price)` avoids context surprises.

**Acceptance:** In the guided lab, the “mixins check” validates this idea; PA tests don’t require mixins.

---

### 5) Promotions & Polymorphic Checkout
**Files:** `promotions.py`  
- Implement `EmployeeDiscount(pct)`:
  - `eligible(customer_id)` returns `True` iff `customer_id.startswith("EMP")`.
  - `apply(basket)` reduces the *price* of each **priced** line by `pct` (`new_price = price * (1 - pct)`).  
    Leave free items (`price == 0`) unchanged. Mutating in place is fine.
- Implement `BOGO(sku)`:
  - If basket contains **2 or more** of `sku`, `apply` should add a **free** line `(sku, 1, Decimal("0.00"))`.  
  - If fewer than 2, do nothing.
- Implement `checkout(store, basket, promos, customer_id)`:
  - Iterate **in the given order** of `promos`. For each promo: if `eligible`, call `apply`.  
  - After all promos, return `store.sell(basket)`.

**Acceptance:** `test_promos.py` expects:
- With `promos=[BOGO("TEE"), EmployeeDiscount(Decimal("0.10"))]` and 2 TEE @$10 each:  
  - **EMP** customer: BOGO first ⇒ 3 TEE with one free. Then 10% off priced lines ⇒ `$20 * 0.9 = 18.00`.  
  - **GUEST**: only BOGO applies ⇒ `$20.00`.
- Any branching on concrete types in `checkout` (e.g., `isinstance`) is a design smell—don’t do it.

---

### 6) Distance Strategies (analytics polymorphism)
**Files:** `distance.py`  
- Implement `Distance` ABC: `between(a, b) -> float`, where `a`, `b` are `(x, y)` (or lat/lon for GC).
- `Euclidean`: `sqrt((ax - bx)**2 + (ay - by)**2)`
- `Manhattan`: `abs(ax - bx) + abs(ay - by)`
- `GreatCircle`: treat points as `(lat, lon)` in **degrees**. Use haversine:
  - `R = 6371.0088` km  
  - Convert degrees→radians, then:
    ```
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    h = sin(dlat/2)**2 + cos(lat1)*cos(lat2)*sin(dlon/2)**2
    d = 2*R*asin(h**0.5)
    ```

**Acceptance:** `test_distance.py` checks exact Euclidean/Manhattan values and GC within range (≈111.32 km per degree of lon at equator).

---

### 7) Orders with alternate constructors
**Files:** `order.py`  
- Implement:
  - `Order.from_pos(order_id, basket, cashier_id)` → channel `"pos"`.
  - `Order.from_web(order_id, cart, user_id, address)` → channel `"web"`.
  - `Order.from_csv_row(row)` where `row = {"order_id": "...", "channel": "csv", "lines": "SKU1:2:10.00;SKU2:1:5.00"}`.  
    - Parse safely, trim whitespace, validate qty/price.  
    - Build a **new** Basket and compute `total` from its lines.
- Keep `__repr__` compact and truthful, e.g., `Order(id='P1', channel='pos', lines=3, total=Decimal('29.00'))`.

**Acceptance:** `test_order.py` verifies all three constructors and totals.

**Error Handling:** For malformed CSV rows, raise `ValueError` with a helpful message.

---

## Coding Standards
- Use `Decimal` for prices and totals; avoid floats.
- Add informative docstrings (you may include tiny doctests).
- Keep methods small and focused.
- Prefer keyword-only args on public constructors where clarity helps.
- No I/O in domain objects (no printing from library code except `__repr__`).

---

## Common Pitfalls (and fixes)
- **Forgetting `super()`** in MI chains → breaks corporate checks or duplicates work. Always call `super()` in overrides.
- **Mutating basket via `__setitem__`** → forbidden. Only `add_line(...)` is allowed.
- **Promotion order** matters. The tests rely on the provided `promos` order.
- **GreatCircle math**: Degrees vs radians—convert!
- **Decimal arithmetic**: Construct via strings (`Decimal("10.00")`), not floats.

---

## How to Run Locally
```bash
pip install pytest
pytest -q
```
Run a single test file while developing:
```bash
pytest -q tests/test_basket.py
```

---

## Deliverables
- Fill in all TODOs in `src/northstar/*.py` without changing public test expectations.
- Optional: add your **own** small tests for edge cases (kept in `tests/` with your initials).

---

## Grading (100 pts)
- Design & LSP correctness — 15  
- Cooperative `super()` / MI working — 15  
- `Basket` correctness & guardrails — 10  
- `Promotion` impl & `checkout` polymorphism — 15  
- Distance strategies — 10  
- Alternate constructors & `Order` — 10  
- Diagnostics (`__repr__`) & doctest — 5  
- Code quality (typing, docs, clarity) — 10  
- Tests you add/modify (if any) — 10  
**Extra credit (+5):** Add a new `Promotion` or `Distance` with tests.

---

## Academic Integrity
Write your own solution. Cite any references (if used) in comments.
