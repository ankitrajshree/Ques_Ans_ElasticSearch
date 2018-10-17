from __future__ import print_function
from urllib.request import urlopen


#import urllib2
import os
import json
from bs4 import BeautifulSoup

base_url = 'https://en.wikibooks.org/wiki/Java_Programming'
# response = urllib2.urlopen(base_url)
baseDir = 'Data'
os.mkdir('Data')
response = urlopen(base_url)
webContent = response.read()
soup = BeautifulSoup(webContent, "html.parser")
div_soup = soup.find('div', attrs={"id": "bodyContent"})
href_links = []
for a in div_soup.find_all('a',href=True):
    if 'Development_stages' in a['href'] or 'Java_Programming' not in a['href'] or 'File:Java_Programming' in a['href']:
        continue
    href_links.append(a['href'].split('/')[-1])
print(href_links)
for link in href_links:
    data = {}
    try:
        final_url = base_url + '/' + link
        response = urlopen(final_url)
        webContent = response.read()
        soup = BeautifulSoup(webContent, "html.parser")
        heading = soup.find('h1', attrs={'id': 'firstHeading'}).text
        print(heading)
        # os.mkdir(heading)
        filename = baseDir+'/'+heading + '.json'
        text = ''
        div_body = soup.find('div', attrs={'id': 'bodyContent'})
        # print div_body
        children = div_body.recursiveChildGenerator()
        # print children
        for child in children:
            if child.name == 'p':
                text += child.text
                #print('Text :', text)
            elif child.name in ['h2', 'h3', 'h4']:
                data['name'] = heading
                data['content'] = text.strip()
                #print(data)

                with open(filename, 'w') as fw:
                    json.dump(data, fw)
                #print child
                heading = child.find('span', attrs={'class': 'mw-headline'}).text
                filename = baseDir+'/'+heading.replace(' ', '_') + '.json'
                #print 'FileName', filename
                text = ''
        data['name'] = heading
        data['content'] = text.encode('ascii', 'ignore')
        with open(filename, 'w') as fw:
            json.dump(data, fw)
    except:
        print('Its okay not a link')