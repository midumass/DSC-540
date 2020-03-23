"""
# DSC-540-T301 Assignment 3.2
# Zach Hill
# 17JUN2019
"""

import pandas as pd
import urllib.request
from xml.etree import ElementTree as ET
import numpy as np

'''
Using Python, import the CSV file provided under Chapter 3 in the GitHub 
repository using the csv library. Put the data in lists and print each record 
on its own dictionary row (Hint: Page 51-52 of Data Wrangling with Python)
'''

csv_url = 'https://raw.githubusercontent.com/jackiekazil/data-wrangling/master/data/chp3/data-text.csv'
csv_df = pd.read_csv(csv_url, sep=',')

# Double checking data as dataframe
print(csv_df.head(5))

# Printing list of dictionaries
csv_list = csv_df.to_dict('records')
print(csv_list[0:5])

'''
Using Python, import the JSON file provided in the GitHub repository under 
Chapter 3. Print each record on its own dictionary row (Hint: page 53-54 of 
Data Wrangling with Python).
'''

json_url = 'https://raw.githubusercontent.com/jackiekazil/data-wrangling/master/data/chp3/data-text.json'
json_df = pd.read_json(json_url)

# Double checking data as dataframe
print(json_df.head(5))

# Printing list of dictionaries
json_list = json_df.to_dict('records')
print(json_list[0:5])

'''
Using Python, import the XML file provided in the GitHub repository under 
Chapter 3. Print each record in its own dictionary row (Hint: page 64 of Data 
Wrangling with Python).
'''

xml_url = 'https://raw.githubusercontent.com/jackiekazil/data-wrangling/master/data/chp3/data-text.xml'
urllib.request.urlretrieve(xml_url, './data-text.xml')

xml_tree = ET.parse('data-text.xml')
xml_root = xml_tree.getroot()
xml_data = xml_root.find('Data')

xml_list = []

for observation in xml_data:
    record = {}
    for item in observation:
        lookup_key = list(item.attrib.keys())[0]
        if lookup_key == 'Numeric':
            rec_key = 'NUMERIC'
            rec_value = item.attrib['Numeric']
        else:
            rec_key = item.attrib[lookup_key]
            rec_value = item.attrib['Code']
        record[rec_key] = rec_value
    xml_list.append(record)

# Double checking data as dataframe
xml_df = pd.DataFrame(xml_list)
print(xml_df.head(5))
     
# Printing list of dictionaries
print(xml_list[0:5])

'''
Using Python, import the Excel file provided in the GitHub repository under 
Chapter 4. Print each record in its own dictionary row. (Hint: page 85-88 of 
Data Wrangling with Python).
'''

excel_url = 'https://raw.githubusercontent.com/jackiekazil/data-wrangling/master/data/chp4/SOWC%202014%20Stat%20Tables_Table%209.xlsx'
excel_df = pd.read_excel(excel_url, sheet_name = 1, index_col = None)
excel_df = excel_df.iloc[13:]
excel_df['Index'] = np.arange(len(excel_df))
excel_df.set_index('Index', inplace = True)

# Double checking data as dataframe
print(excel_df.head(5))

# Printing list of dictionaries
excel_list = excel_df.to_dict('records')
print(excel_list[0:5])
