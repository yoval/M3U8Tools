# -*- coding: utf-8 -*-
"""
Created on Thu May 27 16:10:22 2021

@author: Yue
"""
import requests,re,time,os
from bs4 import BeautifulSoup
from urllib.parse import  unquote,urlparse
from mima import GetPass

#播放链接
PlayPageUrl = 'https://www.yunbtv.com/vodplay/yibuxiaoxinjiandaoai-1-14.html'
# 1.下载.m3u8文件 2.推送至m3u8.exe
TYPE = 1

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
    
#获取m3u8新链接
def GetNewUrl(OldUrl):
#    print(OldUrl)
    WebUrl = urlparse(OldUrl).scheme +'://'+ urlparse(OldUrl).netloc
    M3U8_Res = requests.get(OldUrl)
    M3U8_text = M3U8_Res.text
    M3U8_New = M3U8_text.split('\n')
    for i in M3U8_New:
        if 'm3u8' in i:
            New_M3U8_URL = WebUrl + i
            break
        else:
            New_M3U8_URL=''
    if New_M3U8_URL=='':
        print('.m3u8网址:%s连接失败！尝试瞎猜新链接'%OldUrl)
        New_M3U8_URL = OldUrl.replace('index.m3u8','1000kb/hls/index.m3u8')
        
    return New_M3U8_URL

#生成ReadMe.md文件
def WirteReadMe(PlayName,PlayUrl):
    with open(PlayName+'\\'+'ReadMe.md','w',encoding='utf-8') as f:
        f.write('来源于：'+PlayUrl)

#获取总集数
def GetPages(PlayRes):
    Pages = re.findall('第(\d+)集',PlayRes.text)
    Pages = list(set(Pages))
    Pages = [int(Page) for Page in Pages]
    Pages = max(Pages)
    print('共检测到%s集'%Pages)
    return Pages

#获取播放页面链接列表
def GenPlayUrl(PlayPageUrl,SplitCharacter):
    FrontUrl = PlayPageUrl.rsplit(SplitCharacter,1)[0]
    BackCharacter = PlayPageUrl.rsplit(SplitCharacter,1)[-1]
    Suffixes = BackCharacter.split('.')
    if len(Suffixes)>1:
        Suffixes = '.'+Suffixes[-1]
    else:
        Suffixes = ''
    PlayRes = requests.get(PlayPageUrl)
    Pages = GetPages(PlayRes)
    Playlinklist = [FrontUrl + SplitCharacter +str(Page+1)+ Suffixes for Page in range(Pages)]
    return Playlinklist

if 'q49.net' in PlayPageUrl:
    SplitCharacter = '-'
    Playlistlink = GenPlayUrl(PlayPageUrl,SplitCharacter)
    for PlayPageUrl in Playlistlink:
        PlayRes = requests.get(PlayPageUrl)
        PlaySoup = BeautifulSoup(PlayRes.text,'lxml')
        CurrentSoup = PlaySoup.find_all('div',class_='footer clearfix')[0]
        PlayName = CurrentSoup.select('a')[-1]['title']
        CurrentName = re.findall('【 (.*?)】 ',CurrentSoup.text)[0]
        M3U8_URL = re.findall('"url":"(.*?)"',PlayRes.text)[1]
        M3U8_URL = M3U8_URL.replace('\\','')
        if TYPE==1:
            DownM3U8(M3U8_URL,CurrentName,PlayName)
        else:
            Push2m3u8(CurrentName,M3U8_URL)

elif 'dianyingim.com' in PlayPageUrl:
    SplitCharacter = '-'
    Playlistlink = GenPlayUrl(PlayPageUrl,SplitCharacter)
    for PlayPageUrl in Playlistlink:
        PlayRes = requests.get(PlayPageUrl)
        PlaySoup = BeautifulSoup(PlayRes.text,'lxml')
        PlayName = PlaySoup.h1.get_text()
        CurrentName = re.findall('<span class="btn-pc page-title">(.*?)</span>',PlayRes.text)[0]
        M3U8_URL = re.findall('"url":"(.*?)",',PlayRes.text)[0]
        M3U8_URL = unquote(M3U8_URL)
        M3U8_URL = GetNewUrl(M3U8_URL)
        if TYPE==1:
            DownM3U8(M3U8_URL,CurrentName,PlayName)
        else:
            Push2m3u8(CurrentName,M3U8_URL)
            
