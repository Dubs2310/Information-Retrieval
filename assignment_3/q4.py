from urllib.request import urlopen
from bs4 import BeautifulSoup
import re

html = open('q4.html', 'r')
bs = BeautifulSoup(html.read(), 'html.parser')

print(f'4a. {bs.title.text}')
print(f'4b. {bs.ol.li.find_next_sibling().text}')
print(f'4c. {bs.tr.find_all('td')}')
print(f'4d. {[i.text for i in bs.find_all('h2', string=re.compile('tutorial', re.IGNORECASE))]}')
print(f'4e. {[i.text for i in bs.find_all(string=re.compile('html', re.IGNORECASE))]}')
print(f'4f. {[i.text for i in bs.tr.find_next_sibling().find_all('td')]}')
print(f'4g. {bs.find_all('img')}')