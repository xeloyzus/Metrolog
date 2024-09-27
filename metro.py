
import matplotlib.pyplot as plt

from metro_data import metro_data

def csv_plotting():
    y_temp, x_date = metro_data()
    plt.title("X vs Y")
    plt.plot(x_date,y_temp)
    plt.show()

csv_plotting()