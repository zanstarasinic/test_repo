# CI Test Fixer Playground

A realistic e-commerce backend project designed to test CI tools that analyze
git diffs and automatically fix broken tests.

## Quick Start

```bash
pip install pytest
pytest -v              # All 98 tests pass on main
git checkout break/rename-method
pytest -v              # 9 tests fail — your tool should detect and fix them
```

## Project Structure

```
src/
├── models/
│   ├── user.py          # User model with roles, status, discounts
│   ├── product.py       # Product model with stock, categories, discounts
│   └── order.py         # Order model with items, tax, shipping calculations
├── services/
│   ├── pricing.py       # Pricing engine (bulk/tier/cart calculations)
│   ├── inventory.py     # Stock management and product search
│   └── notification.py  # Email notification service
├── utils/
│   ├── validators.py    # Email, password, address validation
│   └── formatters.py    # Currency, date, text formatting
└── api/
    └── routes.py        # Simulated REST API handlers

tests/
├── unit/                # 7 test files covering each module
└── integration/         # API route integration tests
```

## Break Branches

Each `break/*` branch simulates a realistic code change that breaks existing tests.
They are designed to be used as PRs against `main`.

| Branch | Scenario | Failures | What Changed |
|--------|----------|----------|--------------|
| `break/rename-method` | Method rename | 9 | `get_display_name` → `format_display_name`, `get_discount_percentage` → `get_tier_discount` |
| `break/change-return-type` | Dict → dataclass return | 4 | `calculate_cart_total` returns `CartSummary` instead of `dict` |
| `break/modify-business-logic` | Business rule changes | 9 | Tax rate 8%→10%, shipping threshold $50→$75, bulk threshold 5→10 |
| `break/change-signature` | Parameter changes | 3 | Added required params, renamed keyword args |
| `break/change-enum-values` | Enum value changes | 5 | OrderStatus values lowercase→UPPERCASE, new statuses added |
| `break/refactor-split-module` | Module extraction | 8 | `search_products` & `get_low_stock_products` moved to new `ProductSearchService` |
| `break/change-error-handling` | Exception type changes | 3 | `ValueError` → `InsufficientStockError` / `InvalidDiscountError` |
| `break/change-api-response` | API response restructure | 11 | New envelope format: `{success, data, error}` instead of `{status, data}` |
| `break/update-validation-rules` | Stricter validation | 9 | Password min length 8→12, requires special char, stricter email regex |
| `break/change-constants` | Formatter/threshold changes | 5 | Date format, currency format, truncation defaults all changed |

## Failure Categories

The branches cover these real-world failure patterns:

1. **AttributeError** — method/attribute renamed or removed
2. **TypeError** — function signature changed (missing args, renamed kwargs)
3. **AssertionError** — business logic changed (different expected values)
4. **KeyError / TypeError** — return type changed (dict→dataclass, key renames)
5. **ValueError** — enum values changed, deserialization breaks
6. **Wrong exception type** — `pytest.raises(ValueError)` but code raises custom exception
7. **Import errors** — module split, functions moved to new location
8. **Validation failures** — stricter rules make previously-valid inputs fail

## Verification Script

```bash
./verify.sh
```

## Using with Your CI Tool

1. Push this repo to GitHub
2. For each `break/*` branch, open a PR against `main`
3. Your CI tool should:
   - Detect failing tests from `pytest` output
   - Analyze the git diff (`git diff main...break/branch-name`)
   - Determine the correct test fixes
   - Comment on the PR with suggested changes
