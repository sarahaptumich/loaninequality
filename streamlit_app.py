#Import the required Libraries
import streamlit as st
st.set_page_config(layout="wide") #to make the page wide
import pandas as pd
import numpy as np
import altair as alt
import pyspark 
from pyspark.sql import SparkSession 
from io import StringIO
from scipy.stats import ttest_ind
from causalinference import CausalModel
import statsmodels.formula.api as smf
import statsmodels.api as sm
alt.themes.enable("fivethirtyeight")

# Add a title and intro text
st.title('Loan Discrimination Exploration')
st.subheader("By: Kenny Tang & Sara Haptonstall")
st.write("Recently, we came across an article published by \
         [Reveal news](https://revealnews.org/article/how-we-identified-lending-disparities-in-federal-mortgage-data/), \
         that talks about the presence of discrimination in home mortgage loans in today's society. In their analysis, \
         they were able to determine the likelihood of mortgage denials for different minority groups through the use of \
         binary logistic regression. The results of their research showed significant discrepancies across 48 different metropolitan areas.")
st.write("This research was conducted over 5 years ago using 2015 and 2016 mortgage data provided by Home Mortgage Disclosure Act (HMDA). \
         As years past and America approaches a more culturally diverse society, we would like to know whether discrimination still plays a \
         significant affect on home mortgage loan approvals for different minority groups. In addition to this, to expand upon the work that \
         inspired our analysis, we will also observe discrepancies in interest rates for different minority groups.")
st.header("Meet the data")
st.subheader("Home Owner Loan Corporation (HOLC)")
st.write("We will conduct our exploratory analysis on interest rate and approval rate differences between races across first mortgage loans \
         intended as a primary residence in the United States. We will also use a dataset provided by HOLC to \
         identify areas that may be most affected by redlining discrimination. For more information on Redlining, we suggest this great article\
         [Mapping Inequiality](https://dsl.richmond.edu/panorama/redlining/#loc=5/39.1/-94.58&text=intro)")
st.write("HOLC homeloan applications dataset is extremely large; therefore, we will utilize PySpark to process the data more efficiently and also import\
         additional dependencies ")


#load libraries
libraries= '''#import libraries
import pandas as pd
import numpy as np
import altair as alt
from scipy.stats import ttest_ind
from causalinference import CausalModel
import statsmodels.formula.api as smf
import statsmodels.api as sm
#pyspark to process large datasets
import pyspark
from pyspark.sql import SparkSession 
#theme
alt.themes.enable("fivethirtyeight")'''

st.code(libraries, language='python')

st.write("Due to its size, we will load HMDA loan application data in as a PySpark table. The HOLC dataset is not as large, so\
         we will loaded as a pandas DataFrame. ")

# pyspark session for streamlit
_pyspark= '''#pyspark session

spark = SparkSession.builder.master("local[*]").appName('My First Spark application').getOrCreate()
sc = spark.sparkContext

#load data HMDA
df_hm = spark.read.option("header",True).csv("2021_public_lar.csv")
print((df_hm.count(), len(df_hm.columns)))'''

st.code(_pyspark, language='python')
st.write('[3765289, 99]')
st.write('The original dataset has 99 columns and over 3 million rows. Here is a sample of the data.')

st.code( ''' #Display 5 rows
df_hm.show(5,truncate=False)''', language='python')


st_df1_hmshow= pd.read_csv('st_df1_hmshow5.csv')
st.dataframe(st_df1_hmshow)

st.write("There are a lot of cleaning we need to do for our mortgage dataset. There are missing values, erroneous values such as negative income, \
          and extreme outliers. In addition, there are many types of loans documented in the dataset and we will need to control for them. \
          For the purpose of our analysis, we will observe loans that are: conventional loans, single family homes, for personal use, \
          we will remove incomplete applications as well.")

_N_df_view= '''# filter only loans for home purchases and for personal use, etc.
df_hm_cleaned = df_hm.select('*')\
    .filter((df_hm.business_or_commercial_purpose == 2) & (df_hm.loan_purpose ==1) &
            (df_hm.occupancy_type ==1)& (df_hm.action_taken !=4) &
            (df_hm.action_taken !=5) & (df_hm.loan_type ==1)&
            (df_hm.derived_dwelling_category == 'Single Family (1-4 Units):Site-Built' )&
            (df_hm.derived_loan_product_type == "Conventional:First Lien") &
            (df_hm.conforming_loan_limit == "C") &
            (df_hm.lien_status == 1) &
            (df_hm.reverse_mortgage == 2) &
            (df_hm.open_end_line_of_credit == 2) &
            (df_hm.negative_amortization == 2 ) &
            (df_hm.total_units == 1)&
            (df_hm.balloon_payment ==2))
        
'''

st.code(_N_df_view, language='python')
st.write( "We also selected only our variables of interest to make this dataset more manageble")

_df_cleaned= '''df_hm_cleaned = cut_view_red()
# Take only features we need
df_hm_cleaned = df_hm_cleaned.select('county_code',
                            'derived_ethnicity', 
                            'derived_race', 
                            'derived_sex', 
                            'action_taken', 
                            'loan_purpose', 
                            'business_or_commercial_purpose',
                            'derived_dwelling_category',
                            'loan_amount',
                            'occupancy_type',
                            'combined_loan_to_value_ratio',
                            'interest_rate', 'property_value',
                            'income',
                            'debt_to_income_ratio',
                            'denial_reason_1',
                            'loan_term',
                            'rate_spread')'''
st.code(_df_cleaned, language='python')
st.write('Next, we will split our dataset by different ethnicity groups so that we may load the data as pandas DataFrames.\
         This makes some of our computations more efficient and it makes comparing select groups easier. To make our lives even easier, \
         we will also merge the derived ethnicity and derived race column by moving Hispanic and Latino to race so that all minority groups \
         are recorded in the same column.')

st.code(''' # Split Dataframe by race and ethinicity
df_hm_white = df_hm_cleaned.select('*').filter(df_hm_cleaned.derived_race =='White').toPandas()
df_hm_asian = df_hm_cleaned.select('*').filter(df_hm_cleaned.derived_race =='Asian').toPandas()
df_hm_black = df_hm_cleaned.select('*').filter(df_hm_cleaned.derived_race =='Black or African American').toPandas()
df_hm_hispanic = df_hm_cleaned.select('*').filter(df_hm_cleaned.derived_ethnicity =='Hispanic or Latino').toPandas()'''), language='python')
                            
