import numpy as np
import pandas as pd
import functions as asn


gdp = asn.pars().gdp
pop = asn.pars().pop
em = asn.pars().em


# import data
gdp = asn.file_opener(gdp)
pop = asn.file_opener(pop)
em = asn.file_opener(em, 1)
print(em)

# clean data
pop = pop.dropna(axis=1, how='all')
gdp = gdp.dropna(axis=1, how='all')
em = em.dropna(axis=0, how='all')
print(pop)
em = em[['Year', 'Country', 'Total', 'Per Capita']]
pop = pop.drop(columns=['Country Code', 'Indicator Name', 'Indicator Code'])
gdp = gdp.drop(columns=['Country Code', 'Indicator Name', 'Indicator Code'])

# Provide different year span:
bg = asn.pars().beginning
end = asn.pars().end


if bg is not None and end is not None:
    pop, gdp, em = asn.years_interval_merger(pop, gdp, em, bg, end)
else:
    pop, gdp, em = asn.years_merger(pop, gdp, em)

# Clean Country names
pop['Country Name'] = asn.country_cleaner(pop['Country Name'])
gdp['Country Name'] = asn.country_cleaner(gdp['Country Name'])
em.Country = asn.country_cleaner(em.Country)


#  Adjust and merge gdp and pop
pop = pop.melt(id_vars='Country Name', var_name='Year', value_name='Population')
gdp = gdp.melt(id_vars='Country Name', var_name='Year', value_name='Gdp')
pop_gdp = pd.merge(pop, gdp, how='inner')
pop_gdp = pop_gdp[['Year', 'Country Name', 'Population', 'Gdp']]

pop_gdp = pop_gdp[pop_gdp['Country Name'].isin(np.intersect1d(em.Country.unique(), pop_gdp['Country Name'].unique()))]
em = em[em.Country.isin(np.intersect1d(em.Country.unique(), pop_gdp['Country Name'].unique()))]
em.rename(columns={'Country': 'Country Name', 'Total': 'Total emissions', 'Per Capita': 'Emissions per Capita'},
          inplace='True')
pop_gdp.Year = pop_gdp.Year.astype('int64')
# merge pop_gdp and emissions
data = pd.merge(pop_gdp, em, how='left', on=['Year', 'Country Name'])
data['Emissions per Capita'] = data['Total emissions']/data['Population']
data['Gdp per Capita'] = data['Gdp']/data['Population']
print(data.columns)

# CO2 emissions per capita
cords = data.groupby(["Year"])["Emissions per Capita"].nlargest().index.get_level_values(1).tolist()
emissions_table = data.iloc[cords, [0, 1, 5, 4]].reset_index(drop=True)
print(emissions_table)

# Gdp per capita for each year top 5
cords = data.groupby(["Year"])["Gdp per Capita"].nlargest().index.get_level_values(1).tolist()
emissions_table = data.iloc[cords, [0, 1, 3, -1]].reset_index(drop=True)
print(emissions_table)


# emissions per capita loss in last 10 years
print('Top 5 emissions gained: ')
print(asn.emission_balance(data)[0])
print('Top 5 emissions reduced: ')
print(asn.emission_balance(data)[1])
