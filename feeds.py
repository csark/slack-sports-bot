# Author: Clark Hatch
# Date: Sep. 2016
# Python: 3.x
#
# Description: Send sports feeds to private slack channel

import urllib.request as urllib
import requests

def getFeed(url):
    response = urllib.urlopen(url)
    html = response.read()
    html = html.decode('utf-8').split('\n')
    return html

def cbssports(url, dict_articles):
    articleFlag = False
    titleFlag = False
    html = getFeed(url)
    link = ''
    title = ''
    for line in html:
        if '<li class="article-list-stack-item">' in line:
            articleFlag = True
            continue
        elif titleFlag and articleFlag:
            title = line.replace('  ','')
            title = title.replace('\n','')
            dict_articles[title] = link
            articleFlag = False
            titleFlag = False
        elif articleFlag:
            if '<a ' in line:
                arr = line.split()
                link = url + arr[1].replace('href="','')[:-1]
            if '<h3 ' in line:
                titleFlag = True

    return dict_articles

if __name__ == '__main__':
    dict_articles = {}
    dict_articles = cbssports('http://cbssports.com', dict_articles)
    web_hook = ''

    f = open('db.txt','r')
    output = ''
    lines = []
    for line in f:
        lines.append(line)
    f.close();
    #print(dict_articles)
    for title in dict_articles:
        is_new = True
        title = title.replace('\n','')
        #print("Title is: " + title)
        for line in lines:
            line = line.replace('\n','')
            #print("Line is: " + line)
            if line == title:
                is_new = False
                output += line + '\n'
                print("Status => old. Item is: " + line + '\n')
                break
        if is_new:
            output += title + '\n'
            url     = ''
            text =  'New Post - <' + dict_articles[title] + '|' + title + '>'
            payload = { 'channel': '#sports', 'icon_url': 'http://www.cbssports.com/favicon.ico', 'username': 'cbssports', 'text': text }
            headers = {'Content-Type': 'application/json'}
            res = requests.post(url, json=payload)
            #print(res.text)
            #print("Status => new. Item is: " + title + '\n')

    w = open('db.txt','w+')
    #print('\n')
    #print("Output: " + output)
    w.write(output)
    w.close()
