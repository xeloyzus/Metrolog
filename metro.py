import os
import matplotlib.pyplot as plt
import numpy as np
from rune import RuneMetroDataProcessor
from sola import SolaMetroDataProcessor

rune_processor = RuneMetroDataProcessor()
rune_filepath = os.path.join(os.getcwd(), 'datafiler', 'trykk_og_temperaturlogg_rune_time.csv')
rune_processor.load_data(rune_filepath)

sola_processor = SolaMetroDataProcessor()
sola_filepath = os.path.join(os.getcwd(), 'datafiler', 'temperatur_trykk_met_samme_rune_time_datasett.csv')
sola_processor.load_data(sola_filepath)


def calculate_moving_average(times, temps, n):
    avg_times = []
    avg_temps = []

    # Loop over each valid time and temperature index
    for i in range(n, len(temps) - n):
        avg_times.append(times[i])  # Only append valid times (those that won't go out of bounds)
        avg_temps.append(np.mean(temps[i - n:i + n + 1]))  # Calculate the mean for n previous, current, and n next

    return avg_times, avg_temps


def plot_data():
    rune_bar_dt, rune_bar_pressure = rune_processor.get_pressures_bar()
    rune_abs_dt, rune_abs_pressure = rune_processor.get_pressures_abs()
    rune_temp_dt, rune_temp_list = rune_processor.get_temperatures()
    sola_dt, sola_temp = sola_processor.get_temperatures()
    sola_pressure_dt, sola_pressure = sola_processor.get_pressures()
    sola_tempfall_dt, sola_tempfall_liste, _ = sola_processor.get_temp_fall()
    avg_times, avg_temps = calculate_moving_average(rune_temp_dt, rune_temp_list, 30)

    # axis[0].plot(self.date_time_list[::6], self.pressure_barometer_list[1:], label='Trykk Barometer', color='orange')
    # axis[0].plot(self.date_time_list, self.pressure_absolute_list[:len(self.date_time_list)], label="Trykk absolute", color="blue")

    figure, axis = plt.subplots(2, 1, figsize=(12, 8))

    axis[0].plot(sola_dt, sola_temp, label='Temperature MET', color='green')
    axis[0].plot(rune_temp_dt[:len(rune_temp_list)], rune_temp_list, label="Temperatur", color="blue")
    axis[0].plot(avg_times, avg_temps, label='Gjennomsnittt temperatur', color='orange')

    axis[0].legend()
    axis[0].grid(False)
    axis[0].tick_params(axis="x", rotation=45)

    axis[1].plot(rune_bar_dt[::6], rune_bar_pressure[:-1], label='Trykk Barometer', color='orange')
    axis[1].plot(sola_dt, sola_pressure, label='Absolutt Trykk MET', color='green')
    axis[1].plot(rune_abs_dt, rune_abs_pressure, label="Trykk absolute", color="blue")

    axis[1].legend()
    axis[1].grid(False)
    axis[1].tick_params(axis="x", rotation=45)

    plt.tight_layout()
    plt.show()


plot_data()
