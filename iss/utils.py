def chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i : i + n]


def seconds_to_minutes(secs):
    return f"{secs // 60}:{secs % 60:02}"


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
