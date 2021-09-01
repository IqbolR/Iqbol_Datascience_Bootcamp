===============
  
Project_5_Hypothesis_Test

===============

library(tidyverse)
library(lubridate)
library(report)

Census_metro_dataset="/Users/iqbol.rajabovgmail.com/Desktop/Rework Academy/Projects/Project_5"

#Pulling csv file
-----------------
Census_metro_data_exp<-read.csv('/Users/iqbol.rajabovgmail.com//Desktop/Rework Academy/Projects/Project_5/census_metro_data.csv')

# Data consist of:
# Zip - Zip codes
# median_hh_income - Median household income
# Percent_under_18 - Percent of population aged 0-17
# Percent_70_to_80 - Percent of population aged 70-80

-----------------
# 1. What is the average median_hh_income of the two zip code groups? 
-----------------
avg_income_groups<-Census_metro_data_exp %>%
  group_by(population_bucket) %>%
  summarize(avg_income=mean(median_hh_income, na.rm=T))

# Average median_hh_income:
# high_under_18 = 66274.71
# high_70_80 = 67853.00

-----------------
# 2. What is the standard deviation of the median_hh_income in the two groups? 
-----------------
std_dev_groups<-Census_metro_data_exp %>%
  group_by(population_bucket) %>%
  summarize(stand_dev=sd(median_hh_income, na.rm=T))

# high_under_18 = 32725.64
# high_70_80 = 27157.64

# Hypothesis:
        ## null: metro area with a high % of children will have higher median household incomes then those zip codes with a high % of those 70-80
        ## alternative: metro area with a high % of children "will not have" higher median household incomes then those zip codes with a high % of those 70-80

# lets plot the data first before we run t-test

ggplot(Census_metro_data_exp, aes(x=population_bucket, y=median_hh_income)) +
  geom_boxplot() +
  theme_classic()

# 3. Run a two sample T-Test to test your hypothesis? 

pop_high_under_18<-Census_metro_data_exp %>% 
  filter(population_bucket=='high_under_18')

pop_high_70_80<-Census_metro_data_exp %>% 
  filter(population_bucket=='high_70_80')

var<-var.test(pop_high_under_18$median_hh_income, pop_high_70_80$median_hh_income)

if(var$p.value < .05) {
  var=T
} else { 
  var=F}

test<-t.test(pop_high_under_18$median_hh_income,pop_high_70_80$median_hh_income, var.equal=var)

report(test)

# 2nd scenario function to test our hypothesis:
# test<-t.test(median_hh_income ~ population_bucket, data = Census_metro_data_exp, var.equal = TRUE, paired = FALSE)
# report(test)  # we get exactly the same result as 1st scenario testing function.


# 4. Can you reject the null hypothesis? Why or why not? What does this tell you about your findings?

# The p-value is 0.04572 so at the 5% significance level we reject the null hypothesis of equal means, meaning that we can conclude that the metro area with a high % of children will have higher median household incomes then those zip codes with a high % of those 70-80.

# Because the P-value = 0.04572 we get is lower than 0.05 which is unlikely that two sample means are equal(but small difference). Which means that we have very low chance that 
# the averages of two samples are different.

# Test report:
# The Two Sample t-test testing the difference between pop_high_under_18$median_hh_income and pop_high_70_80$median_hh_income (mean in group high_under_18 = 66274.71, mean in group high_70_80 = 67853.00) suggests that the effect is negative, statistically significant, and very small (difference = -1578.28, 95% CI [-3126.51, -30.06], t(5753) = -2.00, p = 0.046; Cohen's d = -0.05, 95% CI [-0.10, -1.00e-03])

