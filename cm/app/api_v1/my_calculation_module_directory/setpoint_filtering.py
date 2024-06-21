import numpy as np
import pandas as pd
import os

#adapt to coollife structure
#path2data = os.path.split(os.path.abspath(__file__))[0]
#unfiltered_setpoints_dataframe = os.path.join(path2data,"data/setpoints_per_nuts0.csv")

def filter_data_general(df , filter_parameter, filter_coloumn):
        filtered_df = df.copy()  # Make a copy of the original DataFrame
              filtered_df = filtered_df[filtered_df[filter_coloumn] == str(filter_parameter)]
        return filtered_df
