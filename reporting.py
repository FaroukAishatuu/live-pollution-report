# This is a template. 
# You should modify the functions below to match
# the signatures determined by the project specification

import csv
from datetime import datetime
import statistics

def daily_average(data, monitoring_station, pollutant):
    """
    Calculate the daily averages for a specific pollutant and monitoring station.

    Args:
        data (dict): The data dictionary containing the pollution records.
        monitoring_station (str): The code of the monitoring station.
        pollutant (str): The name of the pollutant.

    Returns:
        list: A list of dictionaries, each containing the date and its corresponding daily average.
    """
    daily_averages = []

    if monitoring_station in data and isinstance(data[monitoring_station], list):
        records = data[monitoring_station]
        records.sort(key=lambda x: datetime.strptime(x['date'], '%Y-%m-%d'))  # Sort records by date

        current_date = records[0]['date']
        total = 0
        count = 0

        for record in records:
            if record['date'] == current_date:
                if pollutant in record:
                    total += float(record[pollutant])
                    count += 1
            else:
                if count > 0:
                    daily_average = total / count
                    daily_averages.append({
                        'date': current_date,
                        'average': daily_average
                    })

                # Move to the next date
                current_date = record['date']
                total = 0
                count = 0

                if pollutant in record:
                    total += float(record[pollutant])
                    count += 1

        # Add the last daily average
        if count > 0:
            daily_average = total / count
            daily_averages.append({
                'date': current_date,
                'average': daily_average
            })

    return daily_averages

def daily_median(data, monitoring_station, pollutant):
    """
    Calculate the daily medians for a specific pollutant and monitoring station.

    Args:
        data (dict): The data dictionary containing the pollution records.
        monitoring_station (str): The code of the monitoring station.
        pollutant (str): The name of the pollutant.

    Returns:
        list: A list of dictionaries, each containing the date and its corresponding daily median.
    """
    daily_medians = []

    if monitoring_station in data and isinstance(data[monitoring_station], list):
        records = data[monitoring_station]
        records.sort(key=lambda x: datetime.strptime(x['date'], '%Y-%m-%d'))  # Sort records by date

        current_date = records[0]['date']
        values = []

        for record in records:
            if record['date'] == current_date:
                if pollutant in record:
                    value = record[pollutant]
                    if value != "No data":
                        values.append(float(value))
            else:
                if len(values) > 0:
                    median = statistics.median(values)
                    daily_medians.append({
                        'date': current_date,
                        'median': median
                    })
                else:
                    daily_medians.append({
                        'date': current_date,
                        'median': None
                    })
                    
                # Move to the next date
                current_date = record['date']
                values = []

                if pollutant in record:
                    value = record[pollutant]
                    if value != "No data":
                        values.append(float(value))

        # Add the last daily median
        if len(values) > 0:
            median = statistics.median(values)
            daily_medians.append({
                'date': current_date,
                'median': median
            })
        else:
            daily_medians.append({
                'date': current_date,
                'median': None
            })

    return daily_medians

def hourly_average(data, monitoring_station, pollutant):
    """
    Calculate the hourly averages for a specific pollutant and monitoring station.

    Args:
        data (dict): The data dictionary containing the pollution records.
        monitoring_station (str): The code of the monitoring station.
        pollutant (str): The name of the pollutant.

    Returns:
        list: A list of dictionaries, each containing the time and its corresponding hourly average.
    """
    hourly_averages = []

    if monitoring_station in data and isinstance(data[monitoring_station], list):
        records = data[monitoring_station]

        for hour in range(1, 25):  #the range from 1 to 25 for hours 1 to 24
            values = []
            for record in records:
                record_hour = int(record['time'].split(':')[0])
                if record_hour == hour and pollutant in record:
                    value = float(record[pollutant])
                    values.append(value)

            if values:
                average = sum(values) / len(values)
                hourly_averages.append({'time': f'{hour:02}:00:00', 'average': average})
            else:
                hourly_averages.append({'time': f'{hour:02}:00:00', 'average': None})

    return hourly_averages

def monthly_average(data, monitoring_station, pollutant):
    """
    Calculate the monthly averages for a specific pollutant and monitoring station.

    Args:
        data (dict): The data dictionary containing the pollution records.
        monitoring_station (str): The code of the monitoring station.
        pollutant (str): The name of the pollutant.

    Returns:
        list: A list of dictionaries, each containing the month and its corresponding monthly average.
    """
    monthly_averages = []

    if monitoring_station in data and isinstance(data[monitoring_station], list):
        records = data[monitoring_station]
        records.sort(key=lambda x: datetime.strptime(x['date'], '%Y-%m-%d'))  # Sort records by date

        current_month = None
        total = 0
        count = 0

        for record in records:
            record_date = datetime.strptime(record['date'], '%Y-%m-%d')
            month = record_date.strftime('%B')

            if current_month is None:
                current_month = month

            if month != current_month:
                if count > 0:
                    monthly_average = total / count
                    monthly_averages.append({'month': current_month, 'monthly_average': monthly_average})
                else:
                    monthly_averages.append({'month': current_month, 'monthly_average': None})

                # Move to the next month
                current_month = month
                total = 0
                count = 0

            if pollutant in record:
                value = record[pollutant]
                total += float(value)
                count += 1

        # Add the last monthly average
        if count > 0:
            monthly_average = total / count
            monthly_averages.append({'month': current_month, 'monthly_average': monthly_average})
        else:
            monthly_averages.append({'month': current_month, 'monthly_average': None})

    return monthly_averages

