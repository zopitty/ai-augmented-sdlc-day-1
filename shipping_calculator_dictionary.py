"""
Shipping cost calculator - dictionary lookup implementation.

This version uses dictionaries and lambda functions for cleaner, more maintainable code.
"""

from typing import Union, Tuple, Callable
import bisect

# [All constants same as v1]
WEIGHT_TIER_1_MAX = 2.0
WEIGHT_TIER_2_MAX = 10.0
WEIGHT_TIER_3_MAX = 50.0
BASE_FEE_TIER_1 = 4.99
BASE_FEE_TIER_2 = 7.99
BASE_FEE_TIER_3 = 14.99
BASE_FEE_TIER_4 = 29.99
EXCESS_WEIGHT_RATE = 0.25

DISTANCE_SHORT_MAX = 200.0
DISTANCE_MEDIUM_MAX = 1000.0
PER_KM_SHORT = 0.020
PER_KM_MEDIUM = 0.015
PER_KM_LONG = 0.025

PRIORITY_STANDARD = "standard"
PRIORITY_EXPRESS = "express"
PRIORITY_OVERNIGHT = "overnight"
EXPRESS_MULTIPLIER = 1.50
OVERNIGHT_MULTIPLIER = 2.00
EXPRESS_HANDLING_FEE = 2.00
EXPRESS_HEAVY_WEIGHT_THRESHOLD = 20.0
EXPRESS_HEAVY_SURCHARGE = 1.00
OVERNIGHT_HANDLING_FEE = 5.00
OVERNIGHT_LONG_DISTANCE_THRESHOLD = 800.0
OVERNIGHT_DISTANCE_SURCHARGE = 3.00


class InvalidInputError(ValueError):
    """Raised when input parameters are invalid."""
    pass


# Weight tier configuration using sorted boundaries and fees
WEIGHT_TIERS = [
    (WEIGHT_TIER_1_MAX, BASE_FEE_TIER_1),
    (WEIGHT_TIER_2_MAX, BASE_FEE_TIER_2),
    (WEIGHT_TIER_3_MAX, BASE_FEE_TIER_3),
]


def calculate_base_fee(weight: float) -> float:
    """Calculate base fee using dictionary-based tier lookup."""
    # Find the appropriate tier
    for max_weight, base_fee in WEIGHT_TIERS:
        if weight <= max_weight:
            return base_fee
    
    # Over maximum tier - calculate excess
    excess_weight = weight - WEIGHT_TIER_3_MAX
    return BASE_FEE_TIER_4 + (excess_weight * EXCESS_WEIGHT_RATE)


# Distance tier configuration
DISTANCE_RATES = [
    (DISTANCE_SHORT_MAX, PER_KM_SHORT),
    (DISTANCE_MEDIUM_MAX, PER_KM_MEDIUM),
    (float('inf'), PER_KM_LONG),
]


def calculate_distance_fee(distance: float) -> float:
    """Calculate distance fee using dictionary-based rate lookup."""
    for max_distance, rate in DISTANCE_RATES:
        if distance < max_distance:
            return distance * rate
    
    # Fallback (should never reach here)
    return distance * PER_KM_LONG


# Priority configuration as nested dictionaries
PRIORITY_CONFIG = {
    PRIORITY_STANDARD: {
        'base_handling': 0.0,
        'multiplier': 1.0,
        'weight_surcharge': lambda w: 0.0,
        'distance_surcharge': lambda d: 0.0,
    },
    PRIORITY_EXPRESS: {
        'base_handling': EXPRESS_HANDLING_FEE,
        'multiplier': EXPRESS_MULTIPLIER,
        'weight_surcharge': lambda w: EXPRESS_HEAVY_SURCHARGE if w > EXPRESS_HEAVY_WEIGHT_THRESHOLD else 0.0,
        'distance_surcharge': lambda d: 0.0,
    },
    PRIORITY_OVERNIGHT: {
        'base_handling': OVERNIGHT_HANDLING_FEE,
        'multiplier': OVERNIGHT_MULTIPLIER,
        'weight_surcharge': lambda w: 0.0,
        'distance_surcharge': lambda d: OVERNIGHT_DISTANCE_SURCHARGE if d > OVERNIGHT_LONG_DISTANCE_THRESHOLD else 0.0,
    },
}


def calculate_priority_fees(priority: str, weight: float, distance: float) -> Tuple[float, float]:
    """Calculate priority fees using dictionary lookup."""
    config = PRIORITY_CONFIG.get(priority, PRIORITY_CONFIG[PRIORITY_STANDARD])
    
    handling_fee = (
        config['base_handling'] +
        config['weight_surcharge'](weight) +
        config['distance_surcharge'](distance)
    )
    
    return handling_fee, config['multiplier']


# Priority alias mapping
PRIORITY_ALIASES = {
    # Numeric
    0: PRIORITY_STANDARD,
    1: PRIORITY_EXPRESS,
    2: PRIORITY_OVERNIGHT,
    # String aliases
    's': PRIORITY_STANDARD,
    'std': PRIORITY_STANDARD,
    'standard': PRIORITY_STANDARD,
    'e': PRIORITY_EXPRESS,
    'exp': PRIORITY_EXPRESS,
    'express': PRIORITY_EXPRESS,
    'priority': PRIORITY_EXPRESS,
    'o': PRIORITY_OVERNIGHT,
    'one': PRIORITY_OVERNIGHT,
    'overnight': PRIORITY_OVERNIGHT,
    'night': PRIORITY_OVERNIGHT,
}


def _normalize_priority(priority: Union[str, int, float, None]) -> str:
    """Normalize priority using dictionary lookup."""
    if priority is None:
        return PRIORITY_STANDARD
    
    # Direct numeric lookup
    if isinstance(priority, (int, float)) and priority in PRIORITY_ALIASES:
        return PRIORITY_ALIASES[priority]
    
    # String lookup
    try:
        priority_str = str(priority).strip().lower()
        return PRIORITY_ALIASES.get(priority_str, PRIORITY_STANDARD)
    except (ValueError, AttributeError) as e:
        raise InvalidInputError(f"Invalid priority: cannot convert '{priority}' to string") from e