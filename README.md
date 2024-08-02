## Project Overview
This project is designed to fetch and process automatic observation data from weather stations using a government open data API. It retrieves the data, processes it, and saves it in a convenient format for further analysis.

## Features
- Connects to the government's open data platform API for automatic weather station data
- Retrieves JSON data using the `requests` library
- Converts JSON data to Python dictionary format
- Saves the processed data as a CSV file

## Technologies Used
- Python
- `requests` library: For making HTTP requests to the API
- JSON: For handling the data format returned by the API
- CSV: For storing the processed data

## Project Workflow
1. **API Selection**: Choose the Automatic Weather Station's automatic observation data API from the government's open data website.
2. **Data Retrieval**: Use the `requests` library to fetch data from the selected API.
3. **Data Processing**: 
   - Parse the JSON response from the API
   - Convert the JSON data into a Python dictionary
4. **Data Storage**: Save the processed data as a CSV file for easy access and further analysis.
