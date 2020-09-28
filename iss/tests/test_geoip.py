import pytest
import geoip2.database

from ..config import GEOIP_CITY_PATH

geoip_required = pytest.mark.skipif(
    not GEOIP_CITY_PATH, reason="Path to GeoLite2 city database must be provided"
)


@geoip_required
def test_geo():
    ip = "2.52.2.52"
    with geoip2.database.Reader(GEOIP_CITY_PATH) as reader:
        res = reader.city(ip)
        location = res.location
        assert location.latitude == 31.5
        assert location.longitude == 34.75
        assert location.time_zone == "Asia/Jerusalem"
