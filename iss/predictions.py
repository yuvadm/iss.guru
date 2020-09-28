from collections import defaultdict
from skyfield.api import Topos, load

from .utils import chunks


ISS = "ISS (ZARYA)"
STATIONS_URL = "http://celestrak.com/NORAD/elements/stations.txt"


class Predictions(object):
    def __init__(
        self,
        lat,
        lng,
        altitude=0,
        tz="UTC",
        satellite=ISS,
        start=None,
        days=10,
        tle_file=None,
    ):
        self.lat = lat
        self.lng = lng
        self.altitude = altitude
        self.tz = tz
        self.start = start
        self.days = days
        self.tle_file = tle_file.resolve().as_posix() if tle_file else STATIONS_URL

        self.satellite = self.init_satellite(satellite)
        self.location = self.init_location()

    def init_stations(self):
        return load.tle_file(self.tle_file)

    def init_satellite(self, satellite):
        satellites = self.init_stations()
        by_name = {sat.name: sat for sat in satellites}
        return by_name[satellite]

    def init_location(self):
        return Topos(latitude_degrees=self.lat, longitude_degrees=self.lng)

    def get_next_days(self):
        ts = load.timescale()
        t0 = ts.now() if not self.start else ts.ut1_jd(self.start)
        t1 = ts.ut1_jd(t0.ut1 + self.days)
        return t0, t1

    def get_position_details(self, t):
        difference = self.satellite - self.location
        topocentric = difference.at(t)
        alt, az, distance = topocentric.altaz()
        return {
            "time": t.utc_iso(),
            "degrees": int(alt.degrees),
            "azimuth": int(az.degrees),
            "distance": int(distance.km),
        }

    def get_prediction_details(self, rise, culminate, zet):
        length = int((zet - rise) * 86400)
        return {
            "length": length,
            "rise": self.get_position_details(rise),
            "culminate": self.get_position_details(culminate),
            "set": self.get_position_details(zet),
        }

    def get_prediction_events(self):
        t0, t1 = self.get_next_days()

        ts, _events = self.satellite.find_events(
            self.location, t0, t1, altitude_degrees=self.altitude
        )

        # events are returned as 3-tuples of (rise, culminate, set)
        # where rise/set are relative to given altitude
        # docs mention the possibilibity of several culminations
        # https://rhodesmill.org/skyfield/earth-satellites.html#finding-when-a-satellite-rises-and-sets
        # but this doesn't seem to happen in our case
        res = list(chunks(ts, 3))

        if len(res[-1]) != 3:
            # truncate the last event in case it's a partial one
            res = res[:-1]

        return res

    def get_predictions(self):
        preds = self.get_prediction_events()
        return [self.get_prediction_details(*p) for p in preds]

    def truncate_prediction_dates(self, pred):
        for t in ["rise", "culminate", "set"]:
            pred[t]["time"] = pred[t]["time"][11:]
        return pred

    def get_grouped_predictions(self):
        preds = self.get_predictions()
        res = defaultdict(list)

        for pred in preds:
            date = pred["rise"]["time"][:10]
            res[date].append(self.truncate_prediction_dates(pred))

        return res
