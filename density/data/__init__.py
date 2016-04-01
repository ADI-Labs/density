import pandas as pd



def db_to_pandas(conn):

	df = pd.read_sql('SELECT * FROM density_data', conn) \
		   .set_index("dump_time") \
		   .assign(group_name=lambda df: df["group_name"].astype('category'),
				   parent_name=lambda df: df["parent_name"].astype('category'))

	return df