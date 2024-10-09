import os

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import MaxNLocator
from rune import RuneMetroDataProcessor


def calculate_moving_average(times, temps, n):
    avg_times = []
    avg_temps = []

    # Loop over each valid time and temperature index
    for i in range(n, len(temps) - n):
        avg_times.append(times[i])  # Only append valid times (those that won't go out of bounds)
        avg_temps.append(np.mean(temps[i - n:i + n + 1]))  # Calculate the mean for n previous, current, and n next

    return avg_times, avg_temps


def plot_smoothed_temperature(times, temps, n):
    avg_times, avg_temps = calculate_moving_average(times, temps, n)

    plt.figure(figsize=(12, 6))

    # Plot original temperature data
    plt.plot(times, temps, label='Original Temperature', color='green')

    # Plot smoothed temperature data (moving average)
    plt.plot(avg_times, avg_temps, label=f'{n}-point Moving Average', color='orange')

    plt.xlabel('Time')
    plt.ylabel('Temperature (°C)')
    plt.legend()
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# Usage example
rune_processor = RuneMetroDataProcessor()
rune_filepath = os.path.join(os.getcwd(), 'datafiler', 'trykk_og_temperaturlogg_rune_time.csv')
rune_processor.load_data(rune_filepath)

rune_temp_dt, rune_temp_list = rune_processor.get_temperatures()
# Example usage with n=30
# Assuming times and temps are already loaded from your data files
plot_smoothed_temperature(rune_temp_dt, rune_temp_list, n=30)
