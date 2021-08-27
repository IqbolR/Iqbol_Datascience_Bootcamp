====================

Project 6 Regression

====================


import pandas as pd
import numpy as np
from plotnine import *
from pydataset import data
import statsmodels.formula.api as smf
from scipy import stats as st


----------------------------------
# Extracting data
----------------------------------

women_employment=data("Mroz")


# A dataframe contains 753 - rows & 18 columns such as:

# work - work at home
# hoursw - wife's hours of work in 1975
# child6 - number of children less than 6 years old in household 
# child618 - number of children between ages 6 and 18 in household 
# agew - wife's age
# educw - wife's educational attainment, in years
# hearnw - wife's average hourly earnings, in 1975 dollars
# wagew - wife's wage reported at the time of the 1976 interview 
# hoursh - husband's hours worked in 1975
# ageh - husband's age
# educh - husband's educational attainment, in years
# wageh - husband's wage, in 1975 dollars
# income - family income, in 1975 dollars
# educwm - wife's mother's educational attainment, in years
# educwf - wife's father's educational attainment, in years
# unemprate - unemployment rate in county of residence, in percentage points
# city - lives in large city (SMSA) ?
# experience - actual years of wife's previous labor market experience


----------------------------------
# Define plot themes 
----------------------------------

custom_theme=theme(panel_background = element_rect(fill = 'white'), 
          panel_grid_major = element_line(colour = 'grey', size=0.5, linetype='dashed'), 
          panel_border = element_rect(fill=None, color='grey', size=0.5, linetype='solid')
    )

----------------------------------
# Creating a plot
----------------------------------
# lets see relationship between variables wife's wage and wife's hours of work

(
    ggplot(women_employment) +
    geom_point(aes(x ='wagew', 
                   y='hoursw'),
              color='blue') + 
    labs(
        title ='Relationship between Womens wage and Womens work hours',
        x = 'womens wage',
        y = 'womens work hours') + 
    custom_theme
    )


----------------------------------
# Hypothesis
----------------------------------

# Lets see how variables in the data set will predict women's hours of work

----------------------------------
# The OLS estimation for multiple regression
----------------------------------

est = smf.ols(formula='hoursw ~ work + child6 + child618 + agew + educw + hearnw + wagew + hoursh + ageh + educh + wageh + income + educwm + educwf + unemprate + city + experience', data=women_employment).fit() 

est.summary()



# Regression looks like: 
# hoursw = 2142.6814 - 1065.5361*work - 125.6861*child6 - 46.1696*child618 - 9.5316*agew - 15.7344*educw - 59.9066*hearnw + 87.1417*wagew - 0.1483*hoursh - 2.3518*ageh - 4.6509*educh - 53.4704*wageh + 0.0228*income + 6.2323*educwm - 5.8947*educwf - 7.3138*unemprate - 8.8607*city + 15.6267*experience + e

# R-sq - 0.664. 66.4% of variance explained by OLS model.

# P>[t]:
#       variables are statistically significant: work, child6, child618, hearnw, wagew, hoursh, wageh, income, experience - P>[t] = 0.000 which is lower than 0.05 = type1 error
#       variables are not statistically significant: city, agew, educw, ageh, educh, educwm, educwf, unemprate

# Coef for variables:
#                    Positive coef: wagew, experience, educwm, income 
#                    Negative coef: work, child6, child618, agew, educw, hearnw, hoursh, ageh, educh, wageh, educwf, unemprate, city


# According OLS model:
#       Women's with high expreience, high value wage, high family income and wife's mother's educational attainment increased their work hours, ie when women's wage grows in one point value then women's working hours increasing to 87.14 hour points.
#       Variables: work, child6, child618, agew, educw, hearnw, hoursh, ageh, educh, wageh, educwf, unemprate, city impact negative to women's work hours, ie number of children under 6 years old strongly descrease women's working hours to 125.68 hour points.




