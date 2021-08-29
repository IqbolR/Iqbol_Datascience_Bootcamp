##################

# Project_4/unit_4_week_1_hw_Iqbol

##################

library(tidyverse)
library(lubridate)

# Using NOAA weather dataset for ther project and choosed location is Brooklyn, NY USA area within 59 weather station.

NOAA_weather_data="/Users/iqbol.rajabovgmail.com/Desktop/Rework Academy/Projects/Project_4"


#Data Types	
#DAPR - Number of days included in the multiday precipitation total (MDPR)
#SNOW - Snowfall
#WT03 - Thunder
#WT04 - Ice pellets, sleet, snow pellets, or small hail"
#PRCP - Precipitation
#WT05 - Hail (may include small hail)
#TOBS - Temperature at the time of observation
#WT06 - Glaze or rime
#WT08 - Smoke or haze
#SNWD - Snow depth
#WT09 - Blowing or drifting snow
#WT01 - Fog, ice fog, or freezing fog (may include heavy fog)
#TMAX - Maximum temperature
#WT02 - Heavy fog or heaving freezing fog (not always distinguished from fog)
#TAVG - Average Temperature.
#TMIN - Minimum temperature
#MDPR - Multiday precipitation total (use with DAPR and DWPR, if available)

-------------------
# 1. What was the weather in the city you chose on April 10th, 2019?
-------------------

NOAA_weather_data<-read.csv('./NOAA_weather_data.csv')


weather_on_4_10_19<-NOAA_weather_data %>%
  filter(DATE=='2019-04-10') %>%
  group_by(DATE) %>%
  summarise(avg_temp=mean(TAVG, na.rm=T))

# Average temperature on 2019-04-10 was 51.33333 degree.

-------------------
# 2. How many times has it snowed on New Year's Eve in your city?
-------------------
  
NY_snow<-NOAA_weather_data %>%
  select(DATE, SNOW, SNWD) %>%
  separate(DATE, c('year','month','day'), sep='-') %>%
  group_by(year, month, day) %>%
  filter(month=='12' & day=='31') %>%
  summarize(snowing=sum(SNOW, na.rm=T),
            snow_depth=sum(SNWD, na.rm=T))

# There has not snowed on New Year's Eve in Brooklyn, NY USA during 2018-2020

-------------------
# 3. What is the average annual precipitation in the city you chose?
-------------------
  
Ann_prcp<-NOAA_weather_data %>%
  select("DATE","PRCP","MDPR") %>%
  separate(DATE, c('year','month','day'), sep='-') %>%
  group_by(year) %>%
  summarise(avg_prcp=mean(PRCP, na.rm=T),
            ave_multiday_prcp=mean(MDPR, na.rm=T))

# Annually average precipitation & Multiday precipitation:
# Year     PRCP       Multiday_PRCP(MDPR) 
# 2018 - 0.1764740      0.7889888
# 2019 - 0.1543744      0.6565625
# 2020 - 0.1283399      0.7808772
# 2021 - 0.1524687      1.6680435

