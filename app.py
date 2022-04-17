'''
Dependencies
data: 
data/time_series_covid19.csv
time_series_covid19_confirmed_global.csv
time_series_covid19_deaths_global.csv
time_series_covid19_recovered_global.csv


modules:
frontend.py: Front-end works
generic.py: Load necessary files
'''

import streamlit as st
import pandas as pd
import generic
import frontend
import pydeck as pdk
import math
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
from plotly.subplots import make_subplots
import folium
import numpy as np
from datetime import date
from streamlit_folium import folium_static


filename = 'csse_covid_19_time_series/time_series_covid19.csv'

################################################################
# Header and preprocessing
# Set Title
st.title('Covid-19 Dashboard')
# Initial data load
update_status = st.markdown("Loading infections data...")
covid = generic.read_dataset(filename)
update_status.markdown('Load complete!')



################################################################
# Sidebar section
sel_region, sel_country, chosen_stat = frontend.display_sidebar(covid)


################################################################
# Main section
update_status.markdown("Finding top districts...")
cand = generic.set_candidates(covid,sel_region,sel_country,chosen_stat)
update_status.markdown("Calculation complete!")

update_status.markdown("Drawing charts")
frontend.show_stats(covid,sel_region,sel_country,chosen_stat,cand)
update_status.markdown("Job Complete!")



################################################################
# Dataset for Exploratory Data Analysis
confirmed_df = pd.read_csv('csse_covid_19_time_series/time_series_covid19_confirmed_global.csv')
death_df = pd.read_csv('csse_covid_19_time_series/time_series_covid19_deaths_global.csv')
recovered_df = pd.read_csv('csse_covid_19_time_series/time_series_covid19_recovered_global.csv')

country_df = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/web-data/data/cases_country.csv')


# Adding multiple themes, including light and dark mode
confirmed_total = int(country_df['Confirmed'].sum())
# active_total = int(country_df['Active'].sum())
deaths_total = int(country_df['Deaths'].sum())
# recovered_total = int(country_df['Recovered'].sum())

# helper function
def breakline():
    return st.markdown("<br>", unsafe_allow_html=True)



########################### World Map View ###########################
breakline()
st.markdown("<h2 style='text-align: center; color: black; background-color:crimson'>World Map View</h2>",
            unsafe_allow_html=True)
world_map = folium.Map(location=[11,0], tiles="cartodbpositron", zoom_start=2, max_zoom = 6, min_zoom = 2)

#confirmed_df = confirmed_df[confirmed_df.isnull()]

confirmed_df=confirmed_df.dropna(subset=['Long'])

confirmed_df=confirmed_df.dropna(subset=['Lat'])

for i in range(0,len(confirmed_df)):
    folium.Circle(
        location=[confirmed_df.iloc[i]['Lat'], confirmed_df.iloc[i]['Long']],
        fill=True,
        radius=(int((np.log(confirmed_df.iloc[i,-1]+1.00001)))+0.2)*20000,
        color='red',
        fill_color='indigo',
        tooltip = "<div style='margin: 0; background-color: black; color: white;'>"+
                    "<h4 style='text-align:center;font-weight: bold'>"+confirmed_df.iloc[i]['Country/Region'] + "</h4>"
                    "<hr style='margin:10px;color: white;'>"+
                    "<ul style='color: white;;list-style-type:circle;align-item:left;padding-left:20px;padding-right:20px'>"+
                        "<li>Confirmed: "+str(confirmed_df.iloc[i,-1])+"</li>"+
                        "<li>Deaths:   "+str(death_df.iloc[i,-1])+"</li>"+
                        "<li>Death Rate: "+ str(np.round(death_df.iloc[i,-1]/(confirmed_df.iloc[i,-1]+1.00001)*100,2))+ "</li>"+
                    "</ul></div>",
        ).add_to(world_map)

folium_static(world_map)
#################################################################################
breakline()

############# Plot for Confirmed, Recovered and Death cases across world ############
breakline()
st.markdown("<h2 style='text-align: center; color: black; background-color:crimson'>Covid-19 across the world</h2>",
            unsafe_allow_html=True)
breakline()
df_list = []
labels = []
colors = []
colors_dict =  {
        'Confirmed' : 'blue',
        'Deaths' : 'red',
        'Recovered' : 'green'
    }
features = st.multiselect("Select display features : ", 
                          ['Confirmed', 'Deaths', 'Recovered'],
                          default = ['Confirmed','Recovered','Deaths'],
                          key = 'world_features')
for feature in features:
    if feature == 'Confirmed':
        labels.append('Confirmed')
        colors.append(colors_dict['Confirmed'])
        df_list.append(confirmed_df)
    if feature == 'Deaths':
        labels.append('Deaths')
        colors.append(colors_dict['Deaths'])
        df_list.append(death_df)
    if feature == 'Recovered':
        labels.append('Recovered')
        colors.append(colors_dict['Recovered'])
        df_list.append(recovered_df)


