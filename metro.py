import os

import matplotlib.pyplot as plt

from rune import RuneMetroDataProcessor
from sola import SolaMetroData
from sola import PlotSolaMetro

# Usage example
rune_processor = RuneMetroDataProcessor()
rune_filepath = os.path.join(os.getcwd(), 'datafiler', 'trykk_og_temperaturlogg_rune_time.csv')
rune_processor.load_data(rune_filepath)
rune_processor.plot_data()
sola_processor = SolaMetroData()
#sola_processor = PlotSolaMetro()
sola_filepath = os.path.join(os.getcwd(), 'datafiler', 'temperatur_trykk_met_samme_rune_time_datasett.csv')
sola_processor.load_data(sola_filepath)
sola_processor.plot_data()
