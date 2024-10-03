import matplotlib.pyplot as plt
import matplotlib.dates as mdates

from rune_metro_data import rune_metro_data, temp_date_data, date_time
from sola_metro_data import sola_metro_data


def csv_plotting():
    #date_time, temp, temp_fall, avg_temp, pressure_barometer, pressure_absolute = rune_metro_data()
    #date_time, temp = temp_date_data()
    sola_date_time, sola_temp, _,_ = sola_metro_data()
    rune_date_time,rune_temp, _, _ , _ = rune_metro_data()

    sola_plotting(sola_date_time, sola_temp, rune_date_time, rune_temp)

    # Add a legend and layout
    plt.legend()
    plt.tight_layout()

    # Show the plot
    plt.show()

def sola_plotting(date_time, temp, rune_date_time, rune_temp):

    # Create the plot
    plt.figure(figsize=(10, 6))
    # Plot 1: Temperature vs Time
    plt.subplot(2, 1, 1)
    plt.plot(date_time, temp, label="Temperatur MET", color='green', linestyle='-')  # No connecting lines, just markers

    plott_temp_rune(rune_date_time, rune_temp)

    # Add titles and labels
    plt.title("Temperature Vs Time", fontsize=16)
    plt.xlabel("Date", fontsize=14)
    plt.ylabel("Temp (°C)", fontsize=14)
    plt.grid(False)

def plott_temp_rune(date_time, temp): 

    plt.plot(date_time, temp, color='blue', linestyle='-')
    plt.title('Temperatur', fontsize=16)

# Call the plotting function


def rune_plotting(date_time, temp):

    # Create the plot
    plt.figure(figsize=(10, 6))
    # Plot 1: Temperature vs Time
    plt.subplot(2, 1, 2)
    plt.plot(date_time, temp, label= "Temperatur", color='green', linestyle='-')  # No connecting lines, just markers

    # Add titles and

csv_plotting()