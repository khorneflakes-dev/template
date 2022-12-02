-- Active: 1669318589555@@34.176.218.33@3306@projectyelp
show tables;

/* porcentaje de cambio del promedio de estrellas anio por anio y por categoria */
select avg(stars), id_business, year from reviews limit 4;
select * from business limit 10;
select b.name, b.address, b.latitude, b.longitude, cs.city, cs.state, b.stars, b.review_count,
h.Monday, h.Tuesday, h.Wednesday, h.Thursday, h.Friday, h.Saturday, h.Sunday
from business b
left join business_city_state cs on b.city_state_id = cs.city_state_id
left join business_hours h on b.hours_id = h.hours_id
where b.business_id in 
(82302, 85227, 36756, 53128, 35083, 80458, 93168, 94845, 54722, 66136, 88264, 81856, 71874, 48823, 57224, 
84459, 82701, 57078, 51714, 62156, 37492, 60558, 37226, 66452, 5159, 53510, 88169, 81761, 87325, 79638)
 and b.stars > 3.5;

select * from business limit 10;
 select * from business_city_state limit 10;

select * from business_hours limit 10;

select name from user_names where id_user = 201;