import pandas as pd
from tqdm import *

class ToCSV:
    def __init__(self, data):
        self.data = data

    def write(self, col_name, path, filename):
        combined_df = pd.concat(self.data, axis=1, keys=col_name)
        combined_df.to_csv(f"{path}/{filename}")
        tqdm.write(f"CSV file saved to {path}/{filename}")
        