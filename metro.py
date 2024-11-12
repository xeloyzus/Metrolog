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


def calculate_moving_average(date_time, data, n):
    avg_times = []
    avg_data = []

    # Loop over each valid time and temperature index
    for i in range(n, len(data) - n):
        avg_times.append(date_time[i])  # Only append valid times (those that won't go out of bounds)
        avg_data.append(np.mean(data[i - n:i + n + 1]))  # Calculate the mean for n previous, current, and n next

    return avg_times, avg_data

# Function to calculate the moving standard deviation with sample adjustment
# The Standard deviation must be >=0 and <=1
def calculate_moving_std(times, temps, n):
    std_times = []
    std_temps = []

    # Loop over each valid time and temperature index
    for i in range(n, len(temps) - n):
        std_times.append(times[i])  # Only append valid times

        # Calculate the sample standard deviation for the window
        std_temps.append(np.std(temps[i - n:i + n + 1], ddof=1))

    return std_times, std_temps

rune_bar_dt, rune_bar_pressure = rune_processor.get_pressures_bar()
rune_abs_dt, rune_abs_pressure = rune_processor.get_pressures_abs()
rune_temp_dt, rune_temp_list = rune_processor.get_temperatures()
rune_max_temp_fall_dt, rune_max_temp_fall_list = rune_processor.get_max_min_tempfall()

sola_dt, sola_temp = sola_processor.get_temperatures()
sola_pressure_dt, sola_pressure = sola_processor.get_pressures()
sola_max_temp_fall_dt, sola_max_temp_fall_list = sola_processor.get_max_min_tempfall()

sirdal_dt, sirdal_pressure = sirdal_processor.get_pressures()
sirdal_dt_temp, sirdal_temp = sirdal_processor.get_temperatures()
sauda_dt_trykk, sauda_trykk = sauda_processor.get_pressures()
sauda_dt, sauda_temp_list = sauda_processor.get_temperatures()

rune_avg_dt, rune_avg_temps = calculate_moving_average(rune_temp_dt, rune_temp_list, 30)

# Funksjon for å finne samsvarende tidspunkt og beregne forskjeller
def calculate_differences(rune_dt, rune_temp, rune_pressure, sola_dt, sola_temp, sola_pressure):
    temp_diffs = []
    pressure_diffs = []
    matched_times = []

    # Finn samsvarende tidspunkter
    for i, rune_time in enumerate(rune_dt):
        for j, sola_time in enumerate(sola_dt):
            # Sjekk om dato, time, og minutter (0) stemmer overens
            if rune_time == sola_time:
                temp_diff = abs(rune_temp[i] - sola_temp[j])
                pressure_diff = abs(rune_pressure[i] - sola_pressure[j])

                temp_diffs.append(temp_diff)
                pressure_diffs.append(pressure_diff)
                matched_times.append(rune_time)  # Samme tidspunkt i begge datasett

    return matched_times, temp_diffs, pressure_diffs

def diff_resultat():
    # Beregn forskjeller
    matched_times, temp_diffs, pressure_diffs = calculate_differences(rune_temp_dt, rune_temp_list, rune_abs_pressure,
                                                                      sola_dt, sola_temp, sola_pressure)

    # Finne gjennomsnittlige forskjeller
    average_temp_diff = np.mean(temp_diffs)
    average_pressure_diff = np.mean(pressure_diffs)

    # Finne tidspunkter med størst og minst forskjell
    max_temp_diff_time = matched_times[temp_diffs.index(max(temp_diffs))]
    min_temp_diff_time = matched_times[temp_diffs.index(min(temp_diffs))]

    max_pressure_diff_time = matched_times[pressure_diffs.index(max(pressure_diffs))]
    min_pressure_diff_time = matched_times[pressure_diffs.index(min(pressure_diffs))]

    # Resultater
    print(f"Gjennomsnittlig temperaturforskjell: {average_temp_diff:.2f}")
    print(f"Gjennomsnittlig trykkforskjell: {average_pressure_diff:.2f}")

    print(f"Størst temperaturforskjell ved {max_temp_diff_time}: {max(temp_diffs):.2f}")
    print(f"Minst temperaturforskjell ved {min_temp_diff_time}: {min(temp_diffs):.2f}")

    print(f"Størst trykkforskjell ved {max_pressure_diff_time}: {max(pressure_diffs):.2f}")
    print(f"Minst trykkforskjell ved {min_pressure_diff_time}: {min(pressure_diffs):.2f}")


