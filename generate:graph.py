import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import datetime
from astral.sun import sun
from astral import LocationInfo

def daylight_hours_per_day(city, year):
    # Skapa en lista med datum för varje dag under året
    start_date = datetime.date(year, 1, 1)
    end_date = datetime.date(year, 12, 31)
    date_range = pd.date_range(start_date, end_date)

    # Skapa en lista för att lagra antalet ljusa timmar varje dag
    daily_daylight_hours = []

    for date in date_range:
        # Beräkna soluppgång och solnedgång för varje dag
        s = sun(city.observer, date=date)
        daylight_duration = s['sunset'] - s['sunrise']
        daily_daylight_hours.append(daylight_duration.total_seconds() / 3600)  # Konvertera till timmar

    # Skapa en DataFrame
    return pd.DataFrame({'Date': date_range, 'DaylightHours': daily_daylight_hours})

# Definiera platsinformation för Norrköping
norrkoping = LocationInfo("Norrköping", "Sweden", "Europe/Stockholm", 58.5877, 16.1924)

# Beräkna antalet ljusa timmar per dag för 2024
daylight_hours_2024 = daylight_hours_per_day(norrkoping, 2024)

# Beräkna förändringen i dygnets längd (i minuter) från en dag till nästa
daylight_change = np.diff(daylight_hours_2024['DaylightHours']) * 60  # Konvertera förändringen till minuter

# Skapa en graf
fig, ax1 = plt.subplots(figsize=(15, 6))

# Plotta antalet ljusa timmar
ax1.plot(daylight_hours_2024['Date'], daylight_hours_2024['DaylightHours'], color='skyblue', marker='o', markersize=4, linestyle='-')
ax1.set_ylim(0)  # Börja y-axeln från 0
ax1.set_xlabel('Datum')
ax1.set_ylabel('Antal ljusa timmar', color='skyblue')
ax1.tick_params('y', colors='skyblue')

# Markera dagens datum
today = datetime.date.today()
ax1.axvline(today, color='red', linestyle='--', label='Idag')
ax1.legend()

# Lägg till en sekundär y-axel för förändring i dygnets längd
ax2 = ax1.twinx()
ax2.plot(daylight_hours_2024['Date'][1:], daylight_change, color='green', marker='x', markersize=4, linestyle=':')
ax2.set_ylabel('Förändring i dygnets längd (minuter/dag)', color='green')
ax2.tick_params('y', colors='green')

# Titel och layout
plt.title('Antal ljusa timmar och förändring i dygnets längd per dag i Norrköping, 2024')
ax1.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()

# Spara grafen
plt.savefig('path/to/save/daily_light_graph.png')
