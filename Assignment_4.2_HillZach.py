"""
# DSC-540-T301 Assignment 4.2
# Zach Hill
# 24JUN2019
"""

import pandas as pd
#import numpy as np
import fileinput
import tabula
import re
import os

# clear csv file if found
if os.path.exists('.\csvfile.csv'):
    os.remove('.\csvfile.csv')
        
pdf = 'EN-FINAL Table 9.pdf'

with open(pdf, 'rb') as p:
    df_list = tabula.read_pdf(p, pages = "all", multiple_tables = True, pandas_options = {'header': None})

for n, val in enumerate(df_list):
    val[5:].to_csv(r'.\csvfile.csv', index = False, header = False, mode = 'a')
    
csv = '.\csvfile.csv'  
prev_line = ""

# alter csv file, the ugly and slow way.
with fileinput.FileInput(csv, inplace = True) as c:
    for line in c:
        line = (line.replace("\n", "").
              replace("â€“", '-').
              replace(",", " ").
              replace('"'," ").
              replace(" v ", " ").
              replace(" x ", " ").
              replace(" y", "").
              replace("--", "- -").
              replace("--", "- -").
              replace('**', '').
              replace("  ", " "))
        line = re.sub(r'(-)(\d{1,2})', r'\1 \2', line)
        line = re.sub(r'(\d{2})(\d{2})', r'\1 \2', line)
        line = re.sub(r'(\d{2})(\d{2})', r'\1 \2', line)
        line = re.sub(r'(?!100)(\d{2})(\d{1,2})', r'\1 \2', line)
        line = re.sub(r'([A-Za-z])(\s+)([0-9])', r'\1,\3', line)
        line = re.sub(r'([A-Za-z])(\s+)(-)', r'\1,\3', line)
        line = re.sub(r'(\))(\s+)([0-9])', r'\1,\3', line)
        line = re.sub(r'(\))(\s+)(-)', r'\1,\3', line)        
        line = re.sub(r'([0-9])(\s+)([0-9])', r'\1,\3', line)
        line = re.sub(r'([0-9])(\s+)([0-9])', r'\1,\3', line)
        line = re.sub(r'([0-9])(\s+)(-)', r'\1,\3', line)
        line = re.sub(r'(-)(\s+)([0-9])', r'\1,\3', line)
        line = re.sub(r'(-)(\s+)(-)', r'\1,\3', line)
        line = re.sub(r'(-)(\s+)(-)', r'\1,\3', line)
        
        if line.endswith('    '):
            prev_line = line.rstrip('    ')
        elif prev_line != "":
            print(prev_line, line)
            prev_line = ""
        else:
            print(line)
            
headers = [
    "country",
    "child_labor_total", 
    "child_labor_male", 
    "child_labor_female", 
    "child_marriage_by_15", 
    "child_marriage_by_18",
    "birth_registration_pct_2005–2012_total", 
    "mutilation_prevalence_women", 
    "mutilation_prevalence_girls", 
    "mutilation_support_for_practice", 
    "justify_wife_beating_2005–2012_male", 
    "justify_wife_beating_2005–2012_female",
    "violent_discipline_total", 
    "violent_discipline_male",
    "violent_discipline_female"
]

# create dataframe, I find it easier to work with these and they convert to dict easily.          
df = pd.read_csv(csv, names = headers, header = None, encoding = 'utf-8')
df = df.drop([115,116]).reset_index().drop('index', axis = 1)

countries = df.to_dict('index')
            
print(countries)

# establish mysql connection and create table using previously created dataframe
from sqlalchemy import create_engine

engine = create_engine("mysql://student:password1234@localhost/DSC540?charset=utf8")
con = engine.connect()
df.to_sql(name = 'countries', con = con, if_exists = 'replace')

engine.execute("SELECT * FROM countries").fetchall()