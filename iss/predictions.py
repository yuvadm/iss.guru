from skyfield.api import Topos, load

from .utils import chunks


class Predictions(object):
    ISS = "ISS (ZARYA)"

    def __init__(
        self, lat, lng, altitude=30.0, tz="UTC", satellite=ISS, start=None, days=10
    ):
        self.lat = lat
        self.lng = lng
        self.altitude = altitude
        self.tz = tz
        self.satellite = satellite
        self.start = start
        self.days = days

    def init_stations(self):
        stations_url = "http://celestrak.com/NORAD/elements/stations.txt"
        return load.tle_file(stations_url)

    def get_next_days(self):
        ts = load.timescale()
        t0 = ts.now() if not self.start else ts.ut1_jd(self.start)
        t1 = ts.ut1_jd(t0.ut1 + self.days)
        return t0, t1

    def get_location(self):
        return Topos(latitude_degrees=self.lat, longitude_degrees=self.lng)

    def get_satellite(self):
        satellites = self.init_stations()
        by_name = {sat.name: sat for sat in satellites}
        return by_name[self.satellite]

    def get_predictions(self):
        satellite = self.get_satellite()
        t0, t1 = self.get_next_days()
        location = self.get_location()

        ts, _events = satellite.find_events(
            location, t0, t1, altitude_degrees=self.altitude
        )

        # events are returned as 3-tuples of (rise, culminate, set)
        # where rise/set are relative to given altitude
        # docs mention the possibilibity of several culminations
        # https://rhodesmill.org/skyfield/earth-satellites.html#finding-when-a-satellite-rises-and-sets
        # but this doesn't seem to happen in our case
        preds = chunks(ts, 3)
        return [[t.utc_iso() for t in p] for p in preds]
