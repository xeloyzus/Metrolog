import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from metro_data_rune import metro_data

def csv_plotting():
    # Fetch temperature and date-time data
    y_temp, x_date, _ = metro_data()  # Fetch pressure data if needed but ignore it here
    avg_temp = average_temperature(y_temp)

    # Create the plot
    plt.figure(figsize=(10, 6))

    # Plot 1: Temperature vs Time
    plt.subplot(2, 1, 1)
    plt.plot(x_date, y_temp, label='Temperature', color='b', marker='o', linestyle='')  # No connecting lines, just markers
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m-%d %H'))  # Format as MM/DD HH
    plt.xticks(rotation=45)  # Rotate for readability

    # Add titles and labels
    plt.title("Temperature Vs Time", fontsize=16)
    plt.xlabel("Date", fontsize=14)
    plt.ylabel("Temp (°C)", fontsize=14)
    plt.grid(True)

    # Plot 2: Average Temperature as a line across all dates
    plt.subplot(2, 1, 2)
    plt.plot(x_date, [avg_temp] * len(x_date), label=f'Average Temp = {avg_temp:.2f}°C', color='r', linestyle='--')  # Horizontal line
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m-%d %H'))  # Format as MM/DD HH
    plt.xticks(rotation=45)  # Rotate for readability

    # Add titles and labels
    plt.title("Average Temperature Over Time", fontsize=16)
    plt.xlabel("Date", fontsize=14)
    plt.ylabel("Avg Temp (°C)", fontsize=14)
    plt.grid(True)

    # Add a legend and layout
    plt.legend()
    plt.tight_layout()

    # Show the plot
    plt.show()

def average_temperature(temperatures):
    if not temperatures:
        return None  # Handle the case where the list is empty
    return sum(temperatures) / len(temperatures)

# Call the plotting function
csv_plotting()