def peak_hour_date(data, date, monitoring_station, pollutant):
    """
    Find the hour of the day with the highest pollution level and its corresponding value for a given date,
    monitoring station, and pollutant.

    Args:
        data (dict): The data dictionary containing the pollution records.
        date (str): The date for which to find the peak hour.
        monitoring_station (str): The code of the monitoring station.
        pollutant (str): The name of the pollutant.

    Returns:
        tuple: A tuple containing the hour of the day (in the format 'HH:00:00') and the corresponding pollution value.
               Returns None if no matching records are found.
    """
    records = data.get(monitoring_station, [])
    filtered_records = [record for record in records if record.get('date') == date and pollutant in record]
    
    if not filtered_records:
        return None

    max_value = float(filtered_records[0][pollutant])
    max_hour = filtered_records[0]['time']
    
    for record in filtered_records:
        value = float(record[pollutant])
        if value > max_value:
            max_value = value
            max_hour = record['time']

    return (max_hour, max_value)

def weekly_average(data, monitoring_station, pollutant):
    """
    Calculate the weekly averages for a specific pollutant and monitoring station.

    Args:
        data (dict): The data dictionary containing the pollution records.
        monitoring_station (str): The code of the monitoring station.
        pollutant (str): The name of the pollutant.

    Returns:
        list: A list of dictionaries, each containing the week number and its corresponding weekly average.
    """
    weekly_averages = []

    if monitoring_station in data and isinstance(data[monitoring_station], list):
        records = data[monitoring_station]

        # Group records by week
        weekly_records = {}
        for record in records:
            if pollutant in record:
                date = record['date']
                week_number = datetime.strptime(date, '%Y-%m-%d').isocalendar()[1]
                if week_number not in weekly_records:
                    weekly_records[week_number] = []
                weekly_records[week_number].append(float(record[pollutant]))

        # Calculate weekly averages
        for week_number, records in weekly_records.items():
            average = sum(records) / len(records)
            weekly_averages.append({'week': week_number, 'weekly_average': average})

    return weekly_averages

def day_of_week_average(data, monitoring_station, pollutant):
    """
    Calculate the day-of-the-week averages for a specific pollutant and monitoring station.

    Args:
        data (dict): The data dictionary containing the pollution records.
        monitoring_station (str): The code of the monitoring station.
        pollutant (str): The name of the pollutant.

    Returns:
        list: A list of dictionaries, each containing the day of the week and its corresponding average.
    """
    day_of_week_averages = []

    if monitoring_station in data and isinstance(data[monitoring_station], list):
        records = data[monitoring_station]

        # Group records by day of the week
        day_of_week_records = {}
        for record in records:
            if pollutant in record:
                date = record['date']
                day_of_week = datetime.strptime(date, '%Y-%m-%d').strftime('%A')
                if day_of_week not in day_of_week_records:
                    day_of_week_records[day_of_week] = []
                day_of_week_records[day_of_week].append(float(record[pollutant]))

        # Calculate day of the week averages
        weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        for day_of_week in weekdays:
            if day_of_week in day_of_week_records:
                records = day_of_week_records[day_of_week]
                average = sum(records) / len(records)
                day_of_week_averages.append({'day_of_week': day_of_week, 'average': average})

    return day_of_week_averages

def count_missing_data(data, monitoring_station, pollutant):
    """
    Count the number of missing data occurrences for a specific pollutant and monitoring station.

    Args:
        data (dict): The data dictionary containing the pollution records.
        monitoring_station (str): The code of the monitoring station.
        pollutant (str): The name of the pollutant.

    Returns:
        int: The count of missing data occurrences.
    """
    count = 0
    if monitoring_station in data and isinstance(data[monitoring_station], list):
        for record in data[monitoring_station]:
            if pollutant in record and record[pollutant] == "No data":
                count += 1
    return count

def fill_missing_data(data, new_value, monitoring_station, pollutant):
    """
    Fill the missing data occurrences with a new value for a specific pollutant and monitoring station.

    Args:
        data (dict): The data dictionary containing the pollution records.
        new_value (float or str): The new value to replace the missing data.
        monitoring_station (str): The code of the monitoring station.
        pollutant (str): The name of the pollutant.

    Returns:
        None
    """
    if monitoring_station in data and isinstance(data[monitoring_station], list):
        for record in data[monitoring_station]:
            if pollutant in record and record[pollutant] == "No data":
                record[pollutant] = new_value


def read_csv_files():
    """
    Read the CSV files for each monitoring station and store the data in a dictionary.

    Returns:
        dict: A dictionary containing the data from the CSV files for each monitoring station.
    """
    data = {}

    MY1 = "data/Pollution-London Marylebone Road.csv"
    KC1 = "data/Pollution-London N Kensington.csv"
    HRL = "data/Pollution-London Harlington.csv"

    # Read MY1 data
    with open(MY1, "r") as file:
        reader = csv.DictReader(file)
        data["MY1"] = [row for row in reader]

    # Read KC1 data
    with open(KC1, "r") as file:
        reader = csv.DictReader(file)
        data["KC1"] = [row for row in reader]

    # Read HRL data
    with open(HRL, "r") as file:
        reader = csv.DictReader(file)
        data["HRL"] = [row for row in reader]

    # Count and fill missing data for all pollutants and monitoring stations
    for station_code, station_data in data.items():
        for pollutant in station_data[0].keys():
            if pollutant != "date" and pollutant != "time":
                missing_count = count_missing_data(data, station_code, pollutant)
                # Uncomment the following line to print the missing data count for each pollutant
                # print(f"Missing data count for {station_code} {pollutant}: {missing_count}")
                if missing_count > 0:
                    fill_missing_data(data, 0, station_code, pollutant)

    return data