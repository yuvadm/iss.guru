import pytest

from ..config import GEOIP_GEOLITE2_CITY_PATH
from ..geo import get_location

geoip_required = pytest.mark.skipif(
    not GEOIP_GEOLITE2_CITY_PATH,
    reason="Path to GeoLite2 city database must be provided",
)


@geoip_required
def test_geo():
    ip = "2.52.2.52"
    location = get_location(ip)
    assert location.latitude == 31.5
    assert location.longitude == 34.75
    assert location.time_zone == "Asia/Jerusalem"


@geoip_required
def test_geo_localhost():
    ip = "127.0.0.1"
    location = get_location(ip)
    assert location.latitude == 34.7641
    assert location.longitude == 32.0669
    assert location.time_zone == "Asia/Jerusalem"
