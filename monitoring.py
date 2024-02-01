# This is a template. 
# You should modify the functions below to match
# the signatures determined by the project specification.
# 
# This module will access data from the LondonAir Application Programming Interface (API)
# The API provides access to data to monitoring stations. 
# 
# You can access the API documentation here http://api.erg.ic.ac.uk/AirQuality/help
#
import requests
import datetime
import utils
def get_live_data_from_api(site_code='MY1',species_code='NO',start_date=None,end_date=None):
    """
    Return data from the LondonAir API using its AirQuality API. 
    
    *** This function is provided as an example of how to retrieve data from the API. ***
    It requires the `requests` library which needs to be installed. 
    In order to use this function you first have to install the `requests` library.
    This code is provided as-is. 
    """
    start_date = datetime.date.today() if start_date is None else start_date
    end_date = start_date + datetime.timedelta(days=1) if end_date is None else end_date
    
    
    endpoint = "https://api.erg.ic.ac.uk/AirQuality/Data/SiteSpecies/SiteCode={site_code}/SpeciesCode={species_code}/StartDate={start_date}/EndDate={end_date}/Json"
   
    url = endpoint.format(
        site_code = site_code,
        species_code = species_code,
        start_date = start_date,
        end_date = end_date
    )
    
    res = requests.get(url)
    return res.json()


def display_real_time_statistics(site_code='MY1', species_code='NO'):
    """
    Display real-time statistics for a specific monitoring station and pollutant.
    
    This function retrieves the latest data from the API and displays the real-time statistics.
    
    Args:
        site_code (str): The code of the monitoring station. Defaults to 'MY1'.
        species_code (str): The code of the pollutant. Defaults to 'NO'.
    """
    # Retrieve the latest data from the API
    data = get_live_data_from_api(site_code, species_code)
    
    # Extract relevant information from the data
    data = data['RawAQData']['Data']
    data = list(reversed(data))  # Reverse the list to get the latest data first
    
    print(f"Real-time Statistics for Monitoring Station {site_code} - {species_code}:")
    
    # Iterate over the data and print the pollutant values and measurement dates
    for item in data:
        if item['@Value'] == "":
            item['@Value'] = 0
        print(f"Pollutant Value: {item['@Value']} at {item['@MeasurementDateGMT']}")


def get_highest_pollutant_value(site_code='MY1', species_code='NO', days=7):
    """
    Retrieves the highest pollutant value and its corresponding measurement date
    for a given monitoring site and pollutant species within a specified number of days.

    Args:
        site_code (str): The code of the monitoring site (default: 'MY1').
        species_code (str): The code of the pollutant species (default: 'NO').
        days (int): The number of days to consider for the data (default: 7).
    """
    end_date = datetime.date.today()
    start_date = end_date - datetime.timedelta(days=days)

    data_api = get_live_data_from_api(site_code, species_code, start_date=start_date.strftime('%Y-%m-%d'), end_date=end_date.strftime('%Y-%m-%d'))

    highest_pollutant = None
    highest_value = None
    highest_measurement_date = None

    for entry in data_api['RawAQData']['Data']:
        measurement_date = entry["@MeasurementDateGMT"]
        value = entry["@Value"]

        if highest_value is None or value > highest_value:
            highest_value = value
            highest_measurement_date = measurement_date

    print(f"Highest Pollutant Value for Monitoring Station {site_code} - {species_code} in Last 7 Days:")
    print(f"• Value: {highest_value}") 
    print(f"• Date: {highest_measurement_date}")


def get_pollutant_statistics(site_code='MY1', species_codes=['NO', 'NO2', 'O3']):
    """
    Retrieves live data for the specified species codes from the monitoring station
    identified by the site code and calculates and prints the maximum, minimum, and
    mean values for each pollutant.

    Args:
        site_code (str): The code representing the monitoring station (default: 'MY1')
        species_codes (list): A list of species codes to retrieve data for (default: ['NO', 'NO2', 'O3'])
    """
    start_date = datetime.date.today()
    data = []

    for species_code in species_codes:
        data.append(get_live_data_from_api(site_code, species_code))

    print(f"Pollutant statistics for Monitoring Station {site_code} at {start_date}:")
    for i, entry in enumerate(data):
        pollutant_name = entry['RawAQData']['@SpeciesCode']
        values = []

        data_array = entry['RawAQData']['Data']
        values = [float(item['@Value']) if item['@Value'] != "" else 0 for item in data_array]
        max_value = utils.maxvalue(values)
        min_value = utils.minvalue(values)
        mean_value = utils.meanvalue(values)
        print(f"{pollutant_name}:")
        print(f"• Minimum pollution level: {min_value}")
        print(f"• Maximum pollution level: {max_value}")
        print(f"• Average pollution level: {mean_value}")


