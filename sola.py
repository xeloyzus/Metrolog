import os
from datetime import datetime
from matplotlib import pyplot as plt

class SolaMetroData:
    def __init__(self, file_name):
        # Initialize the data lists
        self.file_name = file_name
        self.temp_list = []
        self.date_time_list = []
        self.pressure_list = []
        self.temp_fall_list = []
        self.temp_fall_datetime_list = []
        self.pressure_fall_list = []
    

    def load_data(self):
        """Loads data from the CSV file and processes temperature and pressure."""
        working_dir = os.getcwd()
        file_path = os.path.join(working_dir, 'datafiler', self.file_name)

        try:
            with open(file_path, "r", encoding='utf-8') as file:
                data = file.readlines()
                for index, lines in enumerate(data):
                    if index == 0 or index == len(data) - 1:
                        continue
                    lines = lines.strip()
                    columns = lines.split(';')
                    if len(columns) < 5:
                        continue
                    date_time_value = columns[2]
                    temperature = columns[3].replace(",", ".")
                    pressure = columns[4].replace(",", ".")

                    self.process_data(index, date_time_value, temperature, pressure)

        except Exception as e:
            print(f"An error occurred: {e}")

    def process_data(self, index, date_time_value, temperature, pressure):
        """Processes each line of data and appends valid entries to the lists."""
        try:
            date_time_obj = datetime.strptime(date_time_value, '%d.%m.%Y %H:%M')
            self.date_time_list.append(date_time_obj)
        except Exception as e:
            print(f"Skipping line {index} due to invalid date format: {date_time_value} | Error: {e}")
            return

        if not temperature:
            return

        try:
            temperature = float(temperature)
            pressure = float(pressure)
            self.temp_list.append(temperature)
            self.pressure_list.append(pressure)
        except Exception as e:
            print(f"Skipping line {index} due to invalid temperature or pressure values | Error: {e}")
            return

        self.filter_temp_fall(date_time_obj, temperature, pressure)

    def filter_temp_fall(self, date_time_obj, temperature, pressure):
        """Filters temperature and pressure within the specific date range."""
        start_date = datetime(2021, 6, 11, 17, 31)
        end_date = datetime(2021, 6, 12, 3, 5)

        if start_date <= date_time_obj <= end_date:
            self.temp_fall_list.append(temperature)
            self.temp_fall_datetime_list.append(date_time_obj)
            self.pressure_fall_list.append(pressure)

    def get_temp_fall(self):
        """Returns temperatures and pressures during the specified fall period."""
        return self.temp_fall_datetime_list, self.temp_fall_list, self.pressure_fall_list

    def get_temperatures(self):
        """Returns the list of temperatures."""
        return self.date_time_list, self.temp_list

    def get_pressures(self):
        """Returns the list of pressures."""
        return self.date_time_list, self.pressure_list

class PlotSolaMetro:
    def __init__(self, data_class):
        self.data_class = data_class

    def plot_temperature_and_pressure(self):
        """Plots temperature and pressure over the filtered date range."""
        self.data_class.load_data()
        sola_dt, sola_temp = self.data_class.get_temperatures()
        sola_tempfall_dt, sola_tempfall_liste, sola_trykk_fall_liste = self.data_class.get_temp_fall()
        self.date_time_list, self.pressure_list= self.data_class.get_pressures()

        plt.figure(figsize=(12, 6))
        plt.figure(1)
        plt.subplot(2,1,1)

        plt.plot(sola_dt, sola_temp, label='Temperature MET', color='green')
        plt.plot(sola_tempfall_dt, sola_tempfall_liste, label='Temperature Fall', color='red')

        plt.subplot(2,1,2)
        plt.plot(self.date_time_list[:len(self.pressure_list)], self.pressure_list, label="Lufttrykk", color="green")

        plt.xlabel('Date-Time')
        plt.ylabel('Values')
        plt.title('Temperature and Pressure over Time')
        plt.legend()
        plt.grid(False)

        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()


# Instantiate and run
data_processor = SolaMetroData('temperatur_trykk_met_samme_rune_time_datasett.csv')
plotter = PlotSolaMetro(data_processor)
plotter.plot_temperature_and_pressure()
