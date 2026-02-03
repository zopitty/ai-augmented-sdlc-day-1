def calc(w, d, p):
    err = -1

    try:
        w = float(str(w).strip())
    except Exception:
        return err

    try:
        d = float(str(d).strip())
    except Exception:
        return err

    if w < 0 or d < 0:
        return err

    if w == 0 and d == 0:
        return 0

    pr = p
    if pr is None:
        pr = "standard"
    elif isinstance(pr, (int, float)):
        if pr == 0:
            pr = "standard"
        elif pr == 1:
            pr = "express"
        elif pr == 2:
            pr = "overnight"
        else:
            pr = str(pr)

    try:
        pr = str(pr).strip().lower()
    except Exception:
        return err

    if pr in ("s", "std", "standard"):
        pr = "standard"
    elif pr in ("e", "exp", "express", "priority"):
        pr = "express"
    elif pr in ("o", "one", "overnight", "night"):
        pr = "overnight"
    else:
        pr = "standard"

    base = 0.0
    if w <= 2:
        base = 4.99
    else:
        if w <= 10:
            base = 7.99
        else:
            if w <= 50:
                base = 14.99
            else:
                base = 29.99
                base = base + (w - 50) * 0.25

    per_km = 0.0
    if d < 200:
        per_km = 0.020
    else:
        per_km = 0.015
        if d >= 1000:
            per_km = 0.025
    distance_fee = d * per_km

    fuel_pct = 0.08 if d < 500 else 0.12
    if w > 30:
        fuel_pct = fuel_pct + 0.01

    handling_fee = 0.0
    priority_multiplier = 1.0

    if pr == "express":
        priority_multiplier = 1.50
        handling_fee = 2.00
        if w > 20:
            handling_fee = handling_fee + 1.00
    elif pr == "overnight":
        priority_multiplier = 2.00
        handling_fee = 5.00
        if d > 800:
            handling_fee = handling_fee + 3.00

    remote_fee = 0.0
    if d > 1500:
        remote_fee = 15.00
    if d > 2000 and pr != "overnight":
        remote_fee = remote_fee + 5.00

    subtotal = base + distance_fee + handling_fee + remote_fee
    subtotal = subtotal + subtotal * fuel_pct

    if subtotal < 5.00:
        subtotal = 5.00

    total = subtotal * priority_multiplier

    if total > 100:
        total = round(total, 2)
    else:
        total = round(total, 1)

    return total
