import os.path
import pandas as pd
import numpy as np
import re


# function input: folder name of relevant data
# output: required data-file in python environment  with .csv extension
# function works only on file system  which
# structure is the same as the one supplied by learning team to moodle (plus unpacked)
def file_opener(file_name):
    if file_name == 'co2-fossil-by-nation_zip':
        path = os.path.join(os.getcwd(), 'Data', file_name, 'data', 'fossil-fuel-co2-emissions-by-nation_csv.csv')
        file = pd.read_csv(path, header=0)
    else:
        path = os.path.join(os.getcwd(), 'Data', file_name)
        path = os.path.join(path, f"{file_name}.csv")
        file = pd.read_csv(path, header=2)
    return file


# Function that selects years in data if no other year-span is supplied
# input: set of three data-like structures
# output: set of three data-like structures but trimmed to have the same year span which is the intersection of
# year spans of those three
def years_merger(population, gdp_loc, emissions):
    pop_years = population.columns[1:]
    gdp_years = gdp_loc.columns[1:]
    em_years = emissions.Year.unique().astype('str')
    all_years = np.intersect1d(np.intersect1d(gdp_years, pop_years), em_years)
    emissions = emissions[emissions.Year.isin(all_years.astype('int'))]
    gdp_loc = pd.concat([gdp_loc.iloc[:, [0]], gdp_loc.loc[:, all_years]], axis=1)
    population = pd.concat([population.iloc[:, [0]], population.loc[:, all_years]], axis=1)
    return[population, gdp_loc, emissions]


# Function that selects years in data if  other year-span is supplied
# input: set of three data-like structures
# output: set of three data-like structures but trimmed to relevant year interval.
def years_interval_merger(population, gdp_loc, emissions, beginning, end):
    beginning = int(beginning)
    end = int(end) + 1
    all_years = list(range(beginning, end))
    emissions = emissions[emissions.Year.isin(all_years)]
    all_years = list(map(str, all_years))
    gdp_loc = pd.concat([gdp_loc.iloc[:, [0]], gdp_loc.loc[:, all_years]], axis=1)
    population = pd.concat([population.iloc[:, [0]], population.loc[:, all_years]], axis=1)
    return[population, gdp_loc, emissions]


# Function that cleans columns with country names, changes letters to lower ones and removes all words in brackets
# input: column of relevant data frame
# output: column of data frame but with changed letters to lower ones and removed all words in brackets
def country_cleaner(data):
    data = data.apply(lambda x: x.lower()).apply(lambda x: re.sub(" \(.*?\)", "", x))
    return data


# Function that measures changes in emission per capita in last 10 years present in supplied dataframe
def emission_balance(data):
    years = [0, 0]
    years[0], years[1] = data.Year.unique()[-1], data.Year.unique()[-11]
    loss = data[data.Year.isin(years)]
    loss.loc[loss.Year.isin([years[1]]), ['Emissions per Capita']] \
        = loss[loss.Year.isin([years[1]])]['Emissions per Capita'].apply(lambda x: -x)
    r1 = loss.groupby(['Country Name'])["Emissions per Capita"].sum().nlargest()
    r2 = loss.groupby(['Country Name'])["Emissions per Capita"].sum().nsmallest()
    return[r1, r2]