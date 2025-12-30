import pandas as pd
import os

class Olist:

    def __init__(self):
        self.path = os.path.expanduser("~/.workintech/olist/data/csv")

    def get_data(self, file_name):
        file_path = os.path.join(self.path, file_name)
        return pd.read_csv(file_path)

    def ping(self):
        return "pong"

