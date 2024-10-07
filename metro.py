import os

import matplotlib.pyplot as plt

from rune import RuneMetroDataProcessor

# Usage example
rune_processor = RuneMetroDataProcessor()
rune_filepath = os.path.join(os.getcwd(), 'datafiler', 'trykk_og_temperaturlogg_rune_time.csv')
rune_processor.load_data(rune_filepath)
rune_processor.plot_data()
