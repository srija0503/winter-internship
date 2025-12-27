# MEDICAL THRESHOLDS (Source: Standard Ranges)
# Keys are in normalized (lower_case_with_underscores) form.
NORMAL_RANGES = {
    "total_bilirubin": (0.1, 1.2),  # mg/dL
    "direct_bilirubin": (0.1, 0.3),
    "alkaline_phosphotase": (44, 147),
    "alamine_aminotransferase": (7, 56),
    "aspartate_aminotransferase": (10, 40),
    "albumin": (3.5, 5.5),
}

def _normalize_key(k: str) -> str:
    return k.strip().lower().replace(" ", "_")

def get_warnings(patient_data: dict) -> list:
    """
    patient_data: mapping of measurements (keys normalized or original).
    Returns list of warning strings.
    """
    # normalize keys for lookups
    normalized = { _normalize_key(k): v for k, v in patient_data.items() }

    warnings = []

    # Jaundice / bilirubin
    tb = normalized.get("total_bilirubin")
    if tb is not None:
        try:
            if float(tb) > NORMAL_RANGES["total_bilirubin"][1]:
                warnings.append("High Bilirubin (>1.2) - Jaundice indicated.")
        except (ValueError, TypeError):
            pass

    # High ALT
    alt = normalized.get("alamine_aminotransferase")
    if alt is not None:
        try:
            if float(alt) > NORMAL_RANGES["alamine_aminotransferase"][1]:
                warnings.append("High ALT - Sign of liver cell damage.")
        except (ValueError, TypeError):
            pass

    # Low albumin -> chronic
    albumin = normalized.get("albumin")
    if albumin is not None:
        try:
            if float(albumin) < NORMAL_RANGES["albumin"][0]:
                warnings.append("Low Albumin - Possible chronic liver disease.")
        except (ValueError, TypeError):
            pass

    # AST/ALT ratio (if both present)
    ast = normalized.get("aspartate_aminotransferase")
    if ast is not None and alt is not None:
        try:
            ratio = float(ast) / float(alt) if float(alt) != 0 else None
            if ratio is not None:
                if ratio > 2:
                    warnings.append("AST/ALT ratio > 2 - suggests alcoholic liver disease or advanced fibrosis.")
        except (ValueError, TypeError, ZeroDivisionError):
            pass

    return warnings