import pytest

from ..utils import deg_to_cardinal, seconds_to_minutes, normalize_lat_lng


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


def test_normalize_lat_lng():
    cases = [
        ("N12.345", "E67.890", 12.345, 67.890),
        ("S12.345", "W67.890", -12.345, -67.890),
        ("S11", "W22", -11, -22),
        ("N0.987", "W0.123", 0.987, -0.123),
        ("S88.765", "E177.654", -88.765, 177.654),
    ]
    for lat, lng, nlat, nlng in cases:
        assert normalize_lat_lng(lat, lng) == (nlat, nlng)


def test_fail_normalize_lat_lng():
    failures = [
        ("12", "E45"),
        ("B12", "E45"),
        ("12", "X45"),
    ]
    for lat, lng in failures:
        with pytest.raises(Exception):
            normalize_lat_lng(lat, lng)


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
