# CI Test Fixer Playground

A realistic e-commerce backend project designed to test CI tools that analyze
git diffs and automatically fix broken tests.

## Structure

- `src/models/` — Data models (User, Product, Order)
- `src/services/` — Business logic (Pricing, Inventory, Notifications)
- `src/utils/` — Validators and formatters
- `src/api/` — Simulated API route handlers
- `tests/` — Unit and integration tests

## Running Tests

```bash
pip install -r requirements.txt
pytest -v
```

## Branches

Each `break/*` branch simulates a realistic code change that breaks tests.
These are meant to be used as PRs against `main`.

| Branch | Scenario | Difficulty |
|---|---|---|
| `break/rename-method` | Rename a model method | Easy |
| `break/change-return-type` | Change dict structure in cart total | Medium |
| `break/modify-business-logic` | Change pricing rules (thresholds, rates) | Medium |
| `break/change-signature` | Add required params, rename args | Medium |
| `break/change-enum-values` | Change status enum values | Medium |
| `break/refactor-split-module` | Split one service into two | Hard |
| `break/change-error-handling` | Change exception types and messages | Medium |
| `break/change-api-response` | Restructure API response format | Hard |
| `break/update-validation-rules` | Tighten validation constraints | Easy |
| `break/change-constants` | Modify thresholds and config values | Medium |
