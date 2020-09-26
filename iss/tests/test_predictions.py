from pathlib import Path
from skyfield.api import Topos

from ..predictions import Predictions

DATA_DIR = Path(__file__).parent / "data"
STATIONS = DATA_DIR / "stations.txt"


def test_get_timescales():
    days = 5
    p = Predictions(lat=32.0853, lng=34.7817, days=days)
    t0, t1 = p.get_next_days()
    delta = t1.ut1 - t0.ut1
    assert delta == days


def test_custom_start():
    start = 2459117.245895914
    p = Predictions(lat=32.0853, lng=34.7817, start=start)
    t0, _t1 = p.get_next_days()
    assert t0.ut1 == start


def test_get_location():
    p = Predictions(lat=32.0853, lng=34.7817)
    tlv = Topos("32.0853 N", "34.7817 E")
    location = p.location
    assert location.latitude.degrees == tlv.latitude.degrees
    assert location.longitude.degrees == tlv.longitude.degrees


def test_get_prediction_events():
    start = 2459117.245895914

    p = Predictions(
        lat=32.0853, lng=34.7817, tz="Asia/Jerusalem", start=start, tle_file=STATIONS
    )
    preds = p.get_prediction_events()
    assert len(preds) == 77
    preds = [[t.ut1 for t in pred] for pred in preds]
    assert preds[0] == [2459117.2606565966, 2459117.2618780565, 2459117.2631023712]

    p = Predictions(
        lat=32.0853,
        lng=34.7817,
        tz="Asia/Jerusalem",
        altitude=0,
        start=start,
        days=5,
        tle_file=STATIONS,
    )
    preds = p.get_prediction_events()
    assert len(preds) == 39


def test_get_predictions():
    start = 2459117.245895914
    p = Predictions(
        lat=32.0853, lng=34.7817, tz="Asia/Jerusalem", start=start, tle_file=STATIONS
    )
    preds = p.get_predictions()
    assert len(preds) == 77
    assert preds[0]["rise"]["time"] == "2020-09-24T18:15:22Z"
    assert preds[0]["rise"]["azimuth"] == 347
    assert preds[0]["culminate"]["degrees"] == 1
    assert preds[0]["set"]["distance"] == 2364
