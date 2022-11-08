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
