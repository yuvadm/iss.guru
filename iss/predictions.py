from skyfield.api import Topos, load

TEL_AVIV = Topos("32.0853 N", "34.7817 E")
ISS = "ISS (ZARYA)"


class Predictions(object):
    def __init__(self, lat, lng, tz="UTC", satellite=ISS):
        self.lat = lat
        self.lng = lng
        self.tz = tz
        self.satellite = satellite

    def init_stations(self):
        stations_url = "http://celestrak.com/NORAD/elements/stations.txt"
        return load.tle_file(stations_url)

    def get_next_days_timescale(self, days=10):
        ts = load.timescale()
        t0 = ts.now()
        t1 = ts.ut1_jd(t0.ut1 + days)
        return t0, t1

    def get_predictions(self, location=TEL_AVIV, satellite_name=ISS):
        satellites = self.init_stations()
        by_name = {sat.name: sat for sat in satellites}
        satellite = by_name[satellite_name]

        t0, t1 = self.get_next_days_timescale()

        t, events = satellite.find_events(location, t0, t1, altitude_degrees=30.0)
        print(t)
        print(events)
        for ti, event in zip(t, events):
            name = ("rise above 30°", "culminate", "set below 30°")[event]
            print(ti.utc_strftime("%Y %b %d %H:%M:%S"), name)
