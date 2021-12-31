import pandas as pd
import os
dir_name = 'C:\demos'

# import pandas module
import pandas as pd
import numpy as np
import data_preparation
from basesvdd import BaseSVDD

###demos are organized by players###
###each player has a folder in which all of their demos are stored###
###so we loop in each folder to read each demos###
###and we append each demo from each player into a large ABT###
###df_appended is out ABT = Analytical Based Table###

df_appended = pd.DataFrame()

for dir in os.listdir(dir_name):
    for filename in os.listdir(os.path.join(dir_name, dir)):
        df = pd.read_csv(os.path.join(dir_name, dir, filename), sep=';', nrows=300)
        df_output = data_preparation.demo_to_dataframe_parser(df)
        ##print(df_output)
        df_appended = df_appended.append(df_output, ignore_index=True)
        ###print(df_appended)

# svdd object using rbf kernel

df_appended = df_appended.drop(columns=["player","timestamp","shooting","hit","gun","crouch"])
training_data = df_appended.to_numpy()

svdd = BaseSVDD(C=0.9, gamma=0.3, kernel='rbf', display='on')

# fit the SVDD model
svdd.fit(training_data)

