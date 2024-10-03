import os
from datetime import datetime
import matplotlib.pyplot as plt

# Assume both imports and functions for data loading are the same
from rune_metro_data import rune_metro_data
from sola_metro_data import sola_metro_data


def metro_data():
    # Load data from both files
    rune_date_time, rune_temp, rune_temp_fall, rune_avg_temp, rune_pressure_barometer, rune_pressure_absolute = rune_metro_data()
    sola_date_time, sola_temp, sola_temp_fall, sola_lufttrykk = sola_metro_data()

    # Create dictionaries for quick lookup of temperatures and pressures by timestamp
    rune_data = {dt: (temp, temp_fall, pressure_baro) for dt, temp, temp_fall, pressure_baro in zip(rune_date_time, rune_temp, rune_temp_fall, rune_pressure_barometer)}
    sola_data = {dt: (temp, temp_fall, lufttrykk) for dt, temp, temp_fall, lufttrykk in zip(sola_date_time, sola_temp, sola_temp_fall, sola_lufttrykk)}

    # Combine unique timestamps from both datasets
    combined_date_time = sorted(set(rune_date_time).union(set(sola_date_time)))

    # Create combined data lists
    combined_temp = []
    combined_temp_fall = []
    combined_pressure_barometer = []

    # Iterate over the combined timestamps
    for dt in combined_date_time:
        if dt in rune_data:
            rune_temp, rune_temp_fall, rune_pressure = rune_data[dt]
        else:
            rune_temp, rune_temp_fall, rune_pressure = None, None, None

        if dt in sola_data:
            sola_temp, sola_temp_fall, sola_pressure = sola_data[dt]
        else:
            sola_temp, sola_temp_fall, sola_pressure = None, None, None

        # Choose how to combine the data (for example, averaging or prioritizing one dataset)
        combined_temp.append(
            (rune_temp if rune_temp is not None else 0) + (sola_temp if sola_temp is not None else 0)
        )

        combined_temp_fall.append(
            (rune_temp_fall if rune_temp_fall is not None else 0) + (sola_temp_fall if sola_temp_fall is not None else 0)
        )

        combined_pressure_barometer.append(
            (rune_pressure if rune_pressure is not None else 0) + (sola_pressure if sola_pressure is not None else 0)
        )

    # Return combined data
    return combined_date_time, combined_temp, combined_temp_fall, combined_pressure_barometer


# Example usage
if __name__ == "__main__":
    combined_date_time, combined_temp, combined_temp_fall, combined_pressure_barometer = metro_data()

    # Optional: Plot the combined data
    plt.figure(figsize=(12, 6))
    plt.plot(combined_date_time, combined_temp, label='Combined Temperature', color='blue')
    plt.plot(combined_date_time, combined_temp_fall, label='Combined Temp Fall', color='black')

    plt.xlabel('Time')
    plt.ylabel('Value')
    plt.title('Combined Data from Rune and Sola')
    plt.legend()
    plt.show()
