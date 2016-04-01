import pandas as pd

from data import db_to_pandas
from density import pg_pool


def test_db_to_pandas():

    conn = pg_pool.getconn()
    df = db_to_pandas(conn)

    assert df.dtypes["group_id"] == "int64"
    assert df.dtypes["group_name"] == "category"
    assert df.dtypes["parent_id"] == "int64"
    assert df.dtypes["parent_name"] == "category"

    assert df.index.name == "dump_time"
    assert isinstance(df.index, pd.DatetimeIndex)
