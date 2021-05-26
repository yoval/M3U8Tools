# -*- coding: utf-8 -*-
"""
Created on Tue May 25 19:12:25 2021

@author: Yue
"""
from mima import GetPass
import requests,re,time,os
from bs4 import BeautifulSoup
from urllib.parse import  unquote

PlayUrl = 'http://www.dianyingim.com/show-190413/'


# 1.下载.m3u8文件 2.推送至m3u8.exe
TYPE = 2

#下载.m3u8文件
def DownM3U8(M3U8_URL,VideoName,PlayName):
    folder = os.path.exists(PlayName)
    if not folder:
        os.makedirs(PlayName)
    time.sleep(1)
    print(VideoName)
    try:
        down_res = requests.get(M3U8_URL)
    except:
        time.sleep(10)
        down_res = requests.get(M3U8_URL)
    with open(PlayName+'\\'+VideoName+'.m3u8',"wb") as f:
        f.write(down_res.content)
        
#生成ReadMe.md文件
def WirteReadMe(PlayName,PlayUrl):
    with open(PlayName+'\\'+'ReadMe.md','w',encoding='utf-8') as f:
        f.write('来源于：'+PlayUrl)
        
#推送至m3u8.exe
def Push2m3u8(VideoName,M3U8_URL):
    print('正在推送%s'%VideoName)
    PostUrl = 'http://127.0.0.1:8787/'
    PostData = {
        'data':VideoName+','+M3U8_URL,
        'type':'2'
        }
    requests.post(PostUrl,PostData)
    time.sleep(1)

if 'q49.net' in PlayUrl:
    PlayRes = requests.get(PlayUrl)
    PlaySoup = BeautifulSoup(PlayRes.text,'lxml')
    PlayName = PlaySoup.h3.get_text()
    print('当前抓取的是：%s'%PlayName)
    PlaylistlinkSoup = PlaySoup.find_all('ul',class_='playlistlink-1 list-15256 clearfix')[0]
    Playlistlink = PlaylistlinkSoup.find_all('a', href=True)
    Playlistlink = ['http://www.q49.net'+Pagelink['href'] for Pagelink in Playlistlink]
    print('共检索到%s集'%len(Playlistlink))
    for url in Playlistlink:
        res = requests.get(url)
        M3U8_URL = re.findall('"url":"(.*?)"',res.text)[1]
        M3U8_URL = M3U8_URL.replace('\\','')
        VideoName = re.findall('style="background:#1f9d79;color:#fff" >(.*?)</a>',res.text)[0]
        if TYPE==1:
            DownM3U8(M3U8_URL,VideoName,PlayName)
        else:
            Push2m3u8(VideoName,M3U8_URL)
        
if 'dianyingim.com' in PlayUrl:
    PlayRes = requests.get(PlayUrl)
    PlaySoup = BeautifulSoup(PlayRes.text,'lxml')
    PlayName = PlaySoup.h1.get_text()
    print('当前抓取的是：%s'%PlayName)
    PlaylistlinkSoup = PlaySoup.find_all('div',class_='module-blocklist scroll-box scroll-box-y')[0]
    Playlistlink = PlaylistlinkSoup.find_all('a', href=True)
    Playlistlink = ['http://www.dianyingim.com'+Pagelink['href'] for Pagelink in Playlistlink]
    print('共检索到%s集'%len(Playlistlink))
    for url in Playlistlink:
        res = requests.get(url)
        M3U8_URL = re.findall('"url":"(.*?)",',res.text)[0]
        M3U8_URL = unquote(M3U8_URL)
        VideoName = re.findall('<span class="btn-pc page-title">(.*?)</span>',res.text)[0]
        if TYPE==1:
            DownM3U8(M3U8_URL,VideoName,PlayName)
        else:
            Push2m3u8(VideoName,M3U8_URL)
        