def compare_pollutant_levels(site_code='MY1', species_code='NO', start_date=None, end_date=None):
    """
    Compare pollutant levels between two different time periods for a specific monitoring station.

    This function retrieves the data for the specified time periods and compares the pollutant levels.

    Args:
        site_code (str): The code of the monitoring station. Defaults to 'MY1'.
        start_date (str or None): The start date of the first time period in 'YYYY-MM-DD' format. If None, uses the current date.
        end_date (str or None): The end date of the second time period in 'YYYY-MM-DD' format. If None, uses the next day after start_date.
    """
    # Get the current date
    current_date = datetime.date.today()

    # Calculate the date for yesterday and the day before yesterday
    yesterday = current_date - datetime.timedelta(days=1)
    day_before_yesterday = current_date - datetime.timedelta(days=2)
    
    # Retrieve data for the first time period (day before yesterday to yesterday)
    data1 = get_live_data_from_api(site_code, start_date=day_before_yesterday, end_date=yesterday)

    # Retrieve data for the second time period (yesterday onwards)
    data2 = get_live_data_from_api(site_code, start_date=yesterday, end_date=None)

    print(f"Pollutant Comparison for Monitoring Station {site_code} - Pollutant {species_code}:")
    
    # Iterate over each species in the data
    for i, species1 in enumerate(data1['RawAQData']['Data']):
        species2 = data2['RawAQData']['Data'][i]
        try:
            value1 = float(species1.get('@Value', 0))
        except ValueError:
            value1 = 0

        try:
            value2 = float(species2.get('@Value', 0))
        except ValueError:
            value2 = 0

        date1 = species1['@MeasurementDateGMT']
        date2 = species2['@MeasurementDateGMT']

        # Print the pollutant comparison for each species
        print(f"{value1} at {date1} - {value2} at {date2}")

def get_air_quality_data(site_code='MY1', species_code='NO', start_date=None, end_date=None):
    """
    Retrieves air quality data from the specified site and date range.
    
    Args:
        site_code (str): The code representing the site (default: 'MY1').
        species_code (str): The code representing the species (default: 'NO').
        start_date (datetime.date): The start date for the data (default: today).
        end_date (datetime.date): The end date for the data (default: start_date + 1 day).
    
    Returns:
        None
    
    Prints:
        Air quality data for the specified site, date range, and species.
    """
    
    # Set default start and end dates if not provided
    start_date = datetime.date.today() if start_date is None else start_date
    end_date = start_date + datetime.timedelta(days=1) if end_date is None else end_date

    # Construct the API endpoint URL
    endpoint = "https://api.erg.ic.ac.uk/AirQuality/Data/Wide/Site/SiteCode={site_code}/StartDate={start_date}/EndDate={end_date}/Json"
    url = endpoint.format(
        site_code=site_code,
        start_date=start_date,
        end_date=end_date
    )

    # Send request to the API and retrieve the data
    res = requests.get(url)
    data = res.json()
    
    # Extract air quality data and column information
    air_quality_data = data["AirQualityData"]["RawAQData"]["Data"]
    columns = data["AirQualityData"]["Columns"]["Column"]

    # Parse the data into a more readable format
    parsed_data = []

    for measurement in air_quality_data:
        parsed_measurement = {"MeasurementDateGMT": measurement["@MeasurementDateGMT"]}

        for column in columns:
            column_id = column["@ColumnId"]
            column_name = column["@ColumnName"]
            column_data = measurement.get("@{}".format(column_id), None)

            if column_data:
                parsed_measurement[column_name] = float(column_data)
            else:
                parsed_measurement[column_name] = 0.0

        parsed_data.append(parsed_measurement)

    # Extract location from the column information and print it as a title
    location = columns[0]["@ColumnName"].split(":")[0].strip()
    print("Location:", location)

    # Print the air quality data for each measurement date
    for entry in parsed_data:
        date = entry["MeasurementDateGMT"]
        print("\n• Date:", date)
        for key, value in entry.items():
            if key != "MeasurementDateGMT":
                pollutant = key.split(":")[1].split("(")[0].strip()
                print("- {}: {}".format(pollutant, value))