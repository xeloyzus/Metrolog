import os
from datetime import datetime
import numpy as np
from matplotlib import pyplot as plt
from sola import SolaMetroData



# Define a class to encapsulate the data handling
class RuneMetroDataProcessor:
    def __init__(self):
        self.temp_list = []
        self.avg_temp = []
        self.temp_fall_list = []
        self.date_time_list = []
        self.temp_fall_datetime_list = []
        self.pressure_barometer_list = []
        self.pressure_absolute_list = []
        self.valid_times_list = []
        self.averaged_temps_list = []
        self.pressure_bar_dt=[]

    def load_data(self, filepath):
        try:
            with open(filepath, "r", encoding='utf-8') as rune_csv:
                data = rune_csv.readlines()

                for index, line in enumerate(data):
                    if index == 0:
                        continue

                    line = line.strip()
                    columns = line.split(';')

                    if len(columns) < 5:
                        continue

                    date_time_value = columns[0]
                    pressure_baro = columns[2].replace(",", ".")
                    pressure_abs = columns[3].replace(",", ".")
                    temperature = columns[4].replace(",", ".")

                    self.process_data(index, date_time_value, pressure_baro, pressure_abs, temperature)

        except Exception as e:
            print(f"Error reading data: {e}")

    def process_data(self, index, date_time_value, pressure_baro, pressure_abs, temperature):
        try:
            if "am" in date_time_value.lower() or "pm" in date_time_value.lower():
                if "00:" in date_time_value:
                    date_time_value = date_time_value.replace("00:", "12:")
                date_time_obj = datetime.strptime(date_time_value, '%m/%d/%Y %I:%M:%S %p')
            else:
                date_time_obj = datetime.strptime(date_time_value, '%m.%d.%Y %H:%M')

            self.date_time_list.append(date_time_obj)

            if pressure_baro:
                self.pressure_barometer_list.append(round(float(pressure_baro),2))
                self.pressure_bar_dt.append(date_time_obj)


            if pressure_abs:
                self.pressure_absolute_list.append(float(pressure_abs))

            if temperature:
                self.temp_list.append(float(temperature))
                self.lim_temp_fall()
        except Exception as e:
            print(f"Error processing line {index}: {e}")

    def lim_temp_fall(self):
        # Define the start and end dates
        start_date = datetime(2021, 6, 11, 17, 31)
        end_date = datetime(2021, 6, 12, 3, 5)
        for date_time_obj, temp_val in zip(self.date_time_list, self.temp_list):
            # Collect temperatures and pressures within the specified date range
            if start_date <= date_time_obj <= end_date:
                self.temp_fall_list.append(temp_val)  # Append valid temperatures
                self.temp_fall_datetime_list.append(date_time_obj)
                #print(f"Time: {date_time_obj.strftime('%Y-%d-%m %H:%M')}, Temperature: {temp_val}")

    def get_temperatures(self):
        """Returns the list of temperatures."""
        return self.date_time_list, self.temp_list

    def get_pressures_abs(self):
        """Returns the list of pressures."""
        return self.date_time_list, self.pressure_absolute_list

    def get_pressures_bar(self):
        """Returns the list of pressures."""
        return self.date_time_list, self.pressure_barometer_list

  


