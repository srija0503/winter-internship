# Clinical Rules & Sources

This document lists the implemented clinical thresholds used by the system and references.

Rules implemented:
- Total Bilirubin > 1.2 mg/dL -> Jaundice (warning)
- Alamine Aminotransferase (ALT) > 56 U/L -> High ALT (warning)
- Albumin < 3.5 g/dL -> Low Albumin (warning)
- AST/ALT ratio > 2 -> possible alcoholic liver disease or advanced fibrosis

Sources:
- Standard clinical laboratory reference ranges (institutional references).
- NOTE: Please verify institution-specific ranges before use in production.

Additions:
- Consider adding direct/indirect bilirubin ratio rules and AG ratio interpretations.