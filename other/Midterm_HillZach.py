"""
# DSC-540-T301 Midterm
# Zach Hill
# 03JUL2019
"""

import pandas as pd
# import saspy
# from sas7bdat import SAS7BDAT


'''
input_file = '/Midterm/cy6_ms_cmb_stu_cog.sas7bdat'

with SAS7BDAT('/Midterm/cy6_ms_cmb_stu_cog.sas7bdat', skip_header = True) as reader:
    for row in reader:
        print(row)

# reader = SAS7BDAT(input_file, skip_header = True)
# df = reader.to_data_frame()

sasds = pd.read_sas(input_file, format = 'SAS7BDAT', chunksize = 1000, iterator = True)

type(sasds)

dfs = []
for chunk in sasds:
    dfs.append(chunk)
''' 


'''
input_file = '/Midterm/INT_COG12_S_DEC03.TXT'

df = pd.read_csv(input_file, sep = '\t', header = None, error_bad_lines = False)
'''

input_file = '/Midterm/SYB61_T04_International Migrants and Refugees.csv'

df = pd.read_csv(input_file, encoding = 'latin-1', header = None)