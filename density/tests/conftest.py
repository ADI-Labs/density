import psycopg2
import pytest


@pytest.fixture
def app():
    from density import app
    return app.test_client()

@pytest.fixture
def auth_header():
    token = 'l7QGxn6doncC9Z9iPk7hykbMilRg2uV0JoIxYljtEai4o7rjVP1J9KDTudwYDNKl'
    return {'Authorization-Token': token}

@pytest.yield_fixture
def cursor():
    from density import pg_pool
    with pg_pool.getconn() as conn:
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        yield cursor
        conn.rollback()
