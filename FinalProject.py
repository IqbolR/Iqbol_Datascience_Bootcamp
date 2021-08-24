==============================

    # Final Project -----

==============================

# Using S&P_500 data set. 
# Source of data: 
#           I took data set from the "ONLINE DATA ROBERT SHILLER" which he with several colleagues collected to examine long term historical trends in the US market.
#           http://www.econ.yale.edu/~shiller/data.htm


import pandas as pd
from plotnine import *
import statsmodels.formula.api as smf
from scipy import stats as st
import statistics
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.stats.proportion import proportions_ztest
from sklearn.cluster import KMeans

----------------------------------
# Define plot themes 
----------------------------------

custom_theme=theme(panel_background = element_rect(fill = 'white'), 
          panel_grid_major = element_line(colour = 'grey', size=0.5, linetype='dashed'), 
          panel_border = element_rect(fill=None, color='grey', size=0.5, linetype='solid')
    )

----------------------------------
# Pull in S&P_500 data
----------------------------------

S_and_P_500=pd.read_csv('/Users/iqbol.rajabovgmail.com/Desktop/Final_Project/ie_data.csv')


S_and_P_500.info()

S_and_P_500.describe()


----------------------------------
# Grouping monthly data set into year 
----------------------------------
#S_and_P_500['year']=pd.to_datetime(S_and_P_500.Date).dt.to_period('Y').dt.to_timestamp()
#S_and_P_500['year']=S_and_P_500['year'].apply(lambda x: x.year)

----------------------------------
# Replacing Nan values
----------------------------------

#S_and_P_500['Earnings_E']=S_and_P_500['Earnings_E'].fillna(0)
#S_and_P_500['S_and_P_Comp_P']=S_and_P_500['S_and_P_Comp_P'].fillna(0)


#S_and_P_500=S_and_P_500[S_and_P_500.Earnings_E.notnull()]
#S_and_P_500=S_and_P_500[S_and_P_500.S_and_P_Comp_P.notnull()]

----------------------------------
# Dropping Nan values
----------------------------------

S_and_P_500=S_and_P_500.dropna()

----------------------------------
# General plot of SP500 price by year for the period 1871-2021
----------------------------------

(
    ggplot(S_and_P_500) +
    geom_line(aes(x = 'Date', 
                   y='S_and_P_Comp_P'),
              color='blue') + 
    geom_line(aes(x = 'Date', 
                   y='Earnings_E'),
              color='red') + 
    geom_line(aes(x = 'Date', 
                   y='Dividend_D'),
              color='green')+
    labs(
        title ='S&P_Comp_P and Earnings in Period 1871-2021',
        x = 'year',
        y = 'S&P_Comp_P(blue) /' 'Earnings(red) / Dividend(green)') + 
    custom_theme
    )

# We can see SP500 price has been growen up for the period 1871 - 2021 on average permanently (especially jumping faster after 1990th) also we can see Earnings and Dividends are getting high value as well within S&P_price 

----------------------------------
# Lets see what the relationship between variables (Price & Earnings) looks like.
----------------------------------

# Pearson Correlation Coefficient 

corr, _ = st.pearsonr(S_and_P_500['Earnings_E'], S_and_P_500['S_and_P_Comp_P'])

print('Pearsons correlation: %.3f' % corr)

# We can see strong correlation between Earnings and S&P500 price and the corr_coef = 0.941


----------------------------------
# Creating a plot between variables Earnings and S&P500 price
----------------------------------

(
    ggplot(S_and_P_500) +
    geom_point(aes(x = 'S_and_P_Comp_P', 
                   y='Earnings_E'),
              color='blue') + 
    labs(
        title ='Earnings in S&P_Comp_P',
        x = 'S&P_Comp_P',
        y = 'Earnings',
    ) + 
    custom_theme
    )

# Strong relationship between variables, when S&P500_price raising up - Earnings is getting high value accordingly.



==============================

#  Running unsupervised model

----------------------------------
# K-Means Clusters
----------------------------------

# Lets see our data set in three clusters how it's look like

kmeans = KMeans(n_clusters=3)

kmeans_model = kmeans.fit(S_and_P_500[['S_and_P_Comp_P','Earnings_E']])

S_and_P_500['cluster'] = kmeans_model.predict(S_and_P_500[['S_and_P_Comp_P','Earnings_E']])


----------------------------------
# Plotting clusters
----------------------------------
(
    ggplot(S_and_P_500) +
    geom_point(aes(x = 'S_and_P_Comp_P', 
                   y='Earnings_E', color='cluster')) + 
    labs(
        title ='Earnings in S&P_Comp_P',
        x = 'S&P_Comp_P',
        y = 'Earnings',
    ) + 
    custom_theme
    )