# Plot confirmed, active, death, recovered cases
def plot_cases_of_world():
    line_size = [4, 5, 6]
    
    fig = go.Figure();
    
    for i, df in enumerate(df_list):
        x_data = np.array(list(df.iloc[:, 4:].columns))
        y_data = np.sum(np.asarray(df.iloc[:,4:]),axis = 0)
            
        fig.add_trace(go.Scatter(x=x_data, y=y_data, mode='lines+markers',
        name=labels[i],
        line=dict(color=colors[i], width=line_size[i]),
        connectgaps=True,
        text = "Total " + str(labels[i]) +": "+ str(y_data[-1])
        ));
    
    fig.update_layout(
        title="COVID-19 cases of World",
        xaxis_title='Date',
        yaxis_title='No. of Cases',
        margin=dict(l=20, r=20, t=40, b=20),
        paper_bgcolor="white",
        width = 800,
        
    );
    
    fig.update_yaxes(type="linear")
    st.plotly_chart(fig);

plot_cases_of_world()
######################################################################################


########### Plot for Confirmed, Recovered and Death cases across countries ########### 
breakline()
st.markdown("<h2 style='text-align: center; color: black; background-color:crimson'>Covid-19 across countries</h2>",
            unsafe_allow_html=True)
st.write("## Covid-19 across countries")
breakline()
df_list2 = []
labels2 = []
colors2 = []
colors_dict2 =  {
        'Confirmed' : 'blue',
        'Deaths' : 'red',
        'Recovered' : 'green'
    }
selected_country = st.selectbox('Select Country : ', tuple(country_df.iloc[:, 0]), 79)
features2 = st.multiselect("Select display features : ", 
                           ['Confirmed', 'Deaths', 'Recovered'],
                           default = ['Confirmed', 'Deaths', 'Recovered'],
                           key = 'country_features')
for feature in features2:
    if feature == 'Confirmed':
        labels2.append('Confirmed')
        colors2.append(colors_dict2['Confirmed'])
        df_list2.append(confirmed_df)
    if feature == 'Deaths':
        labels2.append('Deaths')
        colors2.append(colors_dict2['Deaths'])
        df_list2.append(death_df)
    if feature == 'Recovered':
        labels2.append('Recovered')
        colors2.append(colors_dict2['Recovered'])
        df_list2.append(recovered_df)

# Plot confirmed, active, death, recovered cases
def plot_cases_of_countries(country):
    line_size = [4, 5, 6]
    
    fig = go.Figure();
    
    for i, df in enumerate(df_list2):
        x_data = np.array(list(df.iloc[:, 4:].columns))
        y_data = np.sum(np.asarray(df[df.iloc[:,1] == country].iloc[:, 4:]),axis = 0)
        
        fig.add_trace(go.Scatter(x=x_data, y=y_data, mode='lines+markers',
        name=labels2[i],
        line=dict(color=colors2[i], width=line_size[i]),
        connectgaps=True,
        text = "Total " + str(labels2[i]) +": "+ str(y_data[-1])
        ));
    
    fig.update_layout(
        title="COVID-19 cases of " + country,
        xaxis_title='Date',
        yaxis_title='No. of Cases',
        margin=dict(l=20, r=20, t=40, b=20),
        paper_bgcolor="white",
        width = 800,
        
    );
    
    fig.update_yaxes(type="linear")
    st.plotly_chart(fig);

# default selected country is India in dropdown
breakline()
plot_cases_of_countries(selected_country)
#############################################################


################# Countries With Most Cases #################
breakline()
st.markdown("<h2 style='text-align: center; color: black; background-color:crimson'>Countries with most number of cases</h2>",
            unsafe_allow_html=True)
type_of_case = st.selectbox('Select type of case : ', 
                            ['Confirmed', 'Deaths'],
                            key = 'most_cases')
selected_count = st.slider('No. of countries :', 
                           min_value=1, max_value=50, 
                           value=10, key='most_count')
sorted_country_df = country_df.sort_values(type_of_case, ascending= False) 
def bubble_chart(n):
    fig = px.scatter(sorted_country_df.head(n), x="Country_Region", y=type_of_case, size=type_of_case, color="Country_Region",
               hover_name="Country_Region", size_max=60)
    fig.update_layout(
    title=str(n) +" Countries with most " + type_of_case.lower() + " cases",
    xaxis_title="Countries",
    yaxis_title= type_of_case + " Cases",
    width = 800
    )
    st.plotly_chart(fig);
bubble_chart(selected_count)
#############################################################


################ Countries With Least Cases #################
breakline()
st.markdown("<h2 style='text-align: center; color: black; background-color:crimson'>Countries with least number of cases</h2>",
            unsafe_allow_html=True)
