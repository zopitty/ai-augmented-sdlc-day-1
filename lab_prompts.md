# Lab Session: Prompt Log
**Student Name:** Tan Bing Hong
**Instructions:** Record the exact prompts you typed into GitHub Copilot for each step below (copy/paste). Optionally include key parts of Copilot’s response.

## Step 1: Role & Requirements Clarification (Reverse Prompting)
*(Paste your persona setup and your request for **clarifying questions** here. The goal is to have Copilot ask you ~3 questions about requirements/business rules/inputs/edge cases **before writing any code**. These are requirements-clarification questions for the coding exercise (not a job interview).)*

Prompt:

You are a senior python backend engineer who cares about clean architecture and PEP8.

Before you write code, ask me 3 clarifying questions.

Response:

Looking at this shipping calculator code, I have 3 clarifying questions before refactoring:

Business Logic Preservation: Should I maintain the exact same calculation logic and edge cases (like the fuel percentage increasing for weight > 30, the distance-based per_km logic with the >= 1000 special case, etc.), or are there any known bugs or business rule changes you'd like to address?

API/Interface Compatibility: Do you need to maintain backward compatibility with the current function signature calc(w, d, p), or can I redesign the interface to be more explicit (e.g., calculate_shipping(weight, distance, priority) or even use a dataclass/named parameters)?

Error Handling Strategy: Currently, the function returns -1 for errors and 0 for zero weight/distance. Would you prefer:

Raising exceptions for invalid inputs (more Pythonic)
Returning a result object with success/error states
Keeping the current approach but documenting it better
These answers will help me provide the most appropriate refactoring that meets your needs while maintaining clean architecture principles.

Prompt:

1. There are no known bugs
2. Weight is in kg, Distance is in km, Currency is in USD
3. No.

Response:

Thank you for the clarifications! Here are my 3 questions:

1. **Error Handling Strategy**: Since you said "No" to question 3, I need clarification - would you prefer:
   - **Option A**: Raise exceptions for invalid inputs (more Pythonic and explicit)
   - **Option B**: Keep returning `-1` for errors but with better documentation
   - **Option C**: Use Python's `Optional[float]` and return `None` for errors

2. **Configuration Management**: The business rules have many magic numbers (weight tiers: 2, 10, 50 kg; distance breakpoints: 200, 500, 1000, 1500, 2000 km; fees, multipliers, etc.). Should I:
   - Extract these into named constants at module level
   - Use a configuration class/dataclass
   - Keep them inline with descriptive variable names

3. **Code Structure**: For clean architecture, would you prefer:
   - **Option A**: Single refactored function with helper functions for each calculation step (base fee, distance fee, fuel surcharge, etc.)
   - **Option B**: A `ShippingCalculator` class with methods for each component
   - **Option C**: Pure functions organized by domain (weight-based calculations, distance-based calculations, priority-based calculations)

These will help me deliver the most maintainable and clean solution!

Prompt:

1. Option A. Raise Exceptions for valid inputs
2. Extract them into named constants
3. Option C

Response:

```py
"""
Shipping cost calculator with clean architecture.

Calculates shipping costs based on weight (kg), distance (km), and priority level.
All costs are in USD.
"""

from typing import Union

# Weight-based fee constants (kg)
WEIGHT_TIER_1_MAX = 2.0
WEIGHT_TIER_2_MAX = 10.0
WEIGHT_TIER_3_MAX = 50.0

.
.
.
```


## Step 2: Planning (Zero-Shot CoT + RAG)
*(Paste your prompt asking for a step-by-step refactoring plan referencing coding_standards.md. Include “Let’s think step by step.” Do not generate code yet.)*

Prompt:

Let's think step by step. Do not generate code yet.

Answer:

