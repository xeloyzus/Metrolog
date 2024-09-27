import os
working_dir = os.getcwd()
temp =[]
date_Time=[]
Lufttemperatur = []
temp_snitt=[]
lufttrykk=[]
tempfall_maks_min= []
temp_met=[]
tempfall_solned_solopp =[]

def metro_data():
    working_dir = os.getcwd()
    try:
        with open(f"{working_dir}/datafiler/temperatur_trykk_met_samme_rune_time_datasett.csv", "r") as rune_csv:
            data = rune_csv.readlines()
            #Lopp through the csv file and check for  the index of the each line
            for index, lines in enumerate(data):
                #check for the end of the file such that its not read
                if index == 0 or index == len(data) - 1:
                    continue
                # Strip any extra whitespace or newline characters
                lines = lines.strip()

                # Split the line using semicolon as the delimiter
                columns = lines.split(';')

                # Assign each column to a variable
                location = columns[0]
                station_id = columns[1]
                date_time = columns[2]
                temperature = columns[3].replace(",", ".")  # Replace comma with a dot for float conversion
                pressure = columns[4].replace(",", ".")  # Replace comma with a dot for float conversion
                date_Time.append(date_time)
                if not temperature :
                    continue
                else:
                    # Convert temperature and pressure to float
                    temperature = float(temperature)
                    pressure = float(pressure)
                    temp.append(temperature)
                    lufttrykk.append(pressure)

        print(f" temp {temp}")
        print(f" date-time {date_Time}")

    except Exception as e:

        print(f"{e}")
    return temp, date_Time