import density
import pytest

@pytest.fixture
def app():
    return density.app.test_client()

@pytest.fixture
def auth_header():
    return {'Authorization-Token': 'abcdefghjijklmnopqrstuvwxyz'}
