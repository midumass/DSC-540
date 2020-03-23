"""
# DSC-540-T301 Assignment 6.2
# Zach Hill
# 13JUL2019
"""

'''
Importing Data – (Data Wrangling with Python, Page 219-224)
    Create a function to take an empty list, iterate over the columns and create 
        a full list of all the column types for the dataset. Then load into 
        agate table – make sure to clean the data if you get an error. Follow 
        along with the example in the book on the pages listed.

Exploring Table Functions – (Data Wrangling with Python, Page 225-228)
    Which countries have the highest rates of child labor?
    Which countries have the most girls working?
    What is the average percentage of child labor in cities?
    Find a row with more than 50% of rural child labor.
    Rank the worst offenders in terms of child labor percentages by country.
    Calculate the percentage of children not involved in child labor.

Charting with matplotlib – (Data Wrangling with Python, Page 255-258)
    Chart the perceived corruption scores compared to the child labor percentages.
    Chart the perceived corruption scores compared to the child labor percentages 
        using only the worst offenders.
'''

import xlrd
import agate
from xlrd.sheet import ctype_text
import numpy as np

data_file = './unicef_oct_2014.xls'

workbook = xlrd.open_workbook(data_file)

workbook.nsheets
workbook.sheet_names()

# The following commands failed with iPython version 7. Downgrading to version
# 6 corrected the issue.
sheet = workbook.sheets()[0]

sheet.nrows

sheet.row_values(0)

'''
# Used to identify which rows contain titles and which contain country data
for r in range(sheet.nrows):
    print(r, sheet.row(r))
'''   
    
# Changed zip's default iterable object to list to match book output
# book output showed unicode base, Python 3 does this by default so the output
# is slightly different -- it's missing the 'u's
title_rows = list(zip(sheet.row_values(4), sheet.row_values(5)))
# print(title_rows)

titles = [t[0] + ' ' + t[1] for t in title_rows]
# print(titles)
titles = [t.strip() for t in titles]

country_rows = [sheet.row_values(r) for r in range(6, 114)]

text_type = agate.Text()
number_type = agate.Number()
boolean_type = agate.Boolean()
date_type = agate.Date()
example_row = sheet.row(6)

# print(example_row)
# print(example_row[0].ctype)
# print(example_row[0].value)
# print(ctype_text)

types = []

for v in example_row:
    value_type = ctype_text[v.ctype]
    if value_type == 'text':
        types.append(text_type)
    elif value_type == 'number':
        types.append(number_type)
    elif value_type == 'xldate':
        types.append(date_type)
    else:
        types.append(text_type)

def remove_bad_chars(val):
    if val == '-':
        return None
    else:
        return val

cleaned_rows = []

for row in country_rows:
    cleaned_row = [remove_bad_chars(rv) for rv in row]
    cleaned_rows.append(cleaned_row)

def get_new_array(old_array, function_to_clean):
    new_arr = []
    for row in old_array:
        cleaned_row = [function_to_clean(rv) for rv in row]
        new_arr.append(cleaned_row)
    return new_arr
    
cleaned_rows = get_new_array(country_rows, remove_bad_chars)

table = agate.Table(cleaned_rows, titles, types)

most_egregious = table.order_by('Total (%)', reverse = True).limit(10)

'''
most_egregious.print_table(max_columns = 2)
| Countries and areas  | Total (%) | ... |
| -------------------- | --------- | --- |
| Somalia              |      49.0 | ... |
| Cameroon             |      41.7 | ... |
| Zambia               |      40.6 | ... |
| Burkina Faso         |      39.2 | ... |
| Guinea-Bissau        |      38.0 | ... |
| Ghana                |      33.9 | ... |
| Nepal                |      33.9 | ... |
| Peru                 |      33.5 | ... |
| Niger                |      30.5 | ... |
| Central African R... |      28.5 | ... |
'''

most_females = table.order_by('Female', reverse = True).limit(10)

'''
most_females.print_table(max_columns = 5)
| Countries and areas | Total (%) | c | Sex (%) Male | Female | ... |
| ------------------- | --------- | - | ------------ | ------ | --- |
| Cabo Verde          |       6.4 | y |              |        | ... |
| Chile               |       6.6 | y |              |        | ... |
| Ecuador             |       8.6 | y |              |        | ... |
| Somalia             |      49.0 |   |         44.5 |   53.6 | ... |
| Cameroon            |      41.7 |   |         43.1 |   40.2 | ... |
| Zambia              |      40.6 | y |         41.6 |   39.5 | ... |
| Nepal               |      33.9 | y |         30.2 |   37.8 | ... |
| Guinea-Bissau       |      38.0 |   |         39.5 |   36.4 | ... |
| Peru                |      33.5 | y |         30.6 |   36.3 | ... |
| Burkina Faso        |      39.2 |   |         42.3 |   36.0 | ... |
'''