elif 'wxtv.net' in PlayPageUrl:
    SplitCharacter = '-'
    Playlistlink = GenPlayUrl(PlayPageUrl,SplitCharacter)
    for PlayPageUrl in Playlistlink:
        PlayRes = requests.get(PlayPageUrl)
        PlaySoup = BeautifulSoup(PlayRes.text,'lxml')
        PlayName = PlaySoup.h3.get_text()
        CurrentName = re.findall('data-part="(.*?)"></span>',PlayRes.text)[0]
        M3U8_URL = re.findall(r'https:\\/\\/[vod2.buycar5.cn丨4.mhbobo.com].*?index.m3u8',PlayRes.text)[0]
        M3U8_URL = M3U8_URL.replace('\\','')
        M3U8_URL = GetNewUrl(M3U8_URL)
        if TYPE==1:
            DownM3U8(M3U8_URL,CurrentName,PlayName)
        else:
            Push2m3u8(CurrentName,M3U8_URL)
            
elif 'pilipali.cc' in PlayPageUrl:
    SplitCharacter = '/'
    Playlistlink = GenPlayUrl(PlayPageUrl,SplitCharacter)
    for PlayPageUrl in Playlistlink:
        PlayRes = requests.get(PlayPageUrl)
        PlaySoup = BeautifulSoup(PlayRes.text,'lxml')
        Title = PlaySoup.title.get_text()
        PlayName = Title.split(' ')[0]
        CurrentName = re.findall('-(.*?)在线播放',Title)[0]
        M3U8_URL = re.findall('"url":"(.*?)"',PlayRes.text)[1]
        M3U8_URL = GetPass(M3U8_URL)
        M3U8_URL = GetNewUrl(M3U8_URL)
        if TYPE==1:
            DownM3U8(M3U8_URL,CurrentName,PlayName)
        else:
            Push2m3u8(CurrentName,M3U8_URL)

elif 'pianku.li' in PlayPageUrl:
    SplitCharacter = '_'
    Playlistlink = GenPlayUrl(PlayPageUrl,SplitCharacter)
    for PlayPageUrl in Playlistlink:
        PlayRes = requests.get(PlayPageUrl)
        PlaySoup = BeautifulSoup(PlayRes.text,'lxml')
        Title = PlaySoup.title.get_text()
        PlayName = Title.split('_')[0]
        CurrentName = re.findall('_(.*?)在线播放',Title)[0]
        M3U8_URL = re.findall("geturl(.*?);",PlayRes.text)[0]
        M3U8_URL = M3U8_URL.split('\'')[1]
        M3U8_URL = GetNewUrl(M3U8_URL)
        if TYPE==1:
            DownM3U8(M3U8_URL,CurrentName,PlayName)
        else:
            Push2m3u8(CurrentName,M3U8_URL)

elif 'yunbtv.com' in PlayPageUrl:
    SplitCharacter = '-'
    Playlistlink = GenPlayUrl(PlayPageUrl,SplitCharacter)
    for PlayPageUrl in Playlistlink:
        PlayRes = requests.get(PlayPageUrl)
        PlaySoup = BeautifulSoup(PlayRes.text,'lxml')
        Title = PlaySoup.title.get_text()
        PlayName = Title.split('_')[0]
        CurrentName = Title.split('_')[1]
        M3U8_URL = re.findall('"url":"(.*?)",',PlayRes.text)[1]
        M3U8_URL = M3U8_URL.replace('\\','')
        M3U8_URL = GetNewUrl(M3U8_URL)
        if TYPE==1:
            DownM3U8(M3U8_URL,CurrentName,PlayName)
        else:
            Push2m3u8(CurrentName,M3U8_URL)



