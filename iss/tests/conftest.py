import pytest


def pytest_addoption(parser):
    parser.addoption(
        "--compare", action="store_true", default=False, help="Run compare tests"
    )


def pytest_configure(config):
    config.addinivalue_line("markers", "compare: mark test as a comparison test")


def pytest_collection_modifyitems(config, items):
    if config.getoption("--compare"):
        return
    skip_compare = pytest.mark.skip(reason="need --compare option to run")
    for item in items:
        if "compare" in item.keywords:
            item.add_marker(skip_compare)
