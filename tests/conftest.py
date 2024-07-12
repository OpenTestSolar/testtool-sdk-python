import logging


def pytest_configure():
    logging.basicConfig(level=logging.DEBUG)
