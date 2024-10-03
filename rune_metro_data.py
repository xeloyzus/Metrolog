import os
from datetime import datetime

# Define lists to hold data
temp = []
avg_temp = []
temp_fall = []
date_time = []
pressure_barometer = []
pressure_absolute = []
valid_times = []
averaged_temps = []

def rune_metro_data():
    # Get the current working directory
    working_dir = os.getcwd()
    print(working_dir)

    global temp, temp_fall, date_time, pressure_barometer, pressure_absolute,valid_times, averaged_temps

    try:
        # Open the CSV file manually
        file_path = os.path.join(working_dir, 'datafiler', 'trykk_og_temperaturlogg_rune_time.csv')  # Update the file name
        print(f"Reading file: {file_path}")  # Check if the correct file is being accessed
        with open(file_path, "r", encoding='utf-8') as rune_csv:
            data = rune_csv.readlines()
            print(f"Total lines in file: {len(data)}")  # Debugging line to check how many rows are read

            # Loop through each line in the file
            for index, lines in enumerate(data):
                # Skip the header row (index 0 only)
                if index == 0:
                    continue

                # Strip any extra whitespace or newline characters
                lines = lines.strip()

                # Split the line using semicolon as the delimiter
                columns = lines.split(';')

                # Ensure that the line has at least 5 columns
                if len(columns) < 5:
                    print(f"Skipping line {index} due to insufficient columns")
                    continue

                # Assign each column to a variable
                date_time_value = columns[0]
                pressure_baro = columns[2].replace(",", ".")  # Replace comma with a dot for float conversion
                pressure_abs = columns[3].replace(",", ".")  # Replace comma with a dot for float conversion
                temperature = columns[4].replace(",", ".")  # Replace comma with a dot for float conversion

                # Append the date and time, converting to datetime
                try:
                    # Handle AM/PM time format
                    if "am" in date_time_value.lower() or "pm" in date_time_value.lower():
                        if "00:" in date_time_value:
                            date_time_value = date_time_value.replace("00:", "12:")
                        date_time_obj = datetime.strptime(date_time_value, '%m/%d/%Y %I:%M:%S %p')
                    else:
                        date_time_obj = datetime.strptime(date_time_value, '%d.%m.%Y %H:%M')

                    date_time.append(date_time_obj)  # Append if valid

                except Exception as e:
                    print(f"Skipping line {index} due to invalid date format: {date_time_value} | Error: {e}")
                    continue

                # Convert pressure and temperature to float if available
                try:
                    if pressure_baro:  # Check if the barometer pressure value exists
                        pressure_baro = float(pressure_baro)
                        pressure_barometer.append(pressure_baro)

                    if pressure_abs:  # Check if the absolute pressure value exists
                        pressure_abs = float(pressure_abs)
                        pressure_absolute.append(pressure_abs)

                    if temperature:  # Check if temperature value exists
                        temperature = float(temperature)
                        temp.append(temperature)

                        # Get the temperature fall
                        start_date = datetime(2021, 6, 11, 17, 31)
                        end_date = datetime(2021, 6, 12, 3, 5)
                        if date_time_obj == start_date or end_date:
                            temp_fall = temp

                except Exception as e:
                    print(f"Skipping line {index} due to invalid temperature or pressure values | Error: {e}")
                    continue


    except Exception as e:
        print(f"An error occurred: {e}")

    # Return the variables you're interested in
    return  date_time, temp, temp_fall, pressure_barometer, pressure_absolute


date_time,temp, _, _ , _= rune_metro_data()


# Step 2: Define the moving average function
def average_temp_date(timestamps, temps, n):
    # Loop through the temperatures, excluding the first and last n values
    for i in range(n, len(temps) - n):
        # Calculate the average of the current window (2n+1 values)
        window = temps[i - n:i + n + 1]
        window_avg = sum(window) / len(window)
        # Round the average to two decimal places
        window_avg = round(window_avg, 2)
        # Append the valid timestamp and corresponding averaged temperature
        valid_times.append(timestamps[i])
        averaged_temps.append(window_avg)

    return valid_times, averaged_temps


def temp_date_data():
    # Step 3: Apply the moving average with n=30 (or smaller for this example)
    n = 30  # You can adjust this number
    times, avgtemp = average_temp_date(date_time, temp, n)
    return times, avgtemp

valid_times, averaged_temps = temp_date_data()
# Print the results
for time, avg_temp in zip(valid_times, averaged_temps):
    print(f"Valid Time: {time.strftime('%Y-%m-%d %H:%M')}, Averaged Temperature: {avg_temp}")