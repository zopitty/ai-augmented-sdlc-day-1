# QuickShip Logistics Coding Standards

## 1. Financial Calculations
* **Decimal Usage:** All currency and monetary calculations must use the `Decimal` type from Python's built-in `decimal` module.
* **Prohibited Types:** Never use floating-point numbers (`float`) for money due to precision errors.

## 2. Validation & Error Handling
* **Validate Inputs:** Validate and normalize inputs early (types, ranges, allowed values).
* **Prefer Exceptions:** Prefer raising `ValueError`/`TypeError` for invalid inputs.
* **If Backward Compatibility Is Required:** If you keep legacy sentinel returns (e.g., `-1`), isolate that behavior at the boundary and document it clearly.

## 3. Logging
* Use the standard `logging` module (no `print`).
* Use a module-level logger via `logging.getLogger(__name__)`.
* Log at appropriate levels (`debug` for tracing, `info` for business events, `warning`/`error` for failures).

## 4. Documentation
* All public functions must have a docstring that includes input types and return types.
* Docstrings must describe error behavior (exceptions vs sentinel values).

## 5. Typing & Style
* Add type hints for function inputs/outputs.
* Keep functions small and focused (single responsibility).
* Follow PEP 8 formatting and naming conventions.

## 6. Tests
* Add `unittest` coverage for edge cases, invalid inputs, and boundary conditions.
* Avoid flaky tests; keep tests deterministic.

---

Note: The starter `shipping_calculator.py` is intentionally "legacy" and may violate these standards. Your refactor should move it toward compliance.