from ..predictions import Predictions


def test_get_timescales():
    p = Predictions(lat=32.0853, lng=34.7817, tz="Asia/Jerusalem")
    days = 5
    t0, t1 = p.get_next_days_timescale(days=days)
    delta = t1.ut1 - t0.ut1
    assert delta == days
