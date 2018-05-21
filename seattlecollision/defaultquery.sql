BEFORE

SELECT build_id, build_lat, build_long, build_start_dt, build_end_dt,
count(coll_id) as num_collisions
FROM radius
WHERE build_start_dt LIKE '%2015%' 
	AND date(coll_dt) BETWEEN date(build_start_dt, '-6 months') AND date(build_start_dt)
	AND radius < 1500
GROUP BY build_id, build_lat, build_long, build_start_dt, build_end_dt;

DURING

SELECT build_id, build_lat, build_long, build_start_dt, build_end_dt,
count(coll_id) as num_collisions
FROM radius
WHERE build_start_dt LIKE '%2015%' 
	AND date(coll_dt) BETWEEN date(build_start_dt) AND date(build_end_dt)
	AND radius < 1500
GROUP BY build_id, build_lat, build_long, build_start_dt, build_end_dt;

AFTER

SELECT build_id, build_lat, build_long, build_start_dt, build_end_dt, count(coll_id) as num_collisions
FROM radius
WHERE build_start_dt LIKE '%2015%' 
	AND date(coll_dt) BETWEEN date(build_end_dt) AND date (build_end_dt, '+6 months')
	AND radius < 1500
GROUP BY build_id, build_lat, build_long, build_start_dt, build_end_dt;