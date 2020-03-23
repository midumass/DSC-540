"""
# DSC-540-T301 Assignment 7.2
# Zach Hill
# 20JUL2019
"""

import urllib
from urllib.request import urlopen
import requests
from bs4 import BeautifulSoup

# Testing urllib functions
'''11
# urllib2.urlopen has been split in Python3 into urllib.request and urllib.error
google = urlopen('http://google.com')
google = google.read()

print('Web Page:', google[:200])

# quote_plus has been added as a functional of urllib.parse
url = 'http://google.com?q='
url_with_query = url + urllib.parse.quote_plus('python web scraping')

# urllib2.urlopen has been split in Python3 into urllib.request and urllib.error
web_search = urlopen(url_with_query)
web_search = web_search.read()

print('\nWeb Page with Search:', web_search[:200])
'''

# Testing functions of requests
'''
# use requests library to import different parts of page
google = requests.get('http://google.com')

print('\nStatus Code:', google.status_code)
print('\nContent:', google.content[:200])
print('\nHeaders:', google.headers)
print('\nCookies:', google.cookies.items())
'''

# I dont know web programming well enough to troubleshoot both Python 2-3 errors
# and web development errors so I pointed to the wayback machine for a snapshot
# of the site circa the books publishing date.
page = requests.get('https://web.archive.org/web/20140907183235/http://enoughproject.org/take_action')

# added features tag to remove warning
bs = BeautifulSoup(page.content, 'html.parser')
bslxml = BeautifulSoup(page.content, features = "lxml")

# Testing functions of BeautifulSoup
'''
print('\nPage Title:', bs.title)
print('\nAll "a" tags:', bs.find_all('a'))
print('\nAll "p" tags:', bs.find_all('p'))
'''

# It appears the site has changed as globalNavigation is no longer in the header 
# info. There is a navigation-related item named "hamburger-menu" so I scraped using that
# but abandoned the idea when it worked with the wayback machine
header_children = [c for c in bs.head.children]
print('\nHeader Children:', header_children)

navigation_bar = bs.find(id="globalNavigation")

for d in navigation_bar.descendants:
    print('\n', d)

for s in d.previous_siblings:
    print('\n', s)
    
ta_divs = bs.find_all("div", class_="views-row")
print(len(ta_divs))

all_data = []

for ta in ta_divs:
    title = ta.h2
    link = ta.a
    about = ta.find_all('p')
    # print('\nTitle: ',title, '\nLink:', link, '\nAbout:', about)
    
    data_dict = {}
    data_dict['title'] = ta.h2.get_text()
    data_dict['link'] = ta.a.get('href')
    data_dict['about'] = [p.get_text() for p in ta.find_all('p')]
    all_data.append(data_dict)
    
print(all_data)

########################SELENIUM############################

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException,\
    WebDriverException
from time import sleep

# Testing processes
# Switched to Chrome and added chromedriver.exe to local Python script directory
browser = webdriver.Chrome()

# Again had to use wayback machine, errors were thrown when searching css selectors
browser.get('https://web.archive.org/web/20150906101521/https://www.fairphone.com/we-are-fairphone/')

# Window did not maximize but no error was thrown. When running from console,
# however, window maximized. Book has misprint here, method is stated as 
# "maximize_browser" but the code listed is "maximize_window". Upon initial failure
# of maximize I tried the other method but it threw an error.
browser.maximize_window()

content = browser.find_element_by_css_selector('div.content')
print('\n', content.text)

all_bubbles = browser.find_elements_by_css_selector('div.content')

print('\nNumber of Bubbles:', len(all_bubbles))

for bubble in all_bubbles:
    print('\nBubble Content:', bubble.text)
    
iframe = browser.find_element_by_xpath('//iframe')
new_url = iframe.get_attribute('src')
browser.get(new_url)

