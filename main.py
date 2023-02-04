import assignment.d_preparation as prep
import assignment.d_analysis as an
import numpy as np

# import data from terminal
gdp = prep.pars().gdp
pop = prep.pars().pop
em = prep.pars().em

# Interpretation of files as dataframes
gdp = prep.file_opener(gdp)
pop = prep.file_opener(pop)
em = prep.file_opener(em, 1)

# Provide different year span:
bg = prep.pars().beg
end = prep.pars().end

# capital to small letters in country columns
pop['Country Name'] = prep.country_cleaner_1(pop['Country Name'])
gdp['Country Name'] = prep.country_cleaner_1(gdp['Country Name'])
em.Country = prep.country_cleaner_1(em.Country)

pop, gdp, em = prep.data_cleaner(pop, gdp, em, bg, end)


# how much data is lost

print(f"{prep.data_loss(pop, em)}")


pop['Country Name'] = prep.country_cleaner_2(pop['Country Name'])
gdp['Country Name'] = prep.country_cleaner_2(gdp['Country Name'])
em['Country Name'] = prep.country_cleaner_2(em['Country Name'])

print(f"{prep.data_loss(pop, em)}")

print(em['Country Name'].unique())
print(pop['Country Name'].unique())

data = prep.data_merger(gdp, pop, em)
data['Emissions per Capita'] = data['Total emissions'] / data['Population']
data['Gdp per Capita'] = data['Gdp'] / data['Population']

# CO2 emissions per capita
print(' Top 5 C02 emitters per capita per year \n ' f'{an.emissions_top(data)}')

# Gdp per capita for each year top 5
print(' Top 5 C02 emitters per capita per year \n ' f'{an.gdp_top(data)}')


# emissions per capita loss in last 10 years
print('Top 5 emissions per capita risen in last 10 years: ')
print(an.emission_balance(data)[0])
print('Top 5 emissions per capita reduced in last 10 years: ')
print(an.emission_balance(data)[1])
