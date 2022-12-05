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

select * from reviews limit 10;
ORDER BY CASE
            WHEN reply IS NULL THEN 1  
            ELSE 0 
         END, category;

SELECT year, stars,
CASE WHEN stars > 3 THEN 'greater than 3'
ELSE 'less than 3'
END AS QuantityText
FROM reviews  limit 10;
/* stars | year | stars_q | count(reviews) */
select stars, count(stars) from business group by stars limit 10;

select * from reviews limit 10;
/* case when r.stars > 3 then 'greater than 3' else 'less than 3' end as stars_q */
select count(r.id_review) as review_per_year, cs.state
from reviews r
left join business b on r.id_business = b.business_id
left join business_categories bc on b.categories_id = bc.categories_id
left join business_city_state cs on b.city_state_id = cs.city_state_id
where year = 2019
group by cs.state;
/* where r.year > 2020 and bc.p_categorie = 'Restaurants' group by stars_q, year, cs.state order by year desc limit 10; */

select count(b.business_id), cs.state from business b left join business_city_state cs on b.city_state_id = cs.city_state_id limit 10;

select count(r.id_review) as reviews_per_year, bc.p_categorie, year from reviews r 
left join business b on r.id_business = b.business_id
left join business_categories bc on b.categories_id = bc.categories_id
where bc.p_categorie not in ('Community Service/Non-Profit','Food Banks', 'Religious Organizations', 'Local Services') group by bc.p_categorie, year order by reviews_per_year desc;

show tables;
show databases;
select distinct(`Monday`) from business_hours;

select count(DISTINCT(state)) from business_city_state limit 10;

select count(b.business_id) as business_per_state, cs.state from business b
left join business_city_state cs on b.city_state_id = cs.city_state_id group by cs.state order by business_per_state desc;

