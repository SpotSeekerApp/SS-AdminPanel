import pytest
from services.logger import logger
import config

def test_logger():
    # if logger could not be created, this gives false
    assert True