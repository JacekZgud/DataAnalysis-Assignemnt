import numpy as np
import pandas as pd
import assignment as asn

# import data
gdp = asn.file_opener('API_NY.GDP.MKTP.CD_DS2_en_csv_v2_4751562')
pop = asn.file_opener('API_SP.POP.TOTL_DS2_en_csv_v2_4751604')
em = asn.file_opener('co2-fossil-by-nation_zip')

# clean data
pop = pop.dropna(axis=1, how='all')
gdp = gdp.dropna(axis=1, how='all')
em = em.dropna(axis=0, how='all')
em = em[['Year', 'Country', 'Total', 'Per Capita']]
pop = pop.drop(columns=['Country Code', 'Indicator Name', 'Indicator Code'])
gdp = gdp.drop(columns=['Country Code', 'Indicator Name', 'Indicator Code'])

# Provide different year span:
bg = input("Beginning year:")
end = input("End year:")
if len(bg) != 0 and len(end) != 0:
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
print(data.columns)
print(data.groupby(['Country Name', 'Year'])["Emissions per Capita"].sum())

# CO2 emissions per capita

# Gdp per capita for each year top 5

# emissions per capita loss in last 10 years
print(asn.emission_balance(data)[0])
print(asn.emission_balance(data)[1])

