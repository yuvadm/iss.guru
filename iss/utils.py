def chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i : i + n]


def seconds_to_minutes(secs):
    return f"{secs // 60}:{secs % 60:02}"


def normalize_lat_lng(lat, lng):
    if lat[0] not in "NS" or lng[0] not in "EW":
        raise Exception("Lat/lng must be formatted as N12.345 and E67.890")
    nlat = float(lat[1:]) * (-1 if lat[0] == "S" else 1)
    nlng = float(lng[1:]) * (-1 if lng[0] == "W" else 1)
    return nlat, nlng


def deg_to_cardinal(deg):
    cardinals = [
        "N",
        "NNE",
        "NE",
        "ENE",
        "E",
        "ESE",
        "SE",
        "SSE",
        "S",
        "SSW",
        "SW",
        "WSW",
        "W",
        "WNW",
        "NW",
        "NNW",
    ]
    return cardinals[round((deg % 360) / 22.5) % 16]