# So we can desribe our plot by 3 clusters, that: 
    # Cluster#1 - low price and low earnings, 
    # Cluster#2 - Medium price and higher earnings 
    # Cluster#3 - Medium&High price and Low&High earnings. I would like to mention that most of data are in cluster#3. 

----------------------------------
# Hypothesis
----------------------------------

# How does Price, Dividends, Consumer Price Index, Long interest rate impact Eranings to get max a point

# Let see how much max Earnings could be predicted by other variables from our data set

# Lets use regression model for prediction Earnings for our data set


----------------------------------
# Regression
----------------------------------

# First lets looks at the linear relationship of variables

(
    ggplot(S_and_P_500) +
    geom_point(aes(x = 'S_and_P_Comp_P', 
                   y='Earnings_E'), 
               color='blue') + 
    geom_smooth(aes(x = 'S_and_P_Comp_P',
                    y = 'Earnings_E'), 
                method='lm'
    ) +
    labs(
        title ='Earnings in S&P_Comp_P',
        x = 'S&P_Comp_P',
        y = 'Earnings',
    )+
    custom_theme
    )

----------------------------------
# The OLS estimation for regression
----------------------------------

est = smf.ols(formula='Earnings_E ~ Date + S_and_P_Comp_P + Dividend_D + Consumer_Price_Index_CPI + Long_Interest_Rate_GS10', data=S_and_P_500).fit() 

est.summary()


# R-sq - 0.905. 90.5% of variance explained by OLS model is strong enough.

# P>[t]:
#       all variables are statistically significant P>[t] = 0.000 which is lower than 0.05 = type1 error

# Coef for variables:
#                    Date, S_and_P_Comp_P, Dividend_D, Long_Interest_Rate_GS10 has positive coef 
#                    Consumer_Price_Index_CPI has negative coef

# Regression looks like: 
#       Earnings = -31.2335 + 0.0152*Date + 0.0339*S_and_P_Comp_P + 0.8531*Dividend - 0.0456*Consumer_Price_Index_CPI + 0.7314*Long_Interest_Rate_GS10 + e. 



----------------------------------
# Splitting data to train and test sets as 70/30
----------------------------------

# Lets split our data frame into training, and test data sets to identify the accuracy of the prediction

----------------------------------
# Training data set with 70% of data
----------------------------------

SP500_train_70=S_and_P_500.sample(frac=0.70)

----------------------------------
# Testing data set with other 30% of data
----------------------------------

SP500_test_30=S_and_P_500.drop(SP500_train_70.index)


----------------------------------
# OLS estimation for training set
----------------------------------

SP500_train=smf.ols(formula='Earnings_E ~ Date + S_and_P_Comp_P + Dividend_D + Consumer_Price_Index_CPI + Long_Interest_Rate_GS10', data=SP500_train_70).fit()

SP500_train.summary()


# R-sq - 0.907. 90.7% of variance explained by OLS model is strong enough almost the same as previous data set.

# P>[t]:
#        all variables are statistically significant P>[t] = 0.000 which is lower than 0.05 = type1 error


# Coef for variables:
#                    Date, S_and_P_Comp_P, Dividend_D, Long_Interest_Rate_GS10 has positive coef 
#                    Consumer_Price_Index_CPI still negative coef


----------------------------------
# Prediction
----------------------------------

SP500_test_30['prediction']=SP500_train.predict(SP500_test_30)

SP500_test_30['error_rate']=(SP500_test_30['prediction']-SP500_test_30['Earnings_E'])/SP500_test_30['Earnings_E']

----------------------------------
# Creating plot to estimate a prediction
----------------------------------


# Lets see how error rate fluctuating in time range

(
 ggplot(SP500_test_30) +
 geom_line(aes(x='Date',
              y='error_rate')) +
 labs(title='Error rate in the period 1871 - 2021',
      x='Date',
      y='Error Rate') +
 custom_theme
 )


np.mean(SP500_test_30['error_rate'])

# Average error rate is 0.044281     

----------------------------------
# Compare actual vs prediction Earnings
----------------------------------

(
    ggplot(SP500_test_30) +
    geom_line(aes(x = 'Date', 
                   y='Earnings_E'),
              color='red') + 
     geom_line(aes(x = 'Date', 
                   y='prediction'),
              color='blue')+
    labs(
        title ='Compare actual and prediction Earnings',
        x = 'year',
        y = 'Earnings_actual(red) / ' 'Earnings_prediction(blue)') + 
    custom_theme
    )


