"""
# DSC-540-T301 Midterm
# Zach Hill
# 13JUL2019
"""

import pandas as pd
import numpy as np

df = pd.read_sas('./cy6_ms_cmb_stu_flt.sas7bdat')

# Import compendia files 
hdfcog = pd.read_excel('./pisa_cog_overall_flit_compendium.xlsx')
hdfbq = pd.read_excel('./pisa_bq_overall_flt_compendium.xlsx')
hdfict = pd.read_excel('./pisa_bq_flit_ict_compendium.xlsx')
hdfpaq = pd.read_excel('./pisa_bq_flit_paq_compendium.xlsx')
hdfsch = pd.read_excel('./pisa_bq_flit_sch_compendium.xlsx')
hdfstu = pd.read_excel('./pisa_bq_flit_stu_compendium.xlsx')
hdfflt = pd.read_excel('./pisa_bq_flit_flt_compendium.xlsx')
hdfec = pd.read_excel('./pisa_bq_flit_ec_compendium.xlsx')

# Import Codebook files
cdf = pd.read_excel('./Codebook_CMB.xlsx')
cdf.dropna(subset = ['NAME', 'VARLABEL'], inplace = True)
cdf.reset_index(inplace = True)
cdf.drop('index', 1, inplace = True)
# cdfh = cdf[['NAME','VARLABEL']]
# cdfh.dropna(inplace = True)

# Rename headers of excel for easier reference
def comp_rename(header_file):
    header_file.rename(columns = {'Unnamed: 0':'code',
                      'Table of Contents':'question'}, 
                        inplace = True)

# Changes headers in dataset to match headers from compendium dictionary
def header_rename(dict_file):
    for key, value in dict_file.items():
        if key in df.columns:
            print(key, 'MATCHES! changing header')
            df.rename(columns={key:value}, inplace = True)
        else:
            print(key, 'had no match')

for i, j in cdf.iterrows():
    name = cdf.iloc[i,0]
    varlabel = cdf.iloc[i,1]
    
    if name in df.columns:
        print(name, 'MATCHES! changing header')
        df.rename(columns={name:varlabel}, inplace = True)

         
comp_list = [hdfcog, hdfbq, hdfstu, hdfsch, hdfpaq, hdfict, hdfflt, hdfec]

for comp_file in comp_list:
    comp_rename(comp_file)

# Create dictionaries to modify dataset headers
hdfcog_dict = pd.Series(hdfcog.question.values, index = hdfcog.code).to_dict()
hdfbq_dict = pd.Series(hdfbq.question.values, index = hdfbq.code).to_dict()
hdfstu_dict = pd.Series(hdfstu.question.values, index = hdfstu.code).to_dict()
hdfsch_dict = pd.Series(hdfsch.question.values, index = hdfsch.code).to_dict()
hdfpaq_dict = pd.Series(hdfpaq.question.values, index = hdfpaq.code).to_dict()
hdfict_dict = pd.Series(hdfict.question.values, index = hdfict.code).to_dict()
hdfflt_dict = pd.Series(hdfflt.question.values, index = hdfflt.code).to_dict()
hdfec_dict = pd.Series(hdfec.question.values, index = hdfec.code).to_dict()

# small variables for testing
'''
df_list = df.columns.to_numpy()
codes = ['DF203Q01C','DF004Q03C','CF095Q02S']
'''

# verifying match found by list
'''
if codes in df_list:
    print('match!')
'''

# Verifying code in column name
'''
for codes in df.columns:
    if code == codes:
        print('match!')
    else:
        print('not match')
'''

# Verify all headers in questions list match headers in dataset
'''
for item in hdf_code_list:
    if item in df.columns:
        print(True)
    else:
        print(False)
'''

# Verify keys are in df.columns
'''
for key, value in hdfcog_dict.items():
    if key in df.columns:
        df.rename(columns={key:value}, inplace = True)
    else:
        print('none')
'''

# List of dicts to rename headers
dict_list = [hdfcog_dict, 
             hdfbq_dict, 
             hdfstu_dict, 
             hdfsch_dict, 
             hdfpaq_dict, 
             hdfict_dict, 
             hdfflt_dict, 
             hdfec_dict]
   
for dicts in dict_list:
    header_rename(dicts)
    
# Removes duplicates
df.drop_duplicates(inplace = True)

# Plots for outliers and bad datam example points from Finance literacy
import seaborn as sns

sns.boxplot(x=df['PV1FLIT'])
sns.distplot(df['PV1FLIT'])