female_data = table.where(lambda r: r['Female'] is not None)
most_females = female_data.order_by('Female', reverse = True).limit(10)

'''
most_females.print_table(max_columns = 5)
| Countries and areas | Total (%) | c | Sex (%) Male | Female | ... |
| ------------------- | --------- | - | ------------ | ------ | --- |
| Somalia             |      49.0 |   |         44.5 |   53.6 | ... |
| Cameroon            |      41.7 |   |         43.1 |   40.2 | ... |
| Zambia              |      40.6 | y |         41.6 |   39.5 | ... |
| Nepal               |      33.9 | y |         30.2 |   37.8 | ... |
| Guinea-Bissau       |      38.0 |   |         39.5 |   36.4 | ... |
| Peru                |      33.5 | y |         30.6 |   36.3 | ... |
| Burkina Faso        |      39.2 |   |         42.3 |   36.0 | ... |
| Ghana               |      33.9 |   |         33.8 |   34.0 | ... |
| Rwanda              |      28.5 |   |         26.7 |   30.4 | ... |
| Niger               |      30.5 |   |         30.8 |   30.1 | ... |
'''

# The below returns some nulls, is corrected with lambda function farther below
# table.aggregate(agate.Mean('Place of residence (%) Urban'))
# Decimal('10.41204819277108433734939759')

has_por = table.where(lambda r: r['Place of residence (%) Urban'] is not None)
has_por.aggregate(agate.Mean('Place of residence (%) Urban'))
# Decimal('10.41204819277108433734939759')

first_match = has_por.find(lambda x: x['Rural'] > 50)
first_match['Countries and areas']
# 'Bolivia (Plurinational State of)'

ranked = table.compute([('Total Child Labor Rank', agate.Rank('Total (%)', reverse=True)), ])

for row in ranked.order_by('Total (%)', reverse=True).limit(20).rows:
    print(row['Total Child Labor Rank'], row['Total (%)'], row['Countries and areas'])
    
'''
1 49.0 Somalia
2 41.7 Cameroon
3 40.6 Zambia
4 39.2 Burkina Faso
5 38.0 Guinea-Bissau
6 33.9 Ghana
6 33.9 Nepal
8 33.5 Peru
9 30.5 Niger
10 28.5 Central African Republic
10 28.5 Rwanda
12 28.3 Guinea
12 28.3 Togo
14 27.8 Equatorial Guinea
15 27.6 Paraguay
16 27.4 Ethiopia
17 26.4 Bolivia (Plurinational State of)
17 26.4 Côte d'Ivoire
19 26.3 Burundi
20 26.1 Chad
'''
    
def reverse_percent(row):
    return 100 - row['Total (%)']

ranked = table.compute([('Children not working (%)',
                             agate.Formula(number_type, reverse_percent)), ])

ranked = ranked.compute([('Total Child Labor Rank',
                              agate.Rank('Children not working (%)')), ])
    
for row in ranked.order_by('Children not working (%)', reverse=True).limit(20).rows:
    print(row['Total Child Labor Rank'], row['Total (%)'], row['Countries and areas'])
    
'''
108 0.7 Trinidad and Tobago
107 0.9 Romania
106 1.4 Belarus
105 1.6 Jordan
104 1.9 Lebanon
103 2.1 Tunisia
102 2.2 Kazakhstan
101 2.4 Ukraine
100 2.9 Bhutan
99 3.3 Jamaica
98 3.4 Portugal
97 3.6 Kyrgyzstan
95 3.9 Armenia
95 3.9 Saint Lucia
94 4.0 Syrian Arab Republic
92 4.1 Costa Rica
92 4.1 Suriname
91 4.2 Timor-Leste
89 4.4 Argentina
89 4.4 Serbia
'''

import matplotlib.pyplot as plt

plt.plot(africa_cpi_cl.columns['CPI 2013 Score'],
         africa_cpi_cl.columns['Total (%)'])

plt.xlabel('CPI Score - 2013')
plt.ylabel('Child Labor Percentage')
plt.title('CPI & Child Labor Correlation')

plt.show()