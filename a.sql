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



/* julio */
/* 1.  */

/* grafica 1 con filtro de anios solamente */
select bce.state, bc.p_categorie , r.stars , count(r.id_review) as conteo_rev
from reviews r 
join business b on(r.id_business = b.business_id) 
join business_categories bc on(b.categories_id = bc.categories_id)
join business_city_state bce on (b.city_state_id = bce.city_state_id)
where r.year >= 2017 and r.year <=2022
group by bce.state, bc.p_categorie , r.stars 
order by bce.state, bc.p_categorie, r.stars;





show tables;





/* grafica 2  con filtro de categorias eg. restaurantes*/
select bce.state, bc.p_categorie , r.stars , count(r.id_review) as conteo_rev
from reviews r 
join business b on(r.id_business = b.business_id) 
join business_categories bc on(b.categories_id = bc.categories_id)
join business_city_state bce on (b.city_state_id = bce.city_state_id)
where r.year >= 2017 and r.year <=2022 and bc.p_categorie = 'Restaurants' and bce.state = 'LA'
group by bce.state, bc.p_categorie , r.stars 
order by bce.state, bc.p_categorie, r.stars;


/* del total de reviews calcular una columna con el porcentaje de 4 o n estrellas */

/* state| # reviews 4> stars | # total reviews | percentage */

select * from business;
show tables;

select bce.state, r.stars , count(r.id_review) as conteo_rev
    from reviews r
    join business b on(r.id_business = b.business_id)
    join business_categories bc on(b.categories_id = bc.categories_id)
    join business_city_state bce on (b.city_state_id = bce.city_state_id)
    where r.year >=2010 and r.year <=2021 and bc.p_categorie in ('Active Life', 'Arts & Entertainment', 'Beauty & Spas' , 'Food', 'Hotels & Travel','Nightlife','Restaurants') and bce.state in ('AZ', 'CA', 'DE', 'FL', 'ID', 'IL', 'IN', 'LA', 'MO', 'NJ', 'NV', 'PA', 'TN')
    group by bce.state , r.stars
    order by bce.state, r.stars;


/* heatmap */

select bce.state, r.year, count( distinct business_id)  as count_business
    from reviews r 
    join business b on(r.id_business = b.business_id) 
    join business_categories bc on(b.categories_id = bc.categories_id)
    join business_city_state bce on (b.city_state_id = bce.city_state_id)
    where b.stars >=4 and r.year >=2010 and r.year <=2021 and bc.p_categorie in ('Active Life', 'Arts & Entertainment', 'Beauty & Spas' , 'Food', 'Hotels & Travel','Nightlife','Restaurants') and bce.state in ('AZ', 'CA', 'DE', 'FL', 'ID', 'IL', 'IN', 'LA', 'MO', 'NJ', 'NV', 'PA', 'TN')
    group by bce.state, r.year
    order by bce.state, r.year;


select bce.state, r.year, count( distinct business_id)  as count_business
from reviews r 
join business b on(r.id_business = b.business_id) 
join business_categories bc on(b.categories_id = bc.categories_id)
join business_city_state bce on (b.city_state_id = bce.city_state_id)
where b.stars >=4 and r.year >=2017 and r.year <=2021 and bc.p_categorie = 'Food' and bce.state in ('AZ', 'CA', 'DE', 'FL', 'ID', 'IL', 'IN', 'LA', 'MO', 'NJ', 'NV', 'PA', 'TN')
group by bce.state, r.year
order by bce.state, r.year;

select bce.state, r.stars , count(r.id_review) as conteo_rev
        from reviews r
        join business b on(r.id_business = b.business_id)
        join business_categories bc on(b.categories_id = bc.categories_id)
        join business_city_state bce on (b.city_state_id = bce.city_state_id)
        where r.year >=2010 and r.year <=2021 and bc.p_categorie in ('Active Life', 'Arts & Entertainment', 'Beauty & Spas' , 'Food', 'Hotels & Travel','Nightlife','Restaurants') and bce.state in ('AZ', 'CA', 'DE', 'FL', 'ID', 'IL', 'IN', 'LA', 'MO', 'NJ', 'NV', 'PA', 'TN')
        group by bce.state , r.stars
        order by bce.state, r.stars;


/* para saber la cantidad de negocios cerrados por anio y por categoria con filtro de anios y categoria */

