import os
from datetime import datetime

# Define lists to hold data
temp = []
date_time = []
pressure_barometer = []
pressure_absolute = []


def metro_data_rune():
    # Get the current working directory
    working_dir = os.getcwd()
    print(working_dir)

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

                # Debugging: print the columns to see if data splits correctly
                print(f"Columns: {columns}")

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
                    # Check for different date formats
                    if "pm" in date_time_value.lower() or "am" in date_time_value.lower():
                        date_time_obj = datetime.strptime(date_time_value,
                                                          '%m/%d/%Y %I:%M:%S %p')  # Format for '06/13/2021 09:53:18 pm'
                    else:
                        date_time_obj = datetime.strptime(date_time_value,
                                                          '%d.%m.%Y %H:%M')  # Format for '06.11.2021 14:23'

                    date_time.append(date_time_obj)
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

                except Exception as e:
                    print(f"Skipping line {index} due to invalid temperature or pressure values | Error: {e}")
                    continue

        print(f"Temperature: {temp}")
        print(f"Date-Time: {date_time}")
        print(f"Barometer Pressure: {pressure_barometer}")
        print(f"Absolute Pressure: {pressure_absolute}")

    except Exception as e:
        print(f"An error occurred: {e}")

    # Return the variables you're interested in
    return temp, date_time, pressure_barometer, pressure_absolute


# Call the function for testing
metro_data_rune()  # Uncomment this line to test the function
