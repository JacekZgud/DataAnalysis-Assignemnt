import pandas as pd
import numpy as np
import re
import argparse


# function input: folder name of relevant data
# output: required data-file in python environment  with .csv extension
# function works only on file system  which
# structure is the same as the one supplied by learning team to moodle (plus unpacked)
def pars():
    parser = argparse.ArgumentParser(description='Analyse historical emissions and gdp data')
    parser.add_argument("gdp", type=argparse.FileType('r'), help="file containing gdp")
    parser.add_argument("pop", type=argparse.FileType('r'), help="file containing populations")
    parser.add_argument("em", type=argparse.FileType('r'), help="file containing emissions")
    parser.add_argument("-beg", type=int, default=None, help="Minimum of preferred time period")
    parser.add_argument("-end", type=int, default=None, help="Maximum of preferred time period")
    args = parser.parse_args()
    return args


def file_opener(file_name, emi=0):
    if emi == 1:
        file = pd.read_csv(file_name, header=0)
    else:
        file = pd.read_csv(file_name, header=2)
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
    return [population, gdp_loc, emissions]


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
    return [population, gdp_loc, emissions]


# Function that cleans columns with country names, changes letters to lower ones and removes all words in brackets
# input: column of relevant data frame
# output: column of data frame but with changed letters to lower ones and removed all words in brackets
def country_cleaner_1(data):
    data = data.apply(lambda x: x.lower())
    return data


def country_cleaner_2(data):
    data = data.apply(lambda x: re.sub(" \(.*?\)", "", x))
    data = data.apply(lambda x: re.sub("republic of ", "", x))

    return data


def data_merger(pop, gdp, em):
    pop_gdp = pd.merge(pop, gdp, how='inner')
    pop_gdp = pop_gdp[['Year', 'Country Name', 'Population', 'Gdp']]
    pop_gdp = pop_gdp[
        pop_gdp['Country Name'].isin(np.intersect1d(em['Country Name'].unique(), pop_gdp['Country Name'].unique()))]
    em = em[em['Country Name'].isin(np.intersect1d(em['Country Name'].unique(), pop_gdp['Country Name'].unique()))]

    data = pd.merge(pop_gdp, em, how='left', on=['Year', 'Country Name'])
    return data


def data_loss(pop, em):
    rat1 = len(list(np.intersect1d(em['Country Name'].unique(), pop['Country Name'].unique())))\
          / len(list(pop['Country Name'].unique()))
    rat2 = len(list(np.intersect1d(em['Country Name'].unique(), pop['Country Name'].unique())))\
          / len(list(em['Country Name'].unique()))
    return [rat1, rat2]


def data_cleaner(pop, gdp, em, bg, end):
    pop = pop.dropna(axis=1, how='all')
    gdp = gdp.dropna(axis=1, how='all')
    em = em.dropna(axis=0, how='all')
    em = em[['Year', 'Country', 'Total', 'Per Capita']]
    pop = pop.drop(columns=['Country Code', 'Indicator Name', 'Indicator Code'])
    gdp = gdp.drop(columns=['Country Code', 'Indicator Name', 'Indicator Code'])
    em.rename(columns={'Country': 'Country Name', 'Total': 'Total emissions', 'Per Capita': 'Emissions per Capita'},
              inplace='True')
    if bg is not None and end is not None:
        pop, gdp, em = years_interval_merger(pop, gdp, em, bg, end)
    else:
        pop, gdp, em = years_merger(pop, gdp, em)
    pop = pop.melt(id_vars='Country Name', var_name='Year', value_name='Population')
    gdp = gdp.melt(id_vars='Country Name', var_name='Year', value_name='Gdp')
    pop.Year = pop.Year.astype('int64')
    gdp.Year = gdp.Year.astype('int64')
    return pop, gdp, em
