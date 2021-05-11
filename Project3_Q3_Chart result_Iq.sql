
		------ Unit 3 week 1 project (Project 3)_Iqbol

---- 1. What are the top 5 metros by population?

select * 
from (select metro_city, sum(population) as total_population, 
	rank () over (order by sum(population) desc) as population_rank
	from public.census_metro_data_exp
	group by 1
	order by 2 desc) final_rank 
where population_rank < 6

	---- Answer: The top 5 metros are 
	---- 1. New York with population - 15.3, 
	---- 2. Los Angeles with population 11.4, 
	---- 3. Chicago with population - 6.5, 
	---- 4. Houston with population - 5.7,
	---- 5. Dallas with population - 5.4

-------------------------------------------------------
------ 2nd query to answer the question

select metro_city, sum(population) as total_population
from census_metro_data_exp 
group by 1
order by 2 desc
-------------------------------------------------------


---- 2. For those metro areas, what does the spread of median_hh_income look like?

select metro_city, 
floor(median_hh_income/5000)*5000 as income_bin, count(distinct zip) as total_zip_codes
from public.census_metro_data_exp
where zip > 0 and metro_city in ('New York', 'Los Angeles', 'Chicago', 'Houston', 'Dallas')  
group by 1,2
order by 1
	
	---- Answer: Google sheet chart_
	

---- 3. For those metro areas, what does the spread of student % look like?

---- select *  from public.census_metro_data_exp cmde ----

select metro_city, floor(percent_of_students) as student_population_bin, count(*)
from (select metro_city, ((population_age_5_9 + population_age_10_14 + population_age_15_17)::numeric/population::numeric)*100 as percent_of_students
	from public.census_metro_data_exp
	where population > 0 and metro_city in ('New York', 'Los Angeles', 'Chicago', 'Houston', 'Dallas')) base_query 
group by 1,2
order by 1,2

---- Answer: Google sheet chart_



---- 4. Which zip codes in each metro area should receive the most federal funding?


select *
from (select population.metro_city, population.zip, population.population as total_population, percent_of_students, median_income, 
	rank () over (partition by population.metro_city order by student_population_rank + income_rank desc ) as overall_rank
	
from (select metro_city, zip, population, round((population_age_5_9+population_age_10_14+population_age_15_17)::numeric/population::numeric, 4)*100 as percent_of_students, 
	rank () over (partition by metro_city order by ((population_age_5_9+population_age_10_14+population_age_15_17)::numeric/population::numeric)*100) as student_population_rank
	from public.census_metro_data_exp
	where population > 0 and metro_city in ('New York', 'Los Angeles', 'Chicago', 'Houston', 'Dallas')) population

	inner join (select metro_city, zip, median_hh_income as median_income, 
				rank () over (partition by metro_city order by median_hh_income desc) as income_rank
				from public.census_metro_data_exp
				where population > 0 and metro_city in ('New York', 'Los Angeles', 'Chicago', 'Houston', 'Dallas')) as income on 
population.metro_city=income.metro_city and population.zip=income.zip) base_query
where overall_rank <6

------ Answer: Google sheet chart_