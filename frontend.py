import generic
import pandas as pd
import numpy as np
import math
import altair as alt
import pydeck as pdk
import streamlit as st


read_columns = {7:['Confirmed','State-level Cumulative'],9:['i_Confirmed','State-level Changes'],11:['Tot_Confirmed','Country-level Cumulative'],12:['iTot_Confirmed','Country-level Changes'],15:['Deaths','State-level Cumulative'],17:['i_Deaths','State-level Changes'],19:['Tot_Deaths','Country-level Cumulative'],20:['iTot_Deaths','Country-level Changes']}

# Module to display sidebar
def display_sidebar(data):
    sel_region,sel_country = None, None

    # 1) Choose a Region/Country to display
    st.sidebar.header('Choose Region/Country below')

    # Set candiates of region (Country/Region)
    st.sidebar.markdown('Choose a Country/Region (e.g., US)')
    country = sorted(data.loc[data['len_states']>1,'Country/Region'].unique())
    country = ['Worldwide'] + list(country[:])
    sel_country = st.sidebar.selectbox('Country/Region',country)

    # Candiates of countries (adm0_a3) are automatically set
    if sel_country and sel_country != 'Worldwide':
        sel_region = data.loc[(data['len_states']>1) &  (data['Country/Region'].str.contains(sel_country)),'adm0_a3'].unique()[0]

    # 2) Choose a statistics
    st.sidebar.markdown('Choose a Statistics (e.g., Country-level Changes)')
    if sel_region:
        stat_text = sorted(list(set(val[1] for val in read_columns.values() if val[1][0]=='S')))
    else:
        stat_text = sorted(list(set(val[1] for val in read_columns.values() if val[1][0]=='C')))
    stat_text = [None] + stat_text[:]
    chosen_stat_text = st.sidebar.selectbox('Statistics',stat_text)

    if chosen_stat_text:
        chosen_stat_key = [val[0] for val in read_columns.values() if val[1] in chosen_stat_text]
    else:
        chosen_stat_key = None

    chosen_stat = {}
    if chosen_stat_text:
        for key in chosen_stat_key:
            chosen_stat[key] = chosen_stat_text

#    # 3) Draw map
#    st.sidebar.markdown('Draw a map?')
#    sel_map = st.sidebar.checkbox('Yes')

    return sel_region, sel_country, chosen_stat



# Print latest global status
def show_stats(data,sel_region,sel_country,chosen_stat,candidates,map=None):
    date = max(data['Date'])
    st.header('Summary statistics')

    if not sel_region:
        st.subheader('Global status as of ' + date.strftime('%m/%d/%y'))
        st.markdown(f"Cumulative confirmed cases:  `{data[data['Date']==date].groupby(['adm0_a3','Country/Region'])['Tot_Confirmed'].max().sum():,}`")
        st.markdown(f"Cumulative  fatalities: `{data[data['Date']==date].groupby(['adm0_a3','Country/Region'])['Tot_Deaths'].max().sum():,}`")

    else:
        st.subheader(sel_country + ' status as of ' + date.strftime('%m/%d/%y'))
        st.markdown(f"Cumulative confirmed cases:  `{data[(data['Date']==date) & (data['adm0_a3']==sel_region) & (data['Country/Region']==sel_country)].groupby(['adm0_a3','Country/Region'])['Tot_Confirmed'].max().sum():,}`")
        st.markdown(f"Cumulative fatalities: `{data[(data['Date']==date) & (data['adm0_a3']==sel_region) & (data['Country/Region']==sel_country)].groupby(['adm0_a3','Country/Region'])['Tot_Deaths'].max().sum():,}`")

    show_chart(data,chosen_stat,candidates,sel_region)

    if map and chosen_stat:
        show_map(data,chosen_stat,sel_region)


def show_chart(data,stat,candidates,region,date=None):
    if not date:
        date = min(data['Date'])

    # Set quantiles for x-axis ('Date')
    dates = data['Date'].map(lambda x:x.strftime('%m/%d/%y')).unique().tolist()
    presets = [0,.25,.5,.75,1]
    quantiles = np.quantile(np.arange(0,len(dates)),presets).tolist()
    quantiles = [int(np.floor(q)) for q in quantiles]
    date_visible = [dates[idx] for idx in quantiles]

    if stat:
        st.header('Regional analyses')
        stat_text = ['Infections','Fatalities']
        stat_keys = list(stat.keys())

        data = data.loc[(data['Date']>=date),['Date','adm0_a3','Country/Region','Province/State',stat_keys[0],stat_keys[1]]]

        for idx, stat_key in enumerate(stat_keys):
            if region:
                filtered_data = pd.merge(data[['Date','Province/State',stat_key]],candidates[['index',stat_key]],how='inner',left_on='Province/State',right_on=stat_key)
                filtered_data.drop([stat_key+'_y'],axis=1,inplace=True)
                filtered_data.rename(columns={stat_key+'_x':stat_key,'index':'order'},inplace=True)

                filtered_data['Date'] = filtered_data['Date'].map(lambda x:x.strftime('%m/%d/%y'))

                target_cat = 'Province/State'
            else:
                filtered_data = pd.merge(data[['Date','adm0_a3','Country/Region',stat_key]],candidates[['index',stat_key]],how='inner',left_on='adm0_a3',right_on=stat_key)
                filtered_data.drop([stat_key+'_y'],axis=1,inplace=True)
                filtered_data.rename(columns={stat_key+'_x':stat_key,'index':'order'},inplace=True)

                filtered_data['Date'] = filtered_data['Date'].map(lambda x:x.strftime('%m/%d/%y'))

                target_cat = 'Country/Region'
            if idx == 0:
                st.subheader('Infections developments')
            else:
                st.subheader('Fatalities developments')

            heatmap = alt.Chart(filtered_data).mark_rect().encode(
                x=alt.X('Date:O', sort=dates, axis=alt.Axis(values=date_visible,labelAngle=0)),
                y=alt.Y(target_cat, sort=alt.EncodingSortField(field='order',order='ascending')),
                color=alt.Color(stat_key,scale=alt.Scale(scheme='blues'),title=stat_text[idx]),
                tooltip=['Date:O',target_cat,alt.Tooltip(stat_key,title=stat_text[idx],format=',')]
                ).configure_scale(
                    bandPaddingInner=.1
                    )

            st.altair_chart(heatmap,use_container_width=True)