# Using the wayback machine, sometimes the elements wouldn't appear for some reason,
# I expect that to be lag related. Sometimes it worked just fine.
all_bubbles = browser.find_elements_by_css_selector('div.twine-item-border')

for elem in all_bubbles:
    print('\nElement Text:', elem.text)

# Initial elements testing
'''
all_data = []

for elem in all_bubbles:
    elem_dict = {}
    elem_dict['full_name'] = \
    elem.find_element_by_css_selector('div.fullname').text
    elem_dict['short_name'] = \
    elem.find_element_by_css_selector('div.name').text
    elem_dict['text_content'] = \
    elem.find_element_by_css_selector('div.twine-description').text
    elem_dict['timestamp'] = elem.find_element_by_css_selector('div.when').text
    elem_dict['original_link'] = \
    elem.find_element_by_css_selector('div.when a').get_attribute('href')

    try:
        elem_dict['picture'] = elem.find_element_by_css_selector('div.picture img').get_attribute('src')
    except NoSuchElementException:
        elem_dict['picture'] = None

    all_data.append(elem_dict)
'''

# Further element testing
all_data = []

for elem in all_bubbles:
    elem_dict = {'full_name': None,
                 'short_name': None,
                 'text_content': None,
                 'picture': None,
                 'timestamp': None,
                 'original_link': None,
                 }
    content = elem.find_element_by_css_selector('div.content')
    try:
        elem_dict['full_name'] = \
        content.find_element_by_css_selector('div.fullname').text
    except NoSuchElementException:
        pass
    try:
        elem_dict['short_name'] = \
        content.find_element_by_css_selector('div.name').text
    except NoSuchElementException:
        pass
    try:
        elem_dict['text_content'] = \
        content.find_element_by_css_selector('div.twine-description').text
    except NoSuchElementException:
        pass
    try:
        elem_dict['timestamp'] = elem.find_element_by_css_selector('div.when').text
    except NoSuchElementException:
        pass
    try:
        elem_dict['original_link'] = \
        elem.find_element_by_css_selector('div.when a').get_attribute('href')
    except NoSuchElementException:
        pass
    try:
        elem_dict['picture'] = elem.find_element_by_css_selector('div.picture img').get_attribute('src')
    except NoSuchElementException:
        pass
    
    all_data.append(elem_dict)

   
def find_text_element(html_element, element_css):
    try:
        return html_element.find_element_by_css_selector(element_css).text
    except NoSuchElementException:
        pass
    return None

def find_attr_element(html_element, element_css, attr):
    try:
        return html_element.find_element_by_css_selector(element_css).get_attribute(attr)
    except NoSuchElementException:
        pass
    return None

def get_browser():
    # Switched webdriver to Chrome
    browser = webdriver.Chrome()
    return browser

def main():
    browser = get_browser()
    browser.get('http://apps.twinesocial.com/fairphone')
    
    all_data = []
    browser.implicitly_wait(10)
    try:
        all_bubbles = browser.find_elements_by_css_selector('div.twine-item-border')
    except WebDriverException:
        browser.implicitly_wait(5)
        all_bubbles = browser.find_elements_by_css_selector('div.twine-item-border')
    
    for elem in all_bubbles:
        elem_dict = {}
        content = elem.find_element_by_css_selector('div.content')
        elem_dict['full_name'] = find_text_element(content, 'div.fullname')
        elem_dict['short_name'] = find_attr_element(content, 'div.name', 'innerHTML')
        elem_dict['text_content'] = find_text_element(content, 'div.twine-description')
        elem_dict['timestamp'] = find_attr_element(elem, 'div.when a abbr.timeago', 'title')
        elem_dict['original_link'] = find_attr_element(elem, 'div.when a', 'data-href')
        elem_dict['picture'] = find_attr_element(content, 'div.picture img', 'src')
        
        all_data.append(elem_dict)
    
    browser.quit()
    return all_data

if __name__ == '__main__':
    all_data = main()
    print(all_data)