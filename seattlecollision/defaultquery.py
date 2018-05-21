#Framework for the three queries to pull the data for the before, during, after maps.

import pandas as pd
import sqlite3

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

before_df, during_query, after_query = create_default_query('sample.db')