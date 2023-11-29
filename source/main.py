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
    lat = st.text_input('Enter latitude', value=47.56)
    lon = st.text_input('Enter longitude', value=-122.01)

    # SIDEBAR: submit button for lat, lon
    check_location = st.button('Check Location')

    if check_location and lat and lon:
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

    # SIDEBAR: use a form to get user inputs
    st.header('After confirming location, select spectrum options')
    with st.form('user_inputs'):
        # SIDEBAR: input risk category, only 1.
        risk_category = st.radio(
            'Select risk category',
            ['I', 'II', 'III', 'IV'],
            index=2 #Default to III
            )

        # SIDEBAR: site class inputs, up to 9.
        site_classes = st.multiselect(
            'Select one or more site classes:',
            ['A','B','BC','C','CD', 'D', 'DE', 'E', 'Default'],
            default=['C','CD','D']
            )

        # SIDEBAR: name the location of the project.
        title = st.text_input('Project Location', value="MyCity")

        # SIDEBAR: option to create composite spectrum
        composite = st.radio(
            'Select to plot maximum composite spectrum:',
            ['yes', 'no']
            )

        # SIDEBAR: submit button.
        user_input = st.form_submit_button("SUBMIT")

# Upon submit, get data and show plots and dataframes.
if user_input:
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
        urls.append((url, site_class))

    # When URLs are ready, scrape data
    all_data = []
    for url, site_class in urls:
        periods, ordinates = scraper.scrape_data(url)
        if periods and ordinates:
            all_data.append({
                'Site Class': site_class,
                'Periods': periods,
                'Ordinates': ordinates})

    # Convert all to a dataframe.
    my_df = pd.DataFrame(all_data)

    # Plot the retrieved spectra.
    fig = go.Figure()
    for data in all_data:
        fig.add_trace(
            go.Scatter(
                x=data['Periods'],
                y=data['Ordinates'],
                name=f"Site Class {data['Site Class']}"
            )
        )

    # Add composite spectrum if selected
    if composite == 'yes':
        # Use the periods from first site class since all the same.
        periods = all_data[0]['Periods'] if all_data else []

        # Get max spectral acceleration at each period.
        max_ords = [max(data['Ordinates'][i] for data in all_data) for i in range(len(periods))]
        
        # Add the composite spectrum.
        fig.add_trace(
            go.Scatter(
                x=periods,
                y=max_ords,
                name='Composite Spectrum',
                line=dict(dash='dash')
            )
        )
        
# MAIN AREA: display spectra plot.
st.plotly_chart(fig)

# MAIN AREA: display datarame of spectral ordinates.
st.write('The dataframe contains the spectral ordinates of the plotted data')
st.dataframe(my_df)

# MAIN AREA: write out URLs and data source.
url_list = [url for url, _ in urls]
url_string = "\n".join(url_list)
st.write('The data was gathered from the USGS website using these URLs:', url_string)

