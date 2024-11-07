from datetime import datetime


class SolaMetroDataProcessor:

    def __init__(self):
        # Initialize the data lists
        self.temp_list = []
        self.date_time_list = []
        self.pressure_list = []
        self.temp_fall_list = []
        self.temp_fall_datetime_list = []
        self.pressure_fall_list = []
        self.max_min_temps = []
        self.max_min_dates = []

    def load_data(self, filepath):
        try:
            with open(filepath, "r", encoding='utf-8') as file:
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

                self.max_min_temp_fall()

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
            pressure = float(pressure) / 10
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

    def max_min_temp_fall(self):
        start_date = datetime(2021, 6, 11, 17, 0)
        end_date = datetime(2021, 6, 12, 3, 0)
        temps_in_range = []
        for date_time_obj, temp_val in zip(self.temp_fall_datetime_list, self.temp_fall_list):
            if start_date <= date_time_obj <= end_date:
                temps_in_range.append((date_time_obj, temp_val))

        if temps_in_range:
            start_temp = temps_in_range[0]
            end_temp = temps_in_range[-1]

            self.max_min_dates = [start_temp[0], end_temp[0]]
            self.max_min_temps = [start_temp[1], end_temp[1]]

    def get_max_min_tempfall(self):
        return self.max_min_dates, self.max_min_temps

    def get_temperatures(self):
        """Returns the list of temperatures."""
        return self.date_time_list, self.temp_list

    def get_pressures(self):
        """Returns the list of pressures."""
        return self.date_time_list, self.pressure_list