type_of_case = st.selectbox('Select type of case : ', 
                            ['Confirmed', 'Deaths'],
                            key = 'least_cases')
selected_count = st.slider('No. of countries :', 
                           min_value=1, max_value=50, 
                           value=10, key = 'least_cases')
sorted_country_df = country_df[country_df[type_of_case] > 0].sort_values(type_of_case, ascending= True)
def bubble_chart(n):
    fig = px.scatter(sorted_country_df.head(n), x="Country_Region", y=type_of_case, size=type_of_case, color="Country_Region",
               hover_name="Country_Region", size_max=60)
    fig.update_layout(
    title=str(n) +" Countries with least " + type_of_case.lower() + " cases",
    xaxis_title="Countries",
    yaxis_title= type_of_case + " Cases",
    width = 800
    )   
    st.plotly_chart(fig);
bubble_chart(selected_count)

############################################################



# Dataset for Exploratory Data Analysis
us_confirmed_df = pd.read_csv('csse_covid_19_time_series/time_series_covid19_confirmed_US.csv')
us_deaths_df = pd.read_csv('csse_covid_19_time_series/time_series_covid19_deaths_US.csv')


confirmed_per_state = us_confirmed_df.groupby(['Province_State']).sum().drop(['UID', 'code3', 'FIPS', 'Lat', 'Long_'], axis=1).reset_index().sort_values(by='4/7/22', ascending=False)
confirmed_per_state['Confirmed'] = confirmed_per_state['4/7/22']

deaths_per_state = us_deaths_df.groupby(['Province_State']).sum().drop(['UID', 'code3', 'FIPS', 'Lat', 'Long_'], axis=1).reset_index().sort_values(by='4/7/22', ascending=False)
deaths_per_state = deaths_per_state[deaths_per_state['Population']>0]
deaths_per_state['Deaths'] = deaths_per_state['4/7/22']
deaths_per_state['Fatality_rate'] = (deaths_per_state['4/7/22']/deaths_per_state['Population'])*100

df = pd.merge(confirmed_per_state[{'Province_State', 'Confirmed'}],\
         deaths_per_state[{'Province_State', 'Deaths', 'Fatality_rate'}], on='Province_State')

################# Countries With Most Cases #################
breakline()
st.markdown("<h2 style='text-align: center; color: black; background-color:crimson'>US States with most number of cases</h2>",
            unsafe_allow_html=True)
type_of_case = st.selectbox('Select type of case : ', 
                            ['Confirmed', 'Deaths', 'Fatality_rate'],
                            key = 'state_most_cases')
selected_count = st.slider('No. of states :', 
                           min_value=1, max_value=50, 
                           value=10, key='state_most_count')

sorted_df = df.sort_values(type_of_case, ascending= False)

def bubble_chart(n):   
    fig = px.scatter(sorted_df.head(n), x="Province_State", y=type_of_case, size=type_of_case, color="Province_State",
               hover_name="Province_State", size_max=60)
    fig.update_layout(
    title=str(n) +" States with most " + type_of_case.lower() + " cases",
    xaxis_title="States",
    yaxis_title= type_of_case + " Cases",
    width = 800
    )
    st.plotly_chart(fig);
bubble_chart(selected_count)
############################################################

################# Countries With Most Cases #################
breakline()
st.markdown("<h2 style='text-align: center; color: black; background-color:crimson'>US States with least number of cases</h2>",
            unsafe_allow_html=True)
type_of_case = st.selectbox('Select type of case : ', 
                            ['Confirmed', 'Deaths', 'Fatality_rate'],
                            key = 'state_least_cases')
selected_count = st.slider('No. of states :', 
                           min_value=1, max_value=50, 
                           value=10, key='state_least_count')

sorted_df = df.sort_values(type_of_case, ascending= True)

def bubble_chart(n):   
    fig = px.scatter(sorted_df.head(n), x="Province_State", y=type_of_case, size=type_of_case, color="Province_State",
               hover_name="Province_State", size_max=60)
    fig.update_layout(
    title=str(n) +" States with least " + type_of_case.lower() + " cases",
    xaxis_title="States",
    yaxis_title= type_of_case + " Cases",
    width = 800
    )
    st.plotly_chart(fig);
bubble_chart(selected_count)
############################################################



############################# Time Series Analysis #############################
breakline()
st.markdown("<h2 style='text-align: center; color: black; background-color:crimson'>Time Series Analysis</h2>",
            unsafe_allow_html=True)
country = st.selectbox("Select country :", tuple(country_df.iloc[:, 0]), 79, key='time_series')
case_type = st.selectbox("Select case type : ", ['Confirmed', 'Deaths'])
month_week_date = st.selectbox("Select how you want to plot data :", ['By Weeks','By Months', 'By Date'])
case_dict = {
        'Confirmed' : confirmed_df,
        'Deaths' : death_df,
        'Recovered' : recovered_df
    }
