"""
# DSC-540-T301 Assignment 9.2 - Part 2
# Zach Hill
# 03AUG2019
"""

import xlrd
from xlrd.sheet import ctype_text
import agate

cl_workbook = xlrd.open_workbook('./unicef_oct_2014.xls')
cl_sheet = cl_workbook.sheets()[0]
cpi_workbook = xlrd.open_workbook('./corruption_perception_index.xls')
cpi_sheet = cpi_workbook.sheets()[0]

def get_types(example_row):
    types = []
    for v in example_row:
        value_type = ctype_text[v.ctype]
        if value_type == 'text':
            types.append(agate.Text)
        elif value_type == 'number':
            types.append(agate.Number)
        elif value_type == 'xldate':
            types.append(agate.Date)
        else:
            types.append(agate.Text)
    return types

def get_table(new_arr, types, titles):
    try:
        table = agate.Table(new_arr, titles, types)
        return table
    except Exception as e:
        print(e)
        
def reverse_percent(row):
    return 100 - row['Total (%)']

def remove_bad_chars(val):
    if val == '-':
        return None
    else:
        return val

def get_new_array(old_array, function_to_clean):
    new_arr = []
    for row in old_array:
        cleaned_row = [function_to_clean(rv) for rv in row]
        new_arr.append(cleaned_row)
    return new_arr


sheet = cl_workbook.sheets()[0]

sheet.nrows

sheet.row_values(0)

# Changed zip's default iterable object to list to match book output
# book output showed unicode base, Python 3 does this by default so the output
# is slightly different -- it's missing the 'u's
title_rows = list(zip(sheet.row_values(4), sheet.row_values(5)))
# print(title_rows)

titles = [t[0] + ' ' + t[1] for t in title_rows]
# print(titles)
titles = [t.strip() for t in titles]

country_rows = [sheet.row_values(r) for r in range(6, 114)]

cleaned_rows = []

for row in country_rows:
    cleaned_row = [remove_bad_chars(rv) for rv in row]
    cleaned_rows.append(cleaned_row)
  
cleaned_rows = get_new_array(country_rows, remove_bad_chars)

types = []

table = agate.Table(cleaned_rows, titles, types)

most_egregious = table.order_by('Total (%)', reverse = True).limit(10)

most_females = table.order_by('Female', reverse = True).limit(10)

female_data = table.where(lambda r: r['Female'] is not None)
most_females = female_data.order_by('Female', reverse = True).limit(10)

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

ranked = table.compute([('Children not working (%)',
                             agate.Formula(agate.Number, reverse_percent)), ])

ranked = ranked.compute([('Total Child Labor Rank',
                              agate.Rank('Children not working (%)')), ])
    
for row in ranked.order_by('Children not working (%)', reverse=True).limit(20).rows:
    print(row['Total Child Labor Rank'], row['Total (%)'], row['Countries and areas'])

for r in range(cpi_sheet.nrows):
    print(r, cpi_sheet.row_values(r))

cpi_title_rows = zip(cpi_sheet.row_values(1), cpi_sheet.row_values(2))
cpi_titles = [t[0] + ' ' + t[1] for t in cpi_title_rows]
cpi_titles = [t.strip() for t in cpi_titles]
cpi_titles[0] = cpi_titles[0] + ' Duplicate'

cpi_rows = [cpi_sheet.row_values(r) for r in range(3, cpi_sheet.nrows)]

cpi_types = get_types(cpi_sheet.row(3))

cpi_table = get_table(cpi_rows, cpi_types, cpi_titles)

cpi_and_cl = cpi_table.join(ranked, 'Country / Territory',
                            'Countries and areas', inner=True)

cpi_and_cl.column_names

for r in cpi_and_cl.order_by('CPI 2013 Score').limit(10).rows:
    print('{}: {} - {}%'.format(r['Country / Territory'],
          r['CPI 2013 Score'], r['Total (%)']))