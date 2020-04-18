"""
# DSC-540-T301 Assignment 5.2
# Zach Hill
# 03JUL2019
"""

'''
Fixing Labels/Headers – (page 155 – 156 Data Wrangling with Python).
    Create a new dictionary for each row to create a new array.

Data Formats Readable (page 164-165 Data Wrangling with Python).
    Using the same dataset as the above example (mn.csv and mn-headers.csv), 
    use the format method to make output human readable.

Date Formatting (page 167-169 Data Wrangling with Python).
    Format the dates to determine when the interview started and ended.

Documentation (page 208-212 Data Wrangling with Python).
    Practice adding documentation to your code following best practices and 
    guidance from your book. You can use previous code from the above examples, 
    or another code example from class.
'''

# from csv import DictReader
from csv import reader
# import urllib2
# import pandas as pd
from datetime import datetime

data_file = './mn.csv'
header_file = './mn_headers.csv'
updated_file = './mn_headers_updated.csv'

'''
# Testing with pandas, had issues with dict format but with time I think this could be corrected

# Wanted to use the url but the response stream caused issues with DictReader
data_url = 'https://raw.githubusercontent.com/jackiekazil/data-wrangling/master/data/unicef/mn.csv'
header_url = 'https://raw.githubusercontent.com/jackiekazil/data-wrangling/master/data/unicef/mn_headers.csv'

data_df = pd.read_csv(data_url, dtype = object)
header_df = pd.read_csv(header_url, dtype = object)

data_dict = data_df.to_dict()
header_dict = header_df.to_dict()
'''

'''
# Using DictReader

# setting 'rb' in open caused problems, left it at default of 'rt' and specified encoding
data_rdr = DictReader(open(data_file, encoding = 'utf8'))
header_rdr = DictReader(open(header_file, encoding = 'utf8'))
data_rows = [d for d in data_rdr]
header_rows = [h for h in header_rdr]

# Verifying first few rows of dictionary
# print(data_rows[:5])
# print(header_rows[:5])
'''

# Using reader
data_rdr = reader(open(data_file, encoding = 'utf8'))
header_rdr = reader(open(updated_file, encoding = 'utf8'))

data_rows = [d for d in data_rdr]
header_rows = [h for h in header_rdr if h[0] in data_rows[0]]

# print(len(data_rows))
# print(len(header_rows))

all_short_headers = [h[0] for h in header_rows]

skip_index = []
# Modified header rows to clear mismatch
final_header_rows = []

for header in data_rows[0]:
    if header not in all_short_headers:
        index = data_rows[0].index(header)
        skip_index.append(index)
    else:
        for head in header_rows:
            if head[0] == header:
                final_header_rows.append(head)
                break

'''
# Verify matches between keys and respective headers 
for data_dict in data_rows:
    for dkey, dval in data_dict.items():
        for header_dict in header_rows:
            for hkey, hval in header_dict.items():
                if dkey == hval:
                    print('match!')
'''

'''    
# Create list of dictionariesusing DictReader method            
new_rows = []

for data_dict in data_rows:
    new_row = {}
    for dkey, dval in data_dict.items():
        for header_dict in header_rows:
            if dkey in header_dict.values():
                new_row[header_dict.get('Label')] = dval
    new_rows.append(new_row)
'''

# Create list of dictionaries using ZIP method    
new_data = []

for row in data_rows[1:]:
    new_row = []
    for i, d in enumerate(row):
        if i not in skip_index:
            new_row.append(d)
    new_data.append(new_row)

zipped_data = []

# zip in Python returns a list, in Python 3 it returns an iterable object. 
# Used list to make it match the book
for drow in new_data:
    zipped_data.append(list(zip(final_header_rows, drow)))

'''
# Double checking header mismatches
data_headers = []

for i, header in enumerate(data_rows[0]):
    if i not in skip_index:
        data_headers.append(header)
        
header_match = list(zip(data_headers, all_short_headers))

print(header_match)
'''

'''
# Human readable output of a single dictionary from DictReader list
for k, v in new_rows[0].items():
    print('Question: ', k, '\nAnswer: ', v)
    
# Human readable output, beware, it lists all items
   
for i in new_rows:
    for k, v in i.items():
        print('Question: ', k, '\nAnswer: ', v)

# Looks like rows 5-14 hold our datetime data
for e, k in enumerate(new_rows[0].items()):
    print(e, k)
'''

# Human readable output using ZIP
for x in zipped_data[0]:
    print('Question: {[1]}\nAnswer: {}'.format(x[0], x[1]))

# find data pertaining to start and end date/time of interview, rows 7-9,13-16
for x in enumerate(zipped_data[0][:20]):
    print(x)
   
# Uses strings and format to create a datetime object through strptime
start_string = '{}/{}/{} {}:{}'.format(zipped_data[0][8][1], zipped_data[0][7][1], zipped_data[0][9][1], zipped_data[0][13][1], zipped_data[0][14][1])
print(start_string)

start_time = datetime.strptime(start_string, '%m/%d/%Y %H:%M')
print(start_time)

# Uses datetime with integers to create datetime object
end_time = datetime(int(zipped_data[0][9][1]), int(zipped_data[0][8][1]), int(zipped_data[0][7][1]), int(zipped_data[0][15][1]), int(zipped_data[0][16][1]))
print(end_time)

duration = end_time - start_time
print(duration)
print(duration.days)
print(duration.total_seconds())

minutes = duration.total_seconds() / 60
print(minutes)

print(end_time.strftime('%m/%d/%Y %H:%M:%S'))
print(start_time.ctime())
print(start_time.strftime('%Y-%m-%dT%H:%M:%S'))