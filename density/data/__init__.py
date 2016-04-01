import pandas as pd



def db_to_pandas(conn):
	""" Return occupancy data as pandas dataframe

	column dtypes:
		group_id: int64
		group_name: category
		parent_id: int64
		parent_name: category
		client_count: int64
	index: DateTimeIndex -- dump_time

	Parameters
	----------
	conn: psycopg2.extensions.connection


	Returns
	_______

	pandas.DataFrame

	"""

	df = pd.read_sql('SELECT * FROM density_data', conn) \
		   .set_index("dump_time") \
		   .assign(group_name=lambda df: df["group_name"].astype('category'),
				   parent_name=lambda df: df["parent_name"].astype('category'))

	return df














