from skyfield.api import Topos, load

stations_url = 'http://celestrak.com/NORAD/elements/stations.txt'
satellites = load.tle_file(stations_url)
print('Loaded', len(satellites), 'satellites')

by_name = {sat.name: sat for sat in satellites}
satellite = by_name['ISS (ZARYA)']
print(satellite)

tlv = Topos('32.0853 N', '34.7817 E')

ts = load.timescale()
t0 = ts.utc(2020, 9, 20)
t1 = ts.utc(2020, 9, 30)

t, events = satellite.find_events(tlv, t0, t1, altitude_degrees=60.0)
for ti, event in zip(t, events):
    name = ('rise above 30°', 'culminate', 'set below 30°')[event]
    print(ti)
    print(ti.utc_strftime('%Y %b %d %H:%M:%S'), name)
