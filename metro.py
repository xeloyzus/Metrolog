import os

import matplotlib.pyplot as plt

from rune import RuneMetroDataProcessor
from sola import SolaMetroDataProcessor

rune_processor = RuneMetroDataProcessor()
rune_filepath = os.path.join(os.getcwd(), 'datafiler', 'trykk_og_temperaturlogg_rune_time.csv')
rune_processor.load_data(rune_filepath)

sola_processor = SolaMetroDataProcessor()
sola_filepath = os.path.join(os.getcwd(), 'datafiler', 'temperatur_trykk_met_samme_rune_time_datasett.csv')
sola_processor.load_data(sola_filepath)


def plot_data():
    rune_bar_dt, rune_bar_pressure = rune_processor.get_pressures_bar()
    rune_abs_dt, rune_abs_pressure = rune_processor.get_pressures_bar()
    rune_temp_dt, rune_temp_list = rune_processor.get_temperatures()

    sola_dt, sola_temp = sola_processor.get_temperatures()
    sola_pressure_dt, sola_pressure = sola_processor.get_pressures()
    sola_tempfall_dt, sola_tempfall_liste, _ = sola_processor.get_temp_fall()
    rune_tempfall_dt, rune_tempfall_liste  = rune_processor.get_temp_fall()

    # axis[0].plot(self.date_time_list[::6], self.pressure_barometer_list[1:], label='Trykk Barometer', color='orange')
    # axis[0].plot(self.date_time_list, self.pressure_absolute_list[:len(self.date_time_list)], label="Trykk absolute", color="blue")

    figure, axis = plt.subplots(2, 1, figsize=(12, 8))

    axis[0].plot(sola_dt, sola_temp, label='Temperature MET', color='green')

    #axis[0].plot(rune_tempfall_dt, rune_tempfall_liste  , label='Temperature Fall', color='red')
    #print(f"lentempfall dt {len(rune_tempfall_dt)} len tempfall lst{len(rune_tempfall_liste)}")
    axis[0].plot(rune_temp_dt[:len(rune_temp_list)], rune_temp_list, label="Temperatur", color="blue")

    axis[0].legend()
    axis[0].grid(False)
    axis[0].tick_params(axis="x", rotation=45)

    axis[1].plot(rune_bar_dt[::6], rune_bar_pressure[1:], label='Trykk Barometer', color='orange')
    # axis[1].plot(sola_pressure_dt,sola_pressure, label='Absolutt Trykk MET', color='green')

    # axis[1].plot(rune_abs_dt, rune_abs_pressure[:len(rune_abs_dt)], label="Trykk absolute", color="blue")

    axis[1].legend()
    axis[1].grid(False)
    axis[1].tick_params(axis="x", rotation=45)

    plt.tight_layout()
    plt.show()


plot_data()