/* cantidad de negocios cerrados por estado  */
select r.year ,count(distinct b.business_id) as business_close, bc.p_categorie
from reviews r 
join business b on(r.id_business = b.business_id) 
join business_categories bc on(b.categories_id = bc.categories_id)
join business_city_state bce on (b.city_state_id = bce.city_state_id)
where b.is_open = 0 and r.year >= 2010 and r.year <=2021 and bc.p_categorie in ('Active Life', 'Arts & Entertainment', 'Beauty & Spas' , 'Food', 'Hotels & Travel','Nightlife','Restaurants')
and bce.state in ('AZ', 'CA', 'DE', 'FL', 'ID', 'IL', 'IN', 'LA', 'MO', 'NJ', 'NV', 'PA', 'TN')
group by r.year, bc.p_categorie;

/* cantidad total de negocios  */
select r.year ,count(distinct b.business_id) as total_business, bc.p_categorie
from reviews r 
join business b on(r.id_business = b.business_id) 
join business_categories bc on(b.categories_id = bc.categories_id)
join business_city_state bce on (b.city_state_id = bce.city_state_id)
where r.year >= 2010 and r.year <=2021 and bc.p_categorie in ('Active Life', 'Arts & Entertainment', 'Beauty & Spas' , 'Food', 'Hotels & Travel','Nightlife','Restaurants')
and bce.state in ('AZ', 'CA', 'DE', 'FL', 'ID', 'IL', 'IN', 'LA', 'MO', 'NJ', 'NV', 'PA', 'TN')
group by r.year, bc.p_categorie;



/* spline */
create or replace view date_closed as
select b.business_id, bc.p_categorie, max(r.year) as final_year
from reviews r
join business b on(r.id_business = b.business_id)
join business_categories bc on(b.categories_id = bc.categories_id)
join business_city_state bce on (b.city_state_id = bce.city_state_id)
where b.is_open=0 and bc.p_categorie in ('Active Life', 'Arts & Entertainment', 'Beauty & Spas' , 'Food', 'Hotels & Travel','Nightlife','Restaurants') and bce.state in ('AZ', 'CA', 'DE', 'FL', 'ID', 'IL', 'IN', 'LA', 'MO', 'NJ', 'NV', 'PA', 'TN')
group by b.business_id;

select final_year as year , p_categorie ,count(business_id) as business_close from date_closed group by final_year, p_categorie order by p_categorie, final_year;

select r.year ,count(distinct b.business_id) as total_business, bc.p_categorie
from reviews r 
join business b on(r.id_business = b.business_id) 
join business_categories bc on(b.categories_id = bc.categories_id)
join business_city_state bce on (b.city_state_id = bce.city_state_id)
where r.year >= 2010 and r.year <=2021 and bc.p_categorie in ('Active Life', 'Arts & Entertainment', 'Beauty & Spas' , 'Food', 'Hotels & Travel','Nightlife','Restaurants')
and bce.state in ('AZ', 'CA', 'DE', 'FL', 'ID', 'IL', 'IN', 'LA', 'MO', 'NJ', 'NV', 'PA', 'TN')
group by r.year, bc.p_categorie;


/* top close */
select b.name, count(b.business_id) as top_close from business b 
join business_categories bc on(b.categories_id = bc.categories_id)
join business_city_state bce on (b.city_state_id = bce.city_state_id)
where b.is_open = 0 and bc.p_categorie in ('Active Life', 'Arts & Entertainment', 'Beauty & Spas' , 'Food', 'Hotels & Travel','Nightlife','Restaurants')
and bce.state in ('AZ', 'CA', 'DE', 'FL', 'ID', 'IL', 'IN', 'LA', 'MO', 'NJ', 'NV', 'PA', 'TN')
group by b.name order by top_close desc;

select b.name, count(b.business_id) as total from business b 
join business_categories bc on(b.categories_id = bc.categories_id)
join business_city_state bce on (b.city_state_id = bce.city_state_id)
where bc.p_categorie in ('Active Life', 'Arts & Entertainment', 'Beauty & Spas' , 'Food', 'Hotels & Travel','Nightlife','Restaurants')
and bce.state in ('AZ', 'CA', 'DE', 'FL', 'ID', 'IL', 'IN', 'LA', 'MO', 'NJ', 'NV', 'PA', 'TN')
group by b.name order by total desc;