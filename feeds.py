# Author: Clark Hatch
# Date: Sep. 2016
# Python: 3.x
#
# Description: Send sports feeds to private slack channel

import urllib.request as urllib

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

def espn(url, dict_articles):
    # articleFlag = False
    # titleFlag = False
    # html = getFeed(url)
    # link = ''
    # title = ''
    # print(html)
    # for line in html:
    #     if '<li data-story-id=' in line:
    #         articleFlag = True
    #         continue
    #     elif articleFlag:
    #         print(line)
    #         print('\n')
    #         articleFlag = False

    return dict_articles

if __name__ == '__main__':
    dict_articles = {}
    dict_articles = cbssports('http://cbssports.com', dict_articles)
    dict_articles = espn('http://espn.com', dict_articles)

    for art in dict_articles:
        print(art)
