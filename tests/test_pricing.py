from src.pricing import get_price
from src.pricing import Type


def test_get_price():
    # getting "Sephiroth, the Savior - Atraxa, Grand Unifier (Showcase)"
    assert get_price("FCA",49) > 0.0

def test_get_price_foil():
    # getting "Bartz Klauser - Winota, Joiner of Forces (Showcase)"
    assert get_price("FCA",19, Type.FOIL) > 0.0