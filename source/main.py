# An app to plot the ASCE 7-22 response spectra
# given the user selected location and site class(es).

# Import libraries
import streamlit as st
import hmac
import pandas as pd
import plotly.graph_objects as go
import scraper
import functions

def check_password():
    """Returns `True` if the user had the correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if hmac.compare_digest(st.session_state["password"], st.secrets["password"]):
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # Don't store the password.
        else:
            st.session_state["password_correct"] = False

    # Return True if the passward is validated.
    if st.session_state.get("password_correct", False):
        return True

    # Show input for password.
    st.text_input(
        "Password", type="password", on_change=password_entered, key="password"
    )
    if "password_correct" in st.session_state:
        st.error("Password incorrect")
    return False

if not check_password():
    st.stop()  # Do not continue if check_password is not True.

# Title for app.
st.header('ASCE 7-22 Response Spectra Plotter')

# User input location, confirm on map
with st.sidebar:
    # SIDEBAR: Tell user to start here.
    st.header('Start by Entering Options Here')

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

    # Make a human-reader friendly dataframe.
    # Get periods from first site class since same for all.
    periods = all_data[0]['Periods'] if all_data else []
    my_df = pd.DataFrame({'Periods': periods})

    # Add columns for each site class.
    for data in all_data:
        site_class = data['Site Class']
        ordinates = data['Ordinates']
        my_df[site_class] = ordinates

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
        
        # Add the composite spectrum to the plot.
        fig.add_trace(
            go.Scatter(
                x=periods,
                y=max_ords,
                name='Composite Spectrum',
                line=dict(dash='dash')
            )
        )

        # Add the composite spectrum to the dataframe.
        my_df['Composite'] = max_ords


    # Set x axis to log and add labels.
    fig.update_xaxes(
            type='log',
            title='Period (s)'
        )
    
    fig.update_yaxes(
            title='Spectral Acceleration (g)'
        )
    
    fig.update_layout(
        title=f'Multiperiod Response Spectra for {title}',
        hovermode='x unified'
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

    # MAIN AREA: show a disclaimer.
    st.write('This tool was developed to aid exploratory analysis of projects.' +
             'It is subject to revision. Though developed thoughtfully, ' +
             'neither the functionality of the software nor the reliablity of ' + 
             'the data are guaranteed. No warranty, expressed or implied, is ' +
             'made by the author. Users are urged to vet the data and ' +
             'information here against a unique source before relying on it ' +
             'for decision making.')

# Add a welcome message.
if not user_input:
    st.write('Please submit required data in sidebar to the left.')