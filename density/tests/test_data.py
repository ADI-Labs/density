import io

import pandas as pd
from bokeh.plotting import Figure

from data import db_to_pandas, plot_prediction_point_estimate
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

def test_plot_prediction_point_estimate():

    def fake_predictor(*args, **kwargs):
        return 50

    csv = """
2016-02-26 13:45:00,171.0
2016-02-26 14:00:00,165.0
2016-02-26 14:15:00,159.0
2016-02-26 14:30:00,186.0
2016-02-26 14:45:00,187.0"""

    with io.BytesIO() as fake_file:
        fake_file.write(csv)
        fake_file.seek(0)
        df = pd.read_csv(fake_file, names=["dump_date", "Butler Library 3"]) \
               .assign(dump_date=lambda df: pd.to_datetime(df.dump_date)) \
               .set_index("dump_date")
    series = df["Butler Library 3"]

    figure = plot_prediction_point_estimate(series, fake_predictor)
    assert isinstance(figure, Figure)
