import os.path
import pandas as pd
import numpy as np


def file_opener(file_name):
    if file_name == 'co2-fossil-by-nation_zip':
        path = os.path.join(os.getcwd(), 'Data', file_name, 'data', 'fossil-fuel-co2-emissions-by-nation_csv.csv')
        file = pd.read_csv(path, header=0)
    else:
        path = os.path.join(os.getcwd(), 'Data', file_name)
        path = os.path.join(path, f"{file_name}.csv")
        file = pd.read_csv(path, header=2)
    return file


def years_merger(population, gdp_loc, emissions):
    pop_years = population.columns[4:]
    gdp_years = gdp_loc.columns[4:]
    em_years = emissions.Year.unique().astype('str')
    all_years = np.intersect1d(np.intersect1d(gdp_years, pop_years), em_years)
    emissions = emissions[emissions.Year.isin(all_years.astype('int'))]
    gdp_loc = pd.concat([gdp_loc.iloc[:, [0, 1, 2, 3]], gdp_loc.loc[:, all_years]], axis=1)
    population = pd.concat([population.iloc[:, [0, 1, 2, 3]], population.loc[:, all_years]], axis=1)
    return[population, gdp_loc, emissions]


def years_interval_merger(population, gdp_loc, emissions, beginning, end):
    beginning = int(beginning)
    end = int(end) + 1
    all_years = list(range(beginning, end))
    emissions = emissions[emissions.Year.isin(all_years)]
    all_years = list(map(str, all_years))
    gdp_loc = pd.concat([gdp_loc.iloc[:, [0, 1, 2, 3]], gdp_loc.loc[:, all_years]], axis=1)
    population = pd.concat([population.iloc[:, [0, 1, 2, 3]], population.loc[:, all_years]], axis=1)
    return[population, gdp_loc, emissions]

