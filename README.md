# 🦠 Covid 19 Dashboard 🦠

Checkout the dashboard app here -- https://share.streamlit.io/stellacydong/covid19-dahsboard/main/app.py
<br>

## objectives

* Illustrate cumulative infections and fatalities, daily infections changes, daily fatalities changes in various countries and states in USA. 
* Present the trend of the number of confirmed cases, the number of recovery case, and the number of deaths in countries and USA states. 
* Show the top 10 countries or the top US states which have the most confirmed cases, or the most deaths, or the most fatalities rates. 

## Data sources
* [Johns Hopkins University Github](https://github.com/CSSEGISandData/COVID-19): Global nCov-19 dataset
* [NaturalEarth](http://naturalearthdata.com/): Geographical shapedata for countries (admin0) and states-level (admin1) data to be used (1:10m data is used for selected countries for states details while 1:50m used for others)

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

