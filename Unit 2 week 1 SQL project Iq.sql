--- Unit 2 week 1 SQL Project Iqbol Rajabov

--- Which metro area in the contry has the highest average household incom in the US?

select metro_city, avg(median_hh_income) as avg_hh_income
from public.census_metro_data cmd 
group by metro_city 
order by 2 desc 

--- Bridgeport




---What metro area has the zip code with the largest population? 

select metro_city, zip as zip_code, population 
from public.census_metro_data cmd 
group by 1, 2, 3
order by 3 desc  

--- Houston




--- What state has the most metro areas?

select *
from public.census_metro_data cmd 

select state, count(distinct metro_city) as total_metro_city
from public.census_metro_data cmd 
group by 1
order by 2 desc 

--- CA



--- Which metro area has the largest proportion of people aged 70-97?

select metro_city, population_age_70_74, population_age_75_79
from public.census_metro_data cmd 
group by 1, 2, 3
order by 2  desc 

--- Phoenix