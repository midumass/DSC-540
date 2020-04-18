"""
# DSC-540-T301 Assignment 10.3 Final
# Zach Hill
# 10AUG2019
"""

import pandas as pd
import requests

from wowapi import WowApi

WOW_CLIENT_ID = '0ea5646f90b64f508eb6d5a1f627b64c'
WOW_CLIENT_SECRET = 'bQVuNxl88ci41eBP5Nhr01zuO2osE3HY'

api = WowApi(WOW_CLIENT_ID, WOW_CLIENT_SECRET)

# =============================================================================
# Build Dataset of World of Warcraft Auctions
# =============================================================================

# =============================================================================
# This API allows queries to auction data for over 50 realms, each with over 
# 20000 auctions active at any given time. Because auction data is typically
# realm specific (means vary between realms) this wouldn't typically be useful
# but some edge cases may justify doing so. This function will allow you to pull
# auction data from all realms instead of specifying one specific realm
# =============================================================================

# gets list of realms
realms = api.get_realms('us', 'dynamic-us', locale = 'en_US')
realms_list_of_dicts = list(realms.values())[1]

realms_list = []

for realm in realms_list_of_dicts:
    realm_name = realm['name']
    realms_list.append(realm_name)

# =============================================================================
# The API provides a list of auctions on realm through Auction Houses. These can
# be put into a database or analyzed directly to provide historical bid data for
# would-be auctioners. 
# =============================================================================

ah_df = pd.DataFrame()

# creates dataframe containing the URL for the auction data from the specified realm
def RealmAuctionHouse(realm_name):
    auctions = api.get_auctions('us', realm_name)
    
    # Extract from the auctions dict the key:value pair containing the AH data url
    ah_dict = list(auctions.values())[0][0]

    # pull from the URL the json file of current auctions, create json from response
    ah_url = requests.get(list(ah_dict.values())[0])
    ah_json = ah_url.json()

    # Create a dataframe from json file. Number of Auctions limited for time sake
    realm_ah_df = pd.DataFrame(list(ah_json.values())[1])
    return realm_ah_df

# =============================================================================
# Verify all realms have functioning API
# for realm in realms_list:
#     print(realm)
#     try:
#         api.get_auctions('us', realm)
#     except:
#         print(realm, "failed to query")
# =============================================================================


# Add each realm's Auction House information to the auction dataframe
for realm in realms_list:
    try:
        realm_ah = RealmAuctionHouse(realm)
        ah_df = pd.concat([ah_df, realm_ah])
    except:
        print(realm, "did not concat")

# Remove duplicates as cross-server auctions are listed more than once
ah_df.drop_duplicates(subset = 'auc', keep = 'first', inplace = True)

# Remove variables I'm not interested in
ah_df = ah_df.drop(columns = ['bonusLists',
                              'modifiers',
                              'rand',
                              'seed'])

# =============================================================================
# The API provides more than just AH data, it also can provide item information,
# character information, guild information and hundreds of other data. For human
# readability, the item names were pulled using the 'item' field, which is a
# foreign key for the items table, where item data is stored. This transform
# was done prior to merging but discarded as sometimes more item data is needed 
# when making a purchase.
# =============================================================================
# get item name from item API, add to item_name field in df
# item_name_list = []
# 
# for i in range(len(ah_df)):
#     item = ah_df.iloc[i]['item']
#     item_name = api.get_item('us', item)['name']
#     ah_df['item_name'] = item_name
# =============================================================================
# The below pulls item information from the item API, similar to how the auction
# information is retrieved and formatted, and creates an item dataframe. This
# dataframe is merged with the AH dataframe to provide more detailed item 
# information on each item up for auction
# =============================================================================

# lists to be used for cleaning up duplicate items
all_item_list = []
item_list = []
detailed_item_list = []

# Get full list of items from auctions
for item in ah_df['item']:
    all_item_list.append(item)
    
# Create list of unique items from above list
for item in all_item_list:
    if item not in item_list:
        item_list.append(item)
        
# Call item API to get details of each item in unique list (very slow)
for item in item_list:
    try:
        full_item = api.get_item('us', item)
        detailed_item_list.append(full_item)
    except:
        print("item", item, "not found")

# =============================================================================
# Was faster making a list of unique items and querying just the list. Fewer 
# items, but below is simpler code. Number of queries per hour of 36000 would
# prevent this from being run on a busy auction house.
# =============================================================================
# for i in ah_df['item']:
#     item = api.get_item('us', i)
#     item_list.append(item)
# =============================================================================
    
# Create item dataframe and clean up duplicates (shouldn't be any due to above)
item_df = pd.DataFrame(detailed_item_list)
item_df.drop_duplicates(subset = 'id', keep = 'first', inplace = True)

# Remove variables I'm not interested in
item_df = item_df.drop(columns = ['description', 
                                  'icon', 
                                  'isAuctionable', 
                                  'nameDescription',
                                  'nameDescriptionColor'])

# =============================================================================
# With both the auction dataframe and the item dataframe built and duplicates
# removed, merging the two dataframes with pandas is simple. a Left outer join
# pulls the item data for each item in the item column to allow more detailed
# analysis on bids. Over 5000000 observations with 55 variables. Output changes
# every hour as bids are added and removed.
# =============================================================================

# Create merged dataframe using a left outer join based on item ID
ah_item_df = pd.merge(ah_df, 
                      item_df, 
                      how='left', 
                      left_on = 'item', 
                      right_on = 'id')

# Export complete dataset to csv. 
ah_item_df.sample(10000).to_csv(r'.\Assignment_10.3_Final_HillZach.csv')