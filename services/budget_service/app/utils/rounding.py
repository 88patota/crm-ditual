from decimal import Decimal, ROUND_HALF_UP


def _to_decimal(value) -> Decimal:
    """Converte valor para Decimal de forma segura."""
    if value is None or value == "":
        return Decimal('0')
    try:
        return Decimal(str(value))
    except Exception:
        return Decimal('0')


def _pattern_for_places(places: int) -> str:
    """Gera padrão Decimal para quantize com número de casas."""
    if places <= 0:
        return '1'
    return '0.' + ('0' * (places - 1)) + '1'


def quantize_to(value, pattern: str) -> float:
    """Arredonda usando Decimal.quantize com ROUND_HALF_UP e retorna float."""
    d = _to_decimal(value)
    return float(d.quantize(Decimal(pattern), rounding=ROUND_HALF_UP))


def round_currency(value) -> float:
    """Arredonda valores monetários para 2 casas decimais (ROUND_HALF_UP)."""
    return quantize_to(value, '0.01')


def round_unit(value, places: int = 6) -> float:
    """Arredonda valores unitários/intermediários com precisão configurável (default 6)."""
    pattern = _pattern_for_places(places)
    return quantize_to(value, pattern)


def round_percent(value, places: int = 2) -> float:
    """Arredonda percentuais em forma decimal (ex.: 0.1234) para N casas (default 2)."""
    pattern = _pattern_for_places(places)
    return quantize_to(value, pattern)


def round_percent_display(value, places: int = 2) -> float:
    """Converte percentual decimal para exibição (multiplica por 100) e arredonda."""
    d = _to_decimal(value) * Decimal('100')
    pattern = _pattern_for_places(places)
    return float(d.quantize(Decimal(pattern), rounding=ROUND_HALF_UP))