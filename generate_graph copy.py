import pandas as pd
import numpy as np
import datetime
import json
from astral.sun import sun
from astral import LocationInfo

def daylight_hours_per_day(city, year):
    start_date = datetime.date(year, 1, 1)
    end_date = datetime.date(year, 12, 31)
    date_range = pd.date_range(start_date, end_date)

    daily_daylight_hours = []
    for date in date_range:
        s = sun(city.observer, date=date)
        daylight_duration = s['sunset'] - s['sunrise']
        daily_daylight_hours.append(daylight_duration.total_seconds() / 3600)

    return pd.DataFrame({'Date': date_range, 'DaylightHours': daily_daylight_hours})

# Definiera platsinformation för Norrköping
norrkoping = LocationInfo("Norrköping", "Sweden", "Europe/Stockholm", 58.5877, 16.1924)
daylight_hours_2024 = daylight_hours_per_day(norrkoping, 2024)

# Calculate the change in daylight hours
daylight_change = np.diff(daylight_hours_2024['DaylightHours']) * 60  # Change to minutes

# Estimate the change for the last day
average_last_days = np.mean(daylight_change[-5:])  # Average of the last 5 days
estimated_change_last_day = average_last_days

# Append the estimated change to the daylight_change array
daylight_change = np.append(daylight_change, estimated_change_last_day)

# Append the daylight_change array to the DataFrame
daylight_hours_2024['DaylightChange'] = daylight_change

# Format dates to string for JSON serialization
daylight_hours_2024['Date'] = daylight_hours_2024['Date'].dt.strftime('%Y-%m-%d')

# Convert the DataFrame to a list of dictionaries for JSON output
data_for_json = daylight_hours_2024.to_dict('records')

# Write the data to a JSON file
with open('daylight_data.json', 'w') as json_file:
    json.dump(data_for_json, json_file, indent=4)
