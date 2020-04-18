# -*- coding: utf-8 -*-
"""
# DSC-540-T301 Assignment 2.2
# Zach Hill
# 13JUN2019
"""

'''
For all assignments I will be using Python 3. My first choice of editor is 
Notepad++ due to my background in scripting in vi but I will be making use of
Jupyter, Spyder and PyCharm to find which environment I prefer. All have their
advantages and disadvantages so far and I have yet to find a clear winner. 
The only reason I'm not staying with Notepadd++ is the lack of console.
'''

base_str = 'This string will be manipulated in this exercise   '
xi = 3
yi = 2
xd = 3.5
yd = 2.5

# Change case in a string
str_lower = base_str.lower()
str_upper = base_str.upper()
str_swap = base_str.swapcase()

print(str_lower)
print(str_upper)
print(str_swap)

# Strip space off the end of a string
str_strip = base_str.rstrip()
print('The original is', len(base_str), 'characters long')
print('The stripped string is', len(str_strip), 'characters long')

# Split a string
str_split = base_str.split()
print(str_split)

# Add and Subtract integers and decimals
print(xi + yi)
print(xi - yi)
print(xd + yd)
print(xd - yd)

# Create a list
str_list = base_str.split()
print(str_list)

# Add to the list
str_list.append('many')
str_list.append('times')
print(str_list)

# Subtract from the list
str_list.remove('times')
print(str_list)

# Remove the last item from the list
str_list.remove(str_list[len(str_list)-1])
print(str_list)

# Re-order the list
str_list.sort()
print(str_list)

# Sort the list
str_list.sort(reverse = True)
print(str_list)

# Create a dictionary
str_dict = dict(enumerate(str_list))
print(str_dict)

# Add a key-value pair to the dictionary
str_dict.update({8 : 'added'})
print(str_dict)

# Set a new value to corresponding key in dictionary
str_dict.update({8 : 'replaced'})
print(str_dict)

# Look up a new value by the key in dictionary
print(str_dict[8])