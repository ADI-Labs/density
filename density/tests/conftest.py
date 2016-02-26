import psycopg2
import pytest

import density

@pytest.fixture
def app():
    return density.app.test_client()

@pytest.fixture
def auth_header():
    return {'Authorization-Token': 'abcdefghjijklmnopqrstuvwxyz'}

@pytest.yield_fixture
def cursor():
    with density.pg_pool.getconn() as conn:
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        yield cursor
        conn.rollback()
