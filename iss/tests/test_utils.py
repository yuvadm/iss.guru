from ..utils import deg_to_cardinal, seconds_to_minutes


def test_seconds_to_minutes():
    cases = [
        (0, "0:00"),
        (1, "0:01"),
        (60, "1:00"),
        (61, "1:01"),
        (1439, "23:59"),
        (1440, "24:00"),
    ]
    for secs, s in cases:
        assert seconds_to_minutes(secs) == s


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
