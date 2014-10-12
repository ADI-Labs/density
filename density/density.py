
from flask import Flask, g, render_template
app = Flask(__name__)
# do import early to check that all env variables are present
app.config.from_object('config.flask_config')

# library imports
import psycopg2
import psycopg2.pool
import psycopg2.extras
from datetime import datetime


# create a pool of postgres connections
pg_pool = psycopg2.pool.SimpleConnectionPool(
    5,      # min connections
    20,     # max connections
    database=app.config['PG_DB'],
    user=app.config['PG_USER'],
    password=app.config['PG_PASSWORD'],
    host=app.config['PG_HOST'],
    port=app.config['PG_PORT'],
)


@app.before_request
def get_connections():
    """ Get connections from the Postgres pool. """
    g.pg_conn = pg_pool.getconn()
    g.cursor = g.pg_conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    g.start_time = datetime.now()


def return_connections():
    """ Return the connection to the Postgres connection pool. """
    g.cursor.close()
    pg_pool.putconn(g.pg_conn)


@app.after_request
def log_outcome(resp):
    """ Outputs to a specified logging file """
    # return db connections first
    return_connections()
    # TODO: log the request and its outcome

    return resp


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/docs')
def docs():
    return render_template('docs.html')


@app.route('/auth')
def auth():
    # TODO: Authenticate user and return page based on whether authentication
    # was successful
    return render_template('auth.html')


if __name__ == '__main__':
    app.run(host=app.config['HOST'])
