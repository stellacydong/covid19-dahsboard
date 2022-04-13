# 🦠 Covid 19 Dashboard - A Dashboard Cum Web App 🦠

Checkout the dashboard app here -- https://share.streamlit.io/stellacydong/covid19-dahsboard/main/app.py
<br>


Coronaviruses or Covid-19 are a large family of viruses that may cause respiratory illnesses in humans ranging from common colds to more severe conditions such as Severe Acute Respiratory Syndrome (SARS) and Middle Eastern Respiratory Syndrome (MERS).

## Primary objectives
* Basic options for users to choose
  * Cumulative or daily changes measures
  * Global aggregate stat or per-country information
* Display a basic statistics for selected area (Global or for specific country)
* Draw a heatmap detailing given a region and measure (e.g., Daily infections increases in the US)
* Draw a Choropleth with the same selection (Country-level or state-level comparisons)

## Data sources
* Data sources
  * [Johns Hopkins University Github](https://github.com/CSSEGISandData/COVID-19): Global nCov-19 dataset

### Prerequisites

You need to have the following dependecies before running the app:

- pandas `pip install pandas`
- numpy `pip install numpy`
- scipy `pip install scipy`
- plotly `pip install plotly`
- streamlit `pip install streamlit`
- streamlit-folium `pip install streamlit-folium`
- datetime `pip install DateTime`


### Usage

1. Install all dependencies mentioned in __Prerequisites__.
2. In your terminal, cd your working directory (where you have placed the .py file and other components). Type in the following command and press Enter :<br>
   `streamlit run app.py`<br>
   Please wait for 5-10 seconds for command to run.

