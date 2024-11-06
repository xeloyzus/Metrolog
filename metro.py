import os
import matplotlib.pyplot as plt
import numpy as np

from sauda import SaudaMetroDataProcessor
from sirdal import SirdalMetroDataProcessor
from rune import RuneMetroDataProcessor
from sola import SolaMetroDataProcessor

rune_processor = RuneMetroDataProcessor()
rune_filepath = os.path.join(os.getcwd(), 'datafiler', 'trykk_og_temperaturlogg_rune_time.csv')
rune_processor.load_data(rune_filepath)

sola_processor = SolaMetroDataProcessor()
sola_filepath = os.path.join(os.getcwd(), 'datafiler', 'temperatur_trykk_met_samme_rune_time_datasett.csv')
sola_processor.load_data(sola_filepath)

sirdal_processor = SirdalMetroDataProcessor()
sirdal_filepath = os.path.join(os.getcwd(), 'datafiler', 'temperatur_trykk_sauda_sinnes_samme_tidsperiode.csv.txt')
sirdal_processor.load_data(sirdal_filepath)


sauda_processor = SaudaMetroDataProcessor()
sauda_filepath = os.path.join(os.getcwd(), 'datafiler', 'temperatur_trykk_sauda_sinnes_samme_tidsperiode.csv.txt')
sauda_processor.load_data(sauda_filepath)


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
    rune_max_temp_fall_dt, rune_max_temp_fall_list = rune_processor.get_max_min_tempfall()
    sola_max_temp_fall_dt, sola_max_temp_fall_list= sola_processor.get_max_min_tempfall()
    sirdal_dt, sirdal_pressure = sirdal_processor.get_pressures()
    sirdal_dt_temp, sirdal_temp = sirdal_processor.get_temperatures()
    sauda_dt_trykk, sauda_trykk = sauda_processor.get_pressures()
    sauda_dt_temp, sauda_temp = sauda_processor.get_temperatures()

        
    avg_times, avg_temps = calculate_moving_average(rune_temp_dt, rune_temp_list, 30)

   
    figure, axis = plt.subplots(2, 1, figsize=(12, 8))
    #Todo
    axis[0].plot(sola_dt, sola_temp, label='Temperature MET', color='green')
    axis[0].plot(rune_temp_dt[:len(rune_temp_list)], rune_temp_list, label="Temperatur", color="blue")
    axis[0].plot(avg_times, avg_temps, label='Gjennomsnittt temperatur', color='orange')
    axis[0].plot(rune_max_temp_fall_dt, rune_max_temp_fall_list, label='Temperatur fall', color='purple')
    axis[0].plot(sola_max_temp_fall_dt, sola_max_temp_fall_list, label='Temperatur fall sola', color='black')
    axis[0].plot(sirdal_dt_temp, sirdal_temp, label="Temperatur sirdal", color="red")
    axis[0].plot(sauda_dt_temp, sauda_temp, label="Temperatur sauda", color="pink")


   
    axis[0].legend()
    axis[0].grid(False)
    axis[0].tick_params(axis="x", rotation=45)

    axis[1].plot(rune_bar_dt[::6], rune_bar_pressure[:-1], label='Trykk Barometer', color='orange')
    axis[1].plot(sola_dt, sola_pressure, label='Absolutt Trykk MET', color='green')
    axis[1].plot(rune_abs_dt, rune_abs_pressure, label="Trykk absolute", color="blue")
    axis[1].plot(sirdal_dt, sirdal_pressure, label="Trykk sirdal", color="red")
    axis[1].plot(sauda_dt_trykk, sauda_trykk, label="Trykk sauda", color="pink")


    axis[1].legend()
    axis[1].grid(False)
    axis[1].tick_params(axis="x", rotation=45)

    plt.tight_layout()
    plt.show()

def plot_histogrammene():
    _, sola_temp = sola_processor.get_temperatures()
    _, rune_temp_list = rune_processor.get_temperatures()

    fig, axs = plt.subplots(1, 2, figsize=(12, 5))
    
    axs[0].hist(sola_temp, bins=range(int(min(sola_temp)), int(max(sola_temp))+1))
    axs[0].set_title('Temperaturer, Sola')
    axs[0].set_xlabel('Temperatur')
    axs[0].legend()

    axs[1].hist(rune_temp_list, bins=range(int(min(rune_temp_list)), int(max(rune_temp_list)) + 1))
    axs[1].set_title('Temperaturer, Rune')
    axs[1].set_xlabel('Temperatur')
    axs[1].legend()

    plt.tight_layout()
    plt.show()

plot_data()
plot_histogrammene()