```
Perfect! Let's analyze the current code step by step and create a refactoring plan.

## Step-by-Step Analysis

### 1. **Input Validation & Parsing**
- Currently uses try/except to parse weight and distance to float
- Returns `-1` on any parsing error
- Validates non-negative values
- Special case: returns `0` when both weight and distance are zero
- Priority has complex parsing logic with multiple aliases and type conversions

### 2. **Business Logic Components** (in order of execution)
   
   **a. Base Fee Calculation (weight-based)**
   - Tier 1: ≤2kg → $4.99
   - Tier 2: ≤10kg → $7.99
   - Tier 3: ≤50kg → $14.99
   - Tier 4: >50kg → $29.99 + $0.25 per kg over 50kg

   **b. Distance Fee Calculation**
   - <200km → $0.020/km
   - 200-999km → $0.015/km

## Refactoring Plan

**Ready to proceed with code generation?**
```

## Step 3: Execution (Few-Shot + Tool Use)
*(Paste your prompt containing the docstring examples and your request to implement the refactor. Then paste the prompt that asks Copilot (as a unit test generator) to create `unittest` tests targeting edge cases/boundary conditions.)*

Prompt:
Generate a unittest suite with reference to the following example:

```
    * *Examples:*
      * `Input: w=10 (int), d=100 (int), p='standard' (str) -> Output: 12.34 (Decimal)`
      * `Input: w='2.5' (str), d='0' (str), p=None (None) -> Output: 5.00 (Decimal)`
```

Response:
```
Here's a comprehensive unittest suite for the shipping calculator with edge cases and the reference examples:

````python
"""
Unit tests for shipping_calculator module.

Tests cover:
- Valid inputs with different data types
- Edge cases (zero values, boundary conditions)
- Invalid inputs (negative values, unparseable data)
- Priority level variations and aliases
- Weight and distance tier boundaries
- Remote area calculations
- Fuel surcharge logic
"""

import unittest
from shipping_calculator import (
    calculate_shipping_cost,
    calc,
    InvalidInputError,
    calculate_base_fee,
    calculate_distance_fee,
    calculate_fuel_surcharge,
    calculate_priority_fees,
    calculate_remote_fee,
    _parse_numeric_input,
    _normalize_priority,
)
.
.
````

This unittest suite includes:

1. **Reference Examples**: Tests the exact examples you provided
2. **Edge Cases**: Zero values, boundary conditions, minimum charges
3. **Input Validation**: Invalid strings, negative values, type conversions
4. **Business Logic**: All weight tiers, distance ranges, priority levels, fuel surcharges, remote fees
5. **Backward Compatibility**: Tests for the legacy `calc()` function
6. **Comprehensive Coverage**: 60+ test cases covering all major code paths

Run with: `python -m unittest test_shipping_calculator.py`
```

## Step 4: Review (Reflexion + Self-Consistency)
*(Paste your prompt asking Copilot to critique its own code for logic gaps/type hints/tests, then produce a V2. Also include your prompt requesting 3 alternative implementations and a recommendation.)*

Prompt:
Review the code you just wrote. Identify potential logic errors or missing type hints. Then generate a V2.

Prompt:
Generate three different implementations using if/else, match/case and dictionary lookup

Response:
Winner: Dictionary Lookup (Implementation 3)
Reasons:
Configuration Separation: Business rules (fees, thresholds, multipliers) are cleanly separated into data structures, making updates trivial
No Duplication: The priority configuration uses a single source of truth instead of scattered if/else logic
Easy Testing: Can test configuration separately from logic
Better for Changes: Adding a new priority level only requires adding a dictionary entry, not modifying function logic
Performance: Dictionary lookups are O(1), while if/else chains are O(n)
Python Compatibility: Works on all modern Python versions (unlike match/case)
Industry Standard: This pattern is common in production codebases for rule-based systems
When to use alternatives:

if/else: Simple cases with 2-3 conditions
match/case: When using Python 3.10+ and want pattern matching features for complex types
Recommendation: Use the dictionary lookup implementation for this shipping calculator as it best balances readability, maintainability, and extensibility for a business-rules-heavy application.