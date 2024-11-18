from urllib.request import urlopen
from db_connection_mongo import *
from bs4 import BeautifulSoup
import re

def getProfessorDataUsingH2Tag(h2):
    p = h2.find_next_sibling()
    name = h2.text
    title: BeautifulSoup = p.find('strong', string=re.compile('title', re.IGNORECASE)).next.next.replace(':', '').strip()
    office: BeautifulSoup = p.find('strong', string=re.compile('office', re.IGNORECASE)).next.next.replace(':', '').strip()
    phone: BeautifulSoup = p.find('strong', string=re.compile('phone', re.IGNORECASE)).next.next.replace(':', '').strip()
    email: BeautifulSoup = p.find('a', { 'href': re.compile('mailto:') }).get('href').removeprefix('mailto:').strip()
    website: BeautifulSoup = p.find('a', { 'href': re.compile('http') })
    if website:
        website = website.get('href').strip()
    return {
        "name": name,
        "title": title,
        "office": office,
        "phone": phone,
        "email": email,
        "website": website
    }

if __name__ == '__main__':
    db = connectDataBase()
    pages = db["pages"]
    professors = db["professors"]
    professors.drop()

    page = findPage(pages, { "target": True })
    if not page:
        print("No target page found... Run crawler.py to retrieve target page.")
        exit(0)
    
    html = page["html"]
    bs = BeautifulSoup(html, "html.parser")

    professor_data = [getProfessorDataUsingH2Tag(h2) for h2 in bs.find_all("h2") if not h2.get('id')]
    for data in professor_data:
        addProfessor(professors, **data)