from skyfield.api import Topos, load


class Predictions(object):
    ISS = "ISS (ZARYA)"

    def __init__(self, lat, lng, altitude=30.0, tz="UTC", satellite=ISS):
        self.lat = lat
        self.lng = lng
        self.altitude = altitude
        self.tz = tz
        self.satellite = satellite

    def init_stations(self):
        stations_url = "http://celestrak.com/NORAD/elements/stations.txt"
        return load.tle_file(stations_url)

    def get_next_days(self, days=10):
        ts = load.timescale()
        t0 = ts.now()
        t1 = ts.ut1_jd(t0.ut1 + days)
        return t0, t1

    def get_location(self):
        return Topos(latitude_degrees=self.lat, longitude_degrees=self.lng)

    def get_satellite(self):
        satellites = self.init_stations()
        by_name = {sat.name: sat for sat in satellites}
        return by_name[self.satellite]

    def get_predictions(self):
        satellite = self.get_satellite()
        t0, t1 = self.get_next_days(days=10)
        location = self.get_location()

        t, events = satellite.find_events(
            location, t0, t1, altitude_degrees=self.altitude
        )

        for ti, event in zip(t, events):
            name = ("rise above 30°", "culminate", "set below 30°")[event]
            print(ti.utc_strftime("%Y %b %d %H:%M:%S"), name)
