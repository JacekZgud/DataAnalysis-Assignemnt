import numpy as np
import pandas as pd
import assignment as asn

gdp = asn.file_opener('API_NY.GDP.MKTP.CD_DS2_en_csv_v2_4751562')
pop = asn.file_opener('API_SP.POP.TOTL_DS2_en_csv_v2_4751604')
em = asn.file_opener('co2-fossil-by-nation_zip')

pop = pop.dropna(axis=1, how='all')
gdp = gdp.dropna(axis=1, how='all')
em = em.dropna(axis=0, how='all')

bg = input("Begining date:")
end = input("End date:")
if len(bg) != 0 and len(end) != 0:
    pop, gdp, em = asn.years_interval_merger(pop, gdp, em, bg, end)
else:
    pop, gdp, em = asn.years_merger(pop, gdp, em)

print(pop)
# print(pop['Country Name'])