if 'wxtv.net' in PlayUrl:
    PlayRes = requests.get(PlayUrl)
    PlayRes.encoding='utf-8'
    PlaySoup = BeautifulSoup(PlayRes.text,'lxml')
    PlayName = PlaySoup.h1.get_text()
    print('当前抓取的是：%s'%PlayName)
    PlaylistlinkSoup = PlaySoup.find_all('ul',class_='content_playlist list_scroll clearfix')[0]
    Playlistlink = PlaylistlinkSoup.find_all('a', href=True)
    Playlistlink = ['https://www.wxtv.net'+Pagelink['href'] for Pagelink in Playlistlink]
    print('共检索到%s集'%len(Playlistlink))
    for url in Playlistlink:
        res = requests.get(url)
        res.encoding='utf-8'
        M3U8_URL = re.findall(r'https:\\/\\/[vod2.buycar5.cn丨4.mhbobo.com].*?index.m3u8',res.text)[0]
        M3U8_URL = M3U8_URL.replace('\\','')
        VideoName = re.findall('data-part="(.*?)"></span>',res.text)[0]
        if TYPE==1:
            DownM3U8(M3U8_URL,VideoName,PlayName)
        else:
            Push2m3u8(VideoName,M3U8_URL)
        
if 'pilipali.cc' in PlayUrl:
    PlayRes = requests.get(PlayUrl)
    PlaySoup = BeautifulSoup(PlayRes.text,'lxml')
    PlayName = PlaySoup.find_all('h1',class_='clearfix')[0]
    PlayName = PlayName.get_text()
    print('当前抓取的是：%s'%PlayName)
    PlaylistlinkSoup = PlaySoup.find_all('ul',class_='play_num_list clearfix hide show')[0]
    Playlistlink = PlaylistlinkSoup.find_all('a', href=True)
    Playlistlink = ['http://pilipali.cc'+Pagelink['href'] for Pagelink in Playlistlink]
    for url in Playlistlink:
        res = requests.get(url)
        M3U8_URL = re.findall('"url":"(.*?)"',res.text)[1]
        M3U8_URL = GetPass(M3U8_URL)
        VideoName = re.findall('</h3><p>(.*?)</p></div><div class="fjcon"><div class="fjtop clearfix">',res.text)[0]
        if TYPE==1:
            DownM3U8(M3U8_URL,VideoName,PlayName)
        else:
            Push2m3u8(VideoName,M3U8_URL)
        
if 'pianku.li' in PlayUrl:      
    Url = PlayUrl.split('_')[0]
    PlayRes = requests.get(PlayUrl)
    Pages = re.findall('第(.*?)集',PlayRes.text)
    PlayName = re.findall('<title>(.*?)_第',PlayRes.text)[0]
    Pages = list(set(Pages))
    Pages = [int(Page) for Page in Pages]
    Pages = max(Pages)
    print('共检索到%s集'%Pages)
    for Page in range(Pages):
        P = Page+1
        url = Url + '_%s.html'%P
        res = requests.get(url)
        M3U8_URL = re.findall("geturl(.*?);",res.text)[0]
        M3U8_URL = M3U8_URL.split('\'')[1]
        VideoName = re.findall('class="on">(.*?)</a></li>',res.text)[0]
        if TYPE==1:
            DownM3U8(M3U8_URL,VideoName,PlayName)
        else:
            Push2m3u8(VideoName,M3U8_URL)
        
if 'yunbtv.com' in PlayUrl:
    PlayRes = requests.get(PlayUrl)
    PlaySoup = BeautifulSoup(PlayRes.text,'lxml')
    PlayName = PlaySoup.h2.get_text()
    print('当前抓取的是：%s'%PlayName)
    PlaylistlinkSoup = PlaySoup.find_all('ul',class_='clearfix')[0]
    Playlistlink = PlaylistlinkSoup.find_all('a', href=True)
    Playlistlink = ['https://www.yunbtv.com'+Pagelink['href'] for Pagelink in Playlistlink]
    for url in Playlistlink:
        res = requests.get(url)
        M3U8_URL = re.findall('"url":"(.*?)",',res.text)[1]
        M3U8_URL = M3U8_URL.replace('\\','')
        VideoName = re.findall('<title>(.*?)</title>',res.text)[0]
        VideoName = VideoName.split('_')[1]
        if TYPE==1:
            DownM3U8(M3U8_URL,VideoName,PlayName)
        else:
            Push2m3u8(VideoName,M3U8_URL)

if TYPE==1:
    WirteReadMe(PlayName,PlayUrl)
