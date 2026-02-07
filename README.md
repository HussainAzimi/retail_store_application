# Programming Assignment — Chapter 3: When Objects Are Alike (Inheritance & Polymorphism)

**Theme:** NorthStar Retail (inheritance, cooperative `super()`, multiple inheritance, mixins, and polymorphism)  
**Language:** Python 3.10+ (standard library only)  
**Estimated Time:** ~3–5 hours

## Learning Objectives
- Apply **inheritance** & **LSP** to share contracts safely.
- Use **cooperative `super()`** across single & multiple inheritance.
- Implement small **mixins** (capabilities) vs. deep hierarchies.
- Extend built-ins safely using **`collections.User*`** or composition.
- Design **polymorphic** APIs (ABCs) that avoid `isinstance` branching.
- Read **MRO** and solve diamond ordering in practice.

## What You Will Build
A tiny retail domain with:
- `Store` base + `FlagshipStore` override
- `OutletEligible` and `PopUp` capabilities combined as `HolidayPopUp`
- `Basket` list-like container with guardrails (uses `UserList`)
- `Promotion` ABC with `EmployeeDiscount` and `BOGO`
- `checkout(...)` that composes promos polymorphically
- `Distance` strategies (`Euclidean`, `Manhattan`, `GreatCircle`) for analytics
- `Order` with `from_pos`, `from_web`, `from_csv_row` alternate constructors

## Deliverables
- Complete the TODOs in `src/northstar/*.py` (replace `NotImplementedError`).
- Keep public method contracts consistent with the starter docstrings & tests.
- Ensure **all tests pass**: `pytest -q`

## Constraints
- Standard library only. Use `Decimal` for money.
- Use `super()` in **every** override (`__init__` included) where appropriate.
- Mixins should be small and light on state.
- No I/O in domain objects (no file/network), keep domain pure.

## How to Run
```bash
pip install pytest
pytest -q
```

## Grading Rubric (100 pts)
- Design & LSP correctness — 15
- Cooperative `super()` / MI working — 15
- `Basket` correctness & guardrails — 10
- `Promotion` impl & `checkout` polymorphism — 15
- Distance strategies — 10
- Alternate constructors & `Order` — 10
- Diagnostics (`__repr__`) & doctest example — 5
- Code quality (typing, docs, clarity) — 10
- Tests you add/modify (if any) — 10

**Extra credit (+5):** Add a new `Promotion` or `Distance` strategy with tests.

## Academic Integrity
Write your own solution. Cite any external references in comments.


---

## Start Here
Read **PA3_STUDENT_GUIDE.md** for detailed, step-by-step instructions, acceptance criteria, and common pitfalls.

Quickstart:
```bash
pip install pytest
pytest -q
```
