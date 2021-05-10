---------- 1. Which campaign typically has the highest cost each year?

select year, campaign, avg_cost
from(select year, campaign, avg_cost, 
rank()over (partition by year order by avg_cost desc) as campaign_cost_rank 
from (select date_part('year',date) as year, sac.campaign, round(avg(cost)) as avg_cost
	from public.search_ad_data sad
	inner join public.search_ad_campaigns sac on sad.campaign_id=sac.campaign_id
	group by 1,2) nesty_query_campaign_cost_rank) end_campaign_cost_rank
where campaign_cost_rank = 1
order by 1 desc


---- Answer: Ladder_collection_has_the_highest_cost


---------- 2. Which campaign typically has the lowest cost per conversion each year.

select year, campaign, cost_per_conversion
from (select year, campaign, cost_per_conversion,
rank () over (partition by year order by cost_per_conversion) as campaign_cost_per_conversion_rank 
from (select date_part('year',date) as year, sac.campaign, round(sum(sad.cost)/sum(sad.conversions)) as cost_per_conversion
	from public.search_ad_data sad
	inner join public.search_ad_campaigns sac on sad.campaign_id=sac.campaign_id
	group by 1,2) nesty_query_cpc_rank) end_cost_per_convesion_rank
where campaign_cost_per_conversion_rank = 1
order by 1,2

--- Answer: Mostly desk_organization has the lowest cost per conversion as of 2018 and 2021.



---------- 3. What is the year over year trend in campaign costs?

select date_part('year',date) as year, sac.campaign, round(avg(cost)) as avg_cost 
from public.search_ad_data sad
inner join public.search_ad_campaigns sac on sad.campaign_id=sac.campaign_id
group by 1,2

--- Answer: Total year over year average cost by campaign from 2017 to 2021
---https://docs.google.com/spreadsheets/d/1RSWPBwZuQxUHhrkbVaHeviJHs3iwf2sJT0aosJrgYRE/edit#gid=1965895



---------- 4. What is the year over year trend in CPC?
		
select date_part('year',date) as year, sac.campaign, round(sum(sad.cost)/sum(sad.conversions)) as cost_per_conversion
from public.search_ad_data sad
inner join public.search_ad_campaigns sac on sad.campaign_id=sac.campaign_id
group by 1,2

--- Answer: Total year over year cpc from 2017 to 2021
---https://docs.google.com/spreadsheets/d/1RSWPBwZuQxUHhrkbVaHeviJHs3iwf2sJT0aosJrgYRE/edit#gid=1965895


		
---------- 5. Create a view
		
CREATE OR REPLACE VIEW public.vw_campaign_cost_rank_IqbolR as

select year, campaign, avg_cost
from(select year, campaign, avg_cost, 
rank()over (partition by year order by avg_cost desc) as campaign_cost_rank 
from (select date_part('year',date) as year, sac.campaign, round(avg(cost)) as avg_cost
	from public.search_ad_data sad
	inner join public.search_ad_campaigns sac on sad.campaign_id=sac.campaign_id
	group by 1,2) nesty_query_campaign_cost_rank) end_campaign_cost_rank
where campaign_cost_rank = 1
order by 1 desc


select *
from public.vw_campaign_cost_rank_IqbolR
