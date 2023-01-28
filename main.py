import argparse
import csv
import os.path
import numpy as np
import pandas as pd


def file_opener(file_name):
    if file_name == 'co2-fossil-by-nation_zip':
        path = os.path.join(os.getcwd(), 'Data', file_name, 'data', 'fossil-fuel-co2-emissions-by-nation_csv.csv')
    else:
        path = os.path.join(os.getcwd(), 'Data', file_name)
        path = os.path.join(path, f"{file_name}.csv")
    file = pd.read_csv(path, header=2)
    return file


gdp = file_opener('API_NY.GDP.MKTP.CD_DS2_en_csv_v2_4751562')
pop = file_opener('API_SP.POP.TOTL_DS2_en_csv_v2_4751604')
emiss = file_opener('co2-fossil-by-nation_zip')
print(pop.columns)
print(gdp.columns)
print(emiss)

