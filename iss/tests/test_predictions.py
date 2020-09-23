from skyfield.api import Topos

from ..predictions import Predictions


def test_get_timescales():
    p = Predictions(lat=32.0853, lng=34.7817, tz="Asia/Jerusalem")
    days = 5
    t0, t1 = p.get_next_days(days=days)
    delta = t1.ut1 - t0.ut1
    assert delta == days


def test_get_location():
    p = Predictions(lat=32.0853, lng=34.7817)
    tlv = Topos("32.0853 N", "34.7817 E")
    topos = p.get_location()
    assert topos.latitude.degrees == tlv.latitude.degrees
    assert topos.longitude.degrees == tlv.longitude.degrees
