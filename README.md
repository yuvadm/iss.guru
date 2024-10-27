# ISS Pass Predictions

**[https://iss.guru](https://iss.guru)** - A modern web interface and API serving accurate ISS pass predictions. Provides predictions for both visual passes as well as amateur radio uses.

Built in Python using [Skyfield](https://rhodesmill.org/skyfield/) and [FastAPI](https://fastapi.tiangolo.com/).

## Dev

```bash
$ uv
```

Lock requirements prior to deploy:

```bash
$ uv pip compile pyproject.toml -o requirements.txt
```