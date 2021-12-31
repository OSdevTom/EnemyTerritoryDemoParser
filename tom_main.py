import pandas as pd
import os
dir_name = 'C:\demos'

# import pandas module
import pandas as pd
import numpy as np
import data_preparation

df_appended = pd.DataFrame()

for dir in os.listdir(dir_name):
    for filename in os.listdir(os.path.join(dir_name, dir)):
        df = pd.read_csv(os.path.join(dir_name, dir, filename), sep=';')
        df_output = data_preparation.demo_to_dataframe_parser(df)
        ##print(df_output)
        df_appended = df_appended.append(df_output, ignore_index=True)
        ###print(df_appended)
        df_appended.describe()