# As we see in our graph there is small differences between actual data set and our prediction model data.
# Our data prediction model is not bad if we look into the plot we can observe that predicted Earnings raising according actual data. I would mention that this also depends on accuracy of data in our data set that we drop Nan value data.


==============================================

# 2. Lets drop varibales with negative coef and see how much prediction will change.

==============================================

----------------------------------
# OLS estimation for training set
----------------------------------

SP500_train=smf.ols(formula='Earnings_E ~ Date + S_and_P_Comp_P + Dividend_D + Long_Interest_Rate_GS10', data=SP500_train_70).fit()

SP500_train.summary()

# R-sq - 0.910. 91% of variance explained by OLS model is strong enough almost the same as previous data set.

# P>[t]:
#       again all variables are statistically significant P>[t] = 0.000 which is lower than 0.05 = type1 error

# Coef for variables:
#                    all variables coef are still positive


----------------------------------
# Prediction
----------------------------------

SP500_test_30['prediction']=SP500_train.predict(SP500_test_30)

SP500_test_30['error_rate']=(SP500_test_30['prediction']-SP500_test_30['Earnings_E'])/SP500_test_30['Earnings_E']

----------------------------------
# Creating plot to estimate a prediction
----------------------------------

(
 ggplot(SP500_test_30) +
 geom_line(aes(x='Date',
              y='error_rate')) +
 labs(title='Error rate in the period 1871 - 2021',
      x='Date',
      y='Error Rate') +
 custom_theme
 )

np.mean(SP500_test_30['error_rate'])

# Average error rate is 0.068152   

----------------------------------
# Compare Actual vs prediction Earnings
----------------------------------

(
    ggplot(SP500_test_30) +
    geom_line(aes(x = 'Date', 
                   y='Earnings_E'),
              color='red') + 
     geom_line(aes(x = 'Date', 
                   y='prediction'),
              color='blue')+
    labs(
        title ='Compare actual and prediction Earnings',
        x = 'year',
        y = 'Earnings_actual(red) / ' 'Earnings_prediction(blue)') + 
    custom_theme
    )

# Even when we drop variables with negative coef we received almost same picture of prediction model against actual data.


==============================================

# 3. Now lets see how only one variable SP500_price can impact Earnings. Creating model with one independend variable.

==============================================

----------------------------------
# OLS estimation for training set
----------------------------------

SP500_train=smf.ols(formula='Earnings_E ~ S_and_P_Comp_P', data=SP500_train_70).fit()

SP500_train.summary()

# R-sq - 0.889. 88.9% of variance explained by OLS model is strong enough almost the same as previous data set.

# P>[t]:
#       variable is statistically significant P>[t] = 0.000 which is lower than 0.05 = type1 error

# Coef for variables:
#                    coef still positive


----------------------------------
# Prediction
----------------------------------

SP500_test_30['prediction']=SP500_train.predict(SP500_test_30)

SP500_test_30['error_rate']=(SP500_test_30['prediction']-SP500_test_30['Earnings_E'])/SP500_test_30['Earnings_E']

----------------------------------
# Creating plot to estimate a prediction
----------------------------------

(
 ggplot(SP500_test_30) +
 geom_line(aes(x='Date',
              y='error_rate')) +
 labs(title='Error rate in the period 1871 - 2021',
      x='Date',
      y='Error Rate') +
 custom_theme
 )

np.mean(SP500_test_30['error_rate'])

# Average error rate is 1.17427

----------------------------------
# Compare Actual vs prediction Earnings
----------------------------------

(
    ggplot(SP500_test_30) +
    geom_line(aes(x = 'Date', 
                   y='Earnings_E'),
              color='red') + 
     geom_line(aes(x = 'Date', 
                   y='prediction'),
              color='blue')+
    labs(
        title ='Compare actual and prediction Earnings',
        x = 'year',
        y = 'Earnings_actual(red) / ' 'Earnings_prediction(blue)') + 
    custom_theme
    )


# There is no big differences when we creating model with one or several independent variables.
# In all 3 scenarios we are getting almost the same prediction with small differences error_rate between all prediction models.
# Conclusion:
#     variable Earnings highly depends of all independent variables such as Date, Price, Dividend, Long interest rate.
#     prediction which we received looks like strong enough and the gap between actual data and predictoin not big. Predicted data and actual data both have same trajectory, but Earnings of actual data is fluctuated highly rather than Earnings of predicted data (I would mention here that we dropped some Nan value from our data which is impacted into accuracy of the data set). 
  