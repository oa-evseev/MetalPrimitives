import FreeCAD as App


def qlength(value) -> float:
    """
    Convert App::PropertyLength-like value to a float in mm (FreeCAD base unit for Length).
    Accepts numbers, strings with units, and Quantity.
    """
    if isinstance(value, (int, float)):
        return float(value)
    try:
        return float(App.Units.Quantity(value))
    except Exception as exc:
        raise TypeError(f"Cannot convert to Quantity/Length: {value!r}") from exc
