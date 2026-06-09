from datetime import datetime


def format_price_uzs(value: int | float) -> str:
    """Return a compact price label in Uzbek sums."""
    return f"{value:,.0f} сум".replace(",", " ")


def current_year() -> int:
    """Expose current year for footer/copyright."""
    return datetime.now().year
