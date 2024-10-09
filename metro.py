import os
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from rune import RuneMetroDataProcessor
from sola import SolaMetroDataProcessor

# Usage example
rune_processor = RuneMetroDataProcessor()
rune_filepath = os.path.join(os.getcwd(), 'datafiler', 'trykk_og_temperaturlogg_rune_time.csv')
rune_processor.load_data(rune_filepath)

# Instantiate and run
sola_processor = SolaMetroDataProcessor()
sola_filepath = os.path.join(os.getcwd(), 'datafiler', 'temperatur_trykk_met_samme_rune_time_datasett.csv')
sola_processor.load_data(sola_filepath)

def plot_():
    # Get temperature and pressure data
    sola_temp_dt, sola_temp_list = sola_processor.get_temperatures()
    sola_pressure_dt, sola_pressure_list = sola_processor.get_pressures()
    rune_temp_dt, rune_temp_list = rune_processor.get_temperatures()
    rune_bar_dt,rune_bar_pressure = rune_processor.get_pressures_bar()
    rune_pressure_abs_dt, rune_abs_pressure = rune_processor.get_pressures_abs()

    # Initialise the subplot function (2 rows, 1 column)
    figure, axis = plt.subplots(2, 1, figsize=(12, 8))

    # Plot for sola_temp
    axis[0].plot(sola_temp_dt, sola_temp_list, label='Temperatur MET', color='green')
    axis[0].legend()
    axis[0].grid(False)


    axis[0].tick_params(axis='x', rotation=45)
    print(f"sola dt{len(sola_temp_dt)} rune dt {len(rune_bar_pressure)}")
    # Plot for sola_pressure
    axis[1].plot(sola_temp_dt, sola_pressure_list, label='Pressure MET', color='blue')
    #axis[1].plot(rune_bar_dt,rune_bar_pressure,label='Barometrisk trykk',color='orange')
    axis[1].legend()
    axis[1].grid(False)

    axis[1].tick_params(axis='x', rotation=45)

    # Adjust layout and display the plots
    plt.tight_layout()
    plt.show()

plot_()
