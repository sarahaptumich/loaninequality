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
st.write("We will conduct our exploratory analysis on interest rate and approval rate differences between races across first mortgage loans \
         intended as a primary residence in the United States. We will also use a dataset provided by Home Owner Loan Corporation (HOLC) to \
         identify areas that may be most affected by redlining discrimination. For more information on Redlining, we suggest this great article\
         [Mapping Inequiality](https://dsl.richmond.edu/panorama/redlining/#loc=5/39.1/-94.58&text=intro)")
st.write("Some of our datasets are extremely large; therefore, we will utilize PySpark to process the data more efficiently and also import\
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

# py park soce for streamlit
_pyspark= '''#pyspark session

spark = SparkSession.builder.master("local[*]").appName('My First Spark application').getOrCreate()
sc = spark.sparkContext

#load data HMDA
df_hm = spark.read.option("header",True).csv("2021_public_lar.csv")
df_hm.show(2,truncate=False)'''

st.code(_pyspark, language='python')




