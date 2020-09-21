from skyfield.api import Topos, load

TEL_AVIV = Topos('32.0853 N', '34.7817 E')
ISS = "ISS (ZARYA)"

def init_stations():
    stations_url = 'http://celestrak.com/NORAD/elements/stations.txt'
    return load.tle_file(stations_url)

def get_predictions(location=TEL_AVIV, satellite_name=ISS):
    satellites = init_stations()
    by_name = {sat.name: sat for sat in satellites}
    satellite = by_name[satellite_name]

    ts = load.timescale()
    t0 = ts.now()
    t1 = ts.utc(2020, 9, 30)

    t, events = satellite.find_events(location, t0, t1, altitude_degrees=60.0)
    for ti, event in zip(t, events):
        name = ('rise above 30°', 'culminate', 'set below 30°')[event]
        print(ti)
        print(ti.utc_strftime('%Y %b %d %H:%M:%S'), name)
