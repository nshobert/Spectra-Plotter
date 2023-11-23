import requests

def scrape_data(url):
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        try:
            periods = data['response']['data']['multiPeriodDesignSpectrum']['periods']
            ordinates = data['response']['data']['multiPeriodDesignSpectrum']['ordinates']
            return periods, ordinates
        except KeyError:
            print("Error: Key not found in JSON response.")
            return None, None
    else:
        print(f"Error: Received status code {response.status_code}")
        return None, None
