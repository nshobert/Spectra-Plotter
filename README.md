# ASCE 7 Response Spectra Comparison Tool

## Overview
This tool is designed for engineers and researchers to compare ASCE 7-22 response spectra. It enables users to input specific geographic coordinates (latitude and longitude) and select from various Site Classes (A, B, BC, C, CD, D, DE, E) to view and compare response spectra. The tool provides interactive visualizations, a simple map for location verification, and the ability to generate and download a 'maximum envelope' spectrum.

## Features
- **Data Scraping**: Automatically scrapes spectral ordinate data from a specified website.
- **User Input**: Allows users to input latitude and longitude and select Site Classes.
- **Interactive Plots**: Visualize the spectral data for easy comparison.
- **Map Integration**: Provides a geographic map to validate the selected location.
- **Maximum Envelope Spectrum**: Generates a spectrum composed of the maximum values across selected spectra.
- **Data Download**: Enables users to download the spectral ordinates of selected classes.

## Installation

### Prerequisites
- Python 3.11
- Pipenv for dependency management

### Setup
1. Clone the repository:
   ```
   git clone [repository-url]
   ```

2. Navigate to the project directory:
```
cd asce7_spectra_app
```
3. Install dependencies using Pipenv:
```
pipenv install
```
4. Activate the Pipenv shell:
```
pipenv shell
```
5. Start the Streamlit app:
```
streamlit run src/main.py
```

## Usage
Describe how to use the application, including any required input formats and user interaction guidelines.

How to share without using the repo? A URL?

## Example/ Test run
simple case to test that download/install worked

## Contributing
Instructions on how to contribute to this project. Include coding standards, commit message guidelines, and other relevant information for potential contributors.

## License
This project is licensed under the MIT License - see the [LICENSE.md](LICENSE) file for details.

## Authors
Your Name - Initial Work - YourGithubProfile

## Acknowledgements
List any other contributors, inspirations, or acknowledgments.