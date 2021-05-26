# -*- coding: utf-8 -*-
"""
Created on Wed May 26 03:05:23 2021

@author: Yue

pilipali.cc
"""
import re,requests
from bs4 import BeautifulSoup

def GetCode():
    PlayUrl = 'http://pilipali.cc/vod/detail/id/118842.html'
    PlayRes = requests.get(PlayUrl)
    PlaySoup = BeautifulSoup(PlayRes.text,'lxml')
    PlaylistlinkSoup = PlaySoup.find_all('ul',class_='play_num_list clearfix hide show')[0]
    Playlistlink = PlaylistlinkSoup.find_all('a', href=True)
    Playlistlink = ['http://pilipali.cc'+Pagelink['href'] for Pagelink in Playlistlink]
    for url in Playlistlink:
        res = requests.get(url)
        M3U8_URL = re.findall('"url":"(.*?)"',res.text)[1]
        VideoName = re.findall('</h3><p>(.*?)</p></div><div class="fjcon"><div class="fjtop clearfix">',res.text)[0]
        with open('pilipali.txt','a') as f:
            f.write(VideoName+','+M3U8_URL+','+'\n')
            
PassList = []
f = open('pilipali.txt')
lines =f.readlines()
for line in lines:
    line = line.replace('\n','') #删除回车符
    lins = line.split(',')
    url1 = lins[1] #加密地址
    url2 = lins[2] #真实地址
    if url2=='':
        pass
    else:
        urllist = re.findall(r'\w{4}', url1)
        count = 0
        for i in url2:
            a=(urllist[count],i)
            count+=1
            PassList.append(a)
PassList = list(set(PassList))

for tu in PassList:
    print(tu)

