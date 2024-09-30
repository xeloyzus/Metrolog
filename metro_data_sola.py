import os
from datetime import datetime

# Define lists to hold data
temp = []
date_Time = []
lufttrykk = []

def metro_data_sola():
    # Get the current working directory
    working_dir = os.getcwd()

    try:
        # Open the CSV file manually
        file_path = os.path.join(working_dir, 'datafiler', 'temperatur_trykk_met_samme_rune_time_datasett.csv')
        print(f"Reading file: {file_path}")  # Check if the correct file is being accessed
        with open(file_path, "r", encoding='utf-8') as rune_csv:
            data = rune_csv.readlines()
            print(f"Total lines in file: {len(data)}")  # Debugging line to check how many rows are read

            # Loop through each line in the file
            for index, lines in enumerate(data):

                # Skip the header and the last row
                if index == 0 or index == len(data) - 1:
                    continue

                # Strip any extra whitespace or newline characters
                lines = lines.strip()
                # Split the line using semicolon as the delimiter
                columns = lines.split(';')

                # Ensure that the line has at least 5 columns
                if len(columns) < 5:

                    continue
                # Assign each column to a variable
                location = columns[0]
                station_id = columns[1]
                date_time_value = columns[2]
                temperature = columns[3].replace(",", ".")  # Replace comma with a dot for float conversion
                pressure = columns[4].replace(",", ".")  # Replace comma with a dot for float conversion

                # Append the date and time, converting to datetime
                try:
                    date_time_obj = datetime.strptime(date_time_value, '%d.%m.%Y %H:%M')  # Updated format
                    date_Time.append(date_time_obj)
                except Exception as e:
                    print(f"Skipping line {index} due to invalid date format: {date_time_value} | Error: {e}")
                    continue

                # Skip if temperature is empty
                if not temperature:
                    print(f"Skipping line {index} due to empty temperature")
                    continue

                # Convert temperature and pressure to float
                try:
                    temperature = float(temperature)
                    pressure = float(pressure)
                except Exception as e:
                    print(f"Skipping line {index} due to invalid temperature or pressure values | Error: {e}")
                    continue

                # Append temperature and pressure
                temp.append(temperature)
                lufttrykk.append(pressure)

        print(f"Temperature: {temp}")
        print(f"Date-Time: {date_Time}")
        print(f"Pressure: {lufttrykk}")

    except Exception as e:
        print(f"An error occurred: {e}")

    # Return the variables you're interested in
    return temp, date_Time, lufttrykk

# Call the function
metro_data_sola()
