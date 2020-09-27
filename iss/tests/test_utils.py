from ..utils import deg_to_cardinal


def test_deg_to_cardinal():
    cases = [
        (0, "N"),
        (360, "N"),
        (90, "E"),
        (91.1, "E"),
        (78, "ENE"),
        (182, "S"),
        (255, "WSW"),
        (324.99999, "NW"),
        (345, "NNW"),
        (350, "N"),
    ]
    for deg, cardinal in cases:
        assert deg_to_cardinal(deg) == cardinal
