from collections import namedtuple
import geoip2.database
import geoip2.errors

from .config import GEOIP_GEOLITE2_CITY_PATH

DEFAULT_LOCATION = {
    "latitude": 34.7641,
    "longitude": 32.0669,
    "time_zone": "Asia/Jerusalem",
}

default_location = namedtuple("Location", DEFAULT_LOCATION.keys())(
    *DEFAULT_LOCATION.values()
)


def get_location(ip):
    try:
        with geoip2.database.Reader(GEOIP_GEOLITE2_CITY_PATH) as reader:
            try:
                res = reader.city(ip)
                return res.location
            except geoip2.errors.AddressNotFoundError:
                return default_location
    except TypeError:
        return default_location
