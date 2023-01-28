import numpy as np
import pandas as pd
import assignment as asn

gdp = asn.file_opener('API_NY.GDP.MKTP.CD_DS2_en_csv_v2_4751562')
pop = asn.file_opener('API_SP.POP.TOTL_DS2_en_csv_v2_4751604')
em = asn.file_opener('co2-fossil-by-nation_zip')

pop = pop.dropna(axis=1, how='all')
gdp = gdp.dropna(axis=1, how='all')
em = em.dropna(axis=0, how='all')

pop, gdp, em = asn.years_merger(pop, gdp, em)

print(em)
print(gdp)