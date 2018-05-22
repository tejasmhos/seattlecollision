#Framework for the three queries to pull the data for the before, during, after maps.

import pandas as pd
import sqlite3
import numpy as np
from datetime import datetime

def create_default_query(file_path):
    import pandas as pd
    import sqlite3
    sample_db = sqlite3.connect(file_path)
    before_query = pd.read_sql_query("""
    	SELECT build_id, build_lat, build_long, build_start_dt, build_end_dt,
		count(coll_id) as num_collisions
		FROM radius
		WHERE build_start_dt LIKE '%2015%' 
			AND date(coll_dt) BETWEEN date(build_start_dt, '-6 months') AND date(build_start_dt)
			AND radius < 1500
		GROUP BY build_id, build_lat, build_long, build_start_dt, build_end_dt;
		""", sample_db)
    during_query = pd.read_sql_query("""
		SELECT build_id, build_lat, build_long, build_start_dt, build_end_dt,
		count(coll_id) as num_collisions
		FROM radius
		WHERE build_start_dt LIKE '%2015%' 
			AND date(coll_dt) BETWEEN date(build_start_dt) AND date(build_end_dt)
			AND radius < 1500
		GROUP BY build_id, build_lat, build_long, build_start_dt, build_end_dt;
		""", sample_db)
    after_query = pd.read_sql_query("""
		SELECT build_id, build_lat, build_long, build_start_dt, build_end_dt, count(coll_id) as num_collisions
		FROM radius
		WHERE build_start_dt LIKE '%2015%' 
			AND date(coll_dt) BETWEEN date(build_end_dt) AND date (build_end_dt, '+6 months')
			AND radius < 1500
		GROUP BY build_id, build_lat, build_long, build_start_dt, build_end_dt;
		""", sample_db)
    sample_db.close()
    return before_query, during_query, after_query



before_df, during_df, after_df = create_default_query('sample.db')

before_df['build_start_dt'] = pd.to_datetime(before_df['build_start_dt'])
before_df['build_end_dt'] = pd.to_datetime(before_df['build_end_dt'])
during_df['build_start_dt'] = pd.to_datetime(during_df['build_start_dt'])
during_df['build_end_dt'] = pd.to_datetime(during_df['build_end_dt'])
after_df['build_start_dt'] = pd.to_datetime(after_df['build_start_dt'])
after_df['build_end_dt'] = pd.to_datetime(after_df['build_end_dt'])

months = 6
before_df['norm_collisions'] = before_df['num_collisions']/((np.timedelta64(1, 'D')*months*365/12).astype(int))
after_df['norm_collisions'] = after_df['num_collisions']/((np.timedelta64(1, 'D')*months*365/12).astype(int))
during_df['norm_collisions'] = (during_df['num_collisions']/
                                ((during_df['build_end_dt'] - during_df['build_start_dt']) / 
                                 np.timedelta64(1, 'D')).astype(int))

before_df.to_csv('default_before_df.csv')
during_df.to_csv('default_during_df.csv')
after_df.to_csv('default_after_df.csv')