start_date = case_dict[case_type].columns[4].split('/') # 0-month, 1-day, 2-year
end_date = case_dict[case_type].columns[-1].split('/')  # 0-month, 1-day, 2-year  
date1 = date(int(start_date[2]), int(start_date[0]), int(start_date[1]))
date2 = date(int(end_date[2]), int(end_date[0]), int(end_date[1]))
days = abs(date1 - date2).days

if month_week_date == 'By Months':
    months = days//30
    month_slider = st.slider("Select range of months :", 1, months+1, (1, months+1))
    temp_df = case_dict[case_type]
    temp_df = temp_df.iloc[:, 1: 4+(month_slider[1]-1)*30]
    x_data = np.array(list(temp_df.iloc[:, 3+(month_slider[0]-1)*30 : 3+(month_slider[1]-1)*30].columns))
    y_data = np.sum(temp_df[temp_df['Country/Region'] == country].iloc[:, 3+(month_slider[0]-1)*30 : 3+(month_slider[1]-1)*30], axis=0)
    fig = go.Figure();
    fig.add_trace(go.Scatter(x=x_data, y=y_data, mode='lines+markers',
                             connectgaps=True));
    fig.update_layout(
        title= case_type + " cases of " + country + " - By Months",
        xaxis_title='Date',
        yaxis_title='No. of Cases',
        margin=dict(l=20, r=20, t=40, b=20),
        paper_bgcolor="white",
        width = 700,
        
    );
    st.plotly_chart(fig)
    
    
elif month_week_date == 'By Weeks':
    weeks = days // 7
    week_slider = st.slider("Select range of weeks :",1, weeks, (1,weeks))
    temp_df = case_dict[case_type]
    temp_df = temp_df.iloc[:, 1: 4+(week_slider[1]-1)*7]
    x_data = np.array(list(temp_df.iloc[:, 3+(week_slider[0]-1)*7 : 3+(week_slider[1]-1)*7].columns))
    y_data = np.sum(temp_df[temp_df['Country/Region'] == country].iloc[:, 3+(week_slider[0]-1)*7 : 3+(week_slider[1]-1)*7], axis=0)
    fig = go.Figure();
    fig.add_trace(go.Scatter(x=x_data, y=y_data, mode='lines+markers',
                             connectgaps=True));
    fig.update_layout(
        title= case_type + " cases of " + country + " - By Weeks",
        xaxis_title='Date',
        yaxis_title='No. of Cases',
        margin=dict(l=20, r=20, t=40, b=20),
        paper_bgcolor="white",
        width = 700,
        
    );
    st.plotly_chart(fig)

else:
    full_date_range = list(case_dict[case_type].iloc[:, 4:].columns)
    date_slider = st.select_slider(
        "Choose date range (M/DD/YY) :", full_date_range,
        (full_date_range[0], full_date_range[-1]))
    temp_df = case_dict[case_type]
    temp_df = temp_df.loc[:, 'Country/Region':date_slider[1]]
    x_data = np.array(list(temp_df.loc[:, date_slider[0] : date_slider[1]].columns))
    y_data = np.sum(temp_df[temp_df['Country/Region'] == country].loc[:, date_slider[0] : date_slider[1]], axis=0)
    fig = go.Figure();
    fig.add_trace(go.Scatter(x=x_data, y=y_data, mode='lines+markers',
                             connectgaps=True));
    fig.update_layout(
        title= case_type + " cases of " + country + " - By Date",
        xaxis_title='Date',
        yaxis_title='No. of Cases',
        margin=dict(l=20, r=20, t=40, b=20),
        paper_bgcolor="white",
        width = 700,
        
    );
    st.plotly_chart(fig)


######################## Countries with zero cases #######################
breakline()
st.markdown("<h2 style='text-align: center; color: black; background-color:crimson'>Countries with zero cases</h2>",
            unsafe_allow_html=True)
case_type = st.selectbox("Select case type : ", 
                         ['Confirmed', 'Deaths'], 1,
                         key= 'zero_cases')
temp_df = country_df[country_df[case_type] == 0]
st.write('### Countries with zero ' + case_type.lower() + ' cases :')
if len(temp_df) == 0:
    st.error('Sorry. There are no records present where ' + case_type.lower() + ' cases are zero!')
else:
    temp_df = temp_df[['Country_Region', 'Confirmed', 'Deaths']]
    st.write(temp_df)
##########################################################################

# Data Resource Credits
st.subheader('Resource Credits')
data_source = 'Johns Hopkins University CSSE'
st.write('Data source: ' + data_source)
st.write('Map provider: Mapbox, OpenStreetMap')

st.markdown("For issues Contact - stellacydong@gmail.com")
