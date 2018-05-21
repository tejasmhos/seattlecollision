BEFORE

SELECT build_id, build_lat, build_long, build_start_dt, build_end_dt, 
count(coll_id) as num_collisions
FROM radius
WHERE build_start_dt LIKE '%2015%' 
	AND radius < 1000
	AND date(coll_id) BETWEEN date('build_start_dt', '-6 months') AND date('build_start_dt')
GROUP BY build_id, build_lat, build_long, build_start_dt, build_end_dt

DURING






AFTER

SELECT build_id, build_lat, build_long, build_start_dt, build_end_dt, count(coll_id) as num_collisions
FROM radius
WHERE build_start_dt LIKE '%2016%' 
	AND date(coll_dt) BETWEEN date(build_start_dt, '-6 months') AND date(build_start_dt)
GROUP BY build_id, build_lat, build_long, build_start_dt, build_end_dt;

select count(*) from (
select build_id, build_lat, build_long, build_end_dt, build_start_dt, count(coll_id) as num_collisions
from radius
where build_start_dt like '%2013%' 
and date(coll_dt) between date(build_start_dt, '-6 months') and date(build_start_dt)
group by build_id, build_lat, build_long, build_end_dt, build_start_dt);