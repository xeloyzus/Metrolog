import matplotlib.pyplot as plt
import matplotlib.dates as mdates

from rune_metro_data import rune_metro_data, temp_date_data, date_time
from sola_metro_data import sola_metro_data


def csv_plotting():
    #date_time, temp, temp_fall, avg_temp, pressure_barometer, pressure_absolute = rune_metro_data()
    #date_time, temp = temp_date_data()
    sola_date_time, sola_temp, _,_ = sola_metro_data()

    sola_plotting(sola_date_time, sola_temp)

    # Add a legend and layout
    plt.legend()
    plt.tight_layout()

    # Show the plot
    plt.show()

def sola_plotting(date_time, temp):

    # Create the plot
    plt.figure(figsize=(10, 6))
    # Plot 1: Temperature vs Time
    plt.subplot(2, 1, 1)
    plt.plot(date_time, temp, color='green', linestyle='-')  # No connecting lines, just markers

    # Add titles and labels
    plt.title("Temperature Vs Time", fontsize=16)
    plt.xlabel("Date", fontsize=14)
    plt.ylabel("Temp (°C)", fontsize=14)
    plt.grid(False)

# Call the plotting function
csv_plotting()
