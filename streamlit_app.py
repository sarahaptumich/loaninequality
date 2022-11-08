#Import the required Libraries
import streamlit as st
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
st.write("Recently, we came across an article published by [Reveal News](https://revealnews.org/article/how-we-identified-lending-disparities-in-federal-mortgage-data/), that talks about the presence of discrimination in home mortgage loans in today's society. In their analysis, they were able to determine the likelihood of mortgage denials for different minority groups through the use of binary logistic regression. The results of their research showed significant discrepancies across 48 different metropolitan areas.")
