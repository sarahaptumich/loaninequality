#Import the required Libraries
import pandas as pd
import numpy as np
import altair as alt
from io import StringIO
from scipy.stats import ttest_ind
from causalinference import CausalModel
import statsmodels.formula.api as smf
import statsmodels.api as sm
import streamlit as st
alt.themes.enable("fivethirtyeight")

# Add a title and intro text
st.title('Loan Discrimination Exploration')
st.header("By: Kenny Tang & Sara Haptonstall")