def plot_std():
    plt.subplots(1, 1, figsize=(12, 8))
    rune_std_time, rune_std_temps = calculate_moving_std(rune_avg_dt, rune_avg_temps , 30)
    plt.errorbar(rune_std_time, rune_std_temps, yerr=rune_std_temps, errorevery=100, capsize=0, label="Temperature with Std Dev")
    plt.xlabel("Date-time")
    plt.ylabel("Temp STD")
    plt.title("Temperatur Standardavvik")

    plt.show()


def plot_data():
    figure, axis = plt.subplots(2, 1, figsize=(12, 8))

    # Todo
    axis[0].plot(sola_dt, sola_temp, label='Temperature MET', color='green')
    axis[0].plot(rune_temp_dt[:len(rune_temp_list)], rune_temp_list, label="Temperatur", color="blue")
    axis[0].plot(rune_avg_dt, rune_avg_temps , label='Gjennomsnittt temperatur', color='orange')
    axis[0].plot(rune_max_temp_fall_dt, rune_max_temp_fall_list, label='Temperatur fall', color='purple')
    axis[0].plot(sola_max_temp_fall_dt, sola_max_temp_fall_list, label='Temperatur fall sola', color='black')
    axis[0].plot(sirdal_dt_temp, sirdal_temp, label="Temperatur sirdal", color="red")
    axis[0].plot(sauda_dt, sauda_temp_list, label="Temperatur sauda", color="pink")

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

    axs[0].hist(sola_temp, bins=range(int(min(sola_temp)), int(max(sola_temp)) + 1), color='pink')
    axs[0].set_title('Temperaturer, Sola')
    axs[0].set_xlabel('Temperatur')


    axs[1].hist(rune_temp_list, bins=range(int(min(rune_temp_list)), int(max(rune_temp_list)) + 1), color='purple')
    axs[1].set_title('Temperaturer, Rune')
    axs[1].set_xlabel('Temperatur')


    plt.tight_layout()
    plt.show()

def diff_moving_average(data, n=10):
    smoothed_data = []
    for i in range(n, len(data) - n):
        window_average = np.mean(data[i - n:i + n + 1])
        smoothed_data.append(window_average)
    return smoothed_data


def trykk_diff():

    # dict mapping av date time og  trykk
    bar_pressure_dict = dict(zip(rune_bar_dt, rune_bar_pressure))
    abs_pressure_dict = dict(zip(rune_abs_dt, rune_abs_pressure))

    samtide_tid = sorted(set(rune_bar_dt).intersection(rune_abs_dt))

    like_dt = []
    like_bar_pressure = []
    like_abs_pressure = []

    for time in samtide_tid:
        # Check if the time exists in both dictionaries
        if time in bar_pressure_dict and time in abs_pressure_dict:
            like_dt.append(time)
            like_bar_pressure.append(bar_pressure_dict[time])
            like_abs_pressure.append(abs_pressure_dict[time])

    # Finn differanse mellom  abs and bar trykk
    pressure_diff = np.array(like_abs_pressure) - np.array(like_bar_pressure)

    # pressure_diff = np.array(like_bar_pressure) - np.array(like_abs_pressure)

    # Apply the moving average function to the difference
    avg_trykk_diff = diff_moving_average(pressure_diff)

    # Plot the smoothed pressure difference
    plt.figure(figsize=(12, 6))
    plt.plot(like_dt[10:-10], avg_trykk_diff, label=" Trykk Differanse", color="blue")
    plt.xlabel("Date-Time")
    plt.ylabel("Trykk Differanse (Absolutt - Barometrisk)")
    plt.title("Diff mellom Abs and Bar Trykk")
    plt.legend()
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
plot_data()
plot_histogrammene()
diff_resultat()
plot_std()
trykk_diff()



