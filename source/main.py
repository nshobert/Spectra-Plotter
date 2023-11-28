# An app to plot the ASCE 7-22 response spectra
# given the user selected location and site class(es).

# Import libraries
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import scraper
import functions

# Title for app.
st.header('ASCE 7-22 Response Spectra Plotter')
st.write('an application to plot multiple response spectra')

# User input location, confirm on map
with st.sidebar:
    # SIDEBAR: latitude and longitude inputs.
    lat = st.text_input('Enter latitude (e.g. 47.56)')
    lon = st.text_input('Enter longitude (e.g. -122.01)')

    # SIDEBAR: submit button for lat, lon
    submitted1 = st.button('Check Location')

    if submitted1 and lat and lon:
        try:
            lat_float = float(lat)
            lon_float = float(lon)
            loc = pd.DataFrame({
                'lat': [lat_float],
                'lon': [lon_float]
                })
            st.map(data=loc, zoom=9)
        except ValueError:
            st.error("Please enter valid latitude and longitude values.")
'''
# SIDEBAR: use a form to get user inputs
with st.form('user_inputs'):
    with st.sidebar:
        # SIDEBAR: input risk category, only 1.
        risk_category = st.radio(
            'Select risk category',
            ['I', 'II', 'III', 'IV']
            )

        # SIDEBAR: site class inputs, up to 9.
        site_classes = st.multiselect(
            'Select one or more site classes:',
            ['A','B','BC','C','CD', 'D', 'DE', 'E', 'Default']
            )

        # SIDEBAR: name the location of the project.
        title = st.text_input('Project Location (e.g. Kirkland)')

        # SIDEBAR: option to create composite spectrum
        composite = st.radio(
            'Select to plot maximum composite spectrum:',
            ['yes', 'no']
            )

        # SIDEBAR: submit button.
        submitted2 = st.form_submit_button("SUBMIT")

# Upon submit, get data and show plots and dataframes.
if submitted2:
    # Construct the URLs
    urls = []
    for site_class in site_classes:
        url = functions.construct_url(
            lat,
            lon,
            risk_category,
            site_class,
            title
        )
        urls.append[url]

    # When URLs are ready, scrape data

    # populate dataframes

    # When spectra dfs are made, plot the retrieved spectra

    # MAIN AREA: display spectra plot.
    # create dummy df for development
    my_df=pd.DataFrame(
        [[1,3], [2,2], [3,1]],
        columns=['X', 'Y'])

    # dummy figure for development
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=my_df['X'],
            y=my_df['Y']
            )
    )
    st.plotly_chart(fig)

# MAIN AREA: display datarame of spectral ordinates.
st.write('The dataframe contains the spectral ordinates of the plotted data')
st.dataframe(my_df)

# MAIN AREA: write out URLs and data source.
st.write('The data was gathered from the USGS website using these URLs:', urls)
'''
