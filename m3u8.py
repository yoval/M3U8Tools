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
PlayPageUrl = 'http://www.yzbang.cc/swr/125969-1-1.html'
# 1.下载.m3u8文件 2.推送至m3u8.exe 3.保存链接
TYPE = 3
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'}
#下载.m3u8文件
def DownM3U8(M3U8_URL,VideoName,PlayName):
    folder = os.path.exists(PlayName)
    if not folder:
        os.makedirs(PlayName)
    time.sleep(1)
    print(VideoName)
    count=1
    while True:
        count+=1
        print('第%s次尝试.m3u8下载文件。'%count)
        try:
            down_res = requests.get(M3U8_URL,headers=headers)
            break
        except:
            time.sleep(30)
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
    requests.post(PostUrl,PostData,headers=headers)
    time.sleep(1)
    
#获取m3u8新链接
def GetNewUrl(OldUrl):
#    print(OldUrl)
    WebUrl = urlparse(OldUrl).scheme +'://'+ urlparse(OldUrl).netloc
    count=1
    while True:
        count+=1
        print('第%s次尝试获取新链接。'%count)
        try:
            M3U8_Res = requests.get(OldUrl,headers=headers,allow_redirects=True)
            break
        except:
            time.sleep(10)
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
    try:
        Pages = re.findall('第(\d+)集',PlayRes.text)
        Pages = list(set(Pages))
        Pages = [int(Page) for Page in Pages]
        Pages = max(Pages)
        print('共检测到%s集'%Pages)
    except:
        Pages=1
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
    PlayRes = requests.get(PlayPageUrl,headers=headers)
    Pages = GetPages(PlayRes)
    Playlinklist = [FrontUrl + SplitCharacter +str(Page+1)+ Suffixes for Page in range(Pages)]
    return Playlinklist

#写入TXT文件
def WriteTXT(PlayName,CurrentName,M3U8_URL):
    with open(PlayName+'.txt','a') as f:
        f.write(CurrentName+','+M3U8_URL+'\n')

#进行最后操作
def Last(TYPE,M3U8_URL,CurrentName,PlayName):
    if TYPE==1:
        DownM3U8(M3U8_URL,CurrentName,PlayName)
    elif TYPE==2:
        Push2m3u8(CurrentName,M3U8_URL)
    elif TYPE==3:
        WriteTXT(PlayName,CurrentName,M3U8_URL)

if 'q49.net' in PlayPageUrl:
    SplitCharacter = '-'
    Playlistlink = GenPlayUrl(PlayPageUrl,SplitCharacter)
    for PlayPageUrl in Playlistlink:
        PlayRes = requests.get(PlayPageUrl,headers=headers)
        PlaySoup = BeautifulSoup(PlayRes.text,'lxml')
        CurrentSoup = PlaySoup.find_all('div',class_='footer clearfix')[0]
        PlayName = CurrentSoup.select('a')[-1]['title']
        CurrentName = re.findall('【 (.*?)】 ',CurrentSoup.text)[0]
        M3U8_URL = re.findall('"url":"(.*?)"',PlayRes.text)[1]
        M3U8_URL = M3U8_URL.replace('\\','')
        Last(TYPE,M3U8_URL,CurrentName,PlayName)

elif 'dianyingim.com' in PlayPageUrl:
    SplitCharacter = '-'
    Playlistlink = GenPlayUrl(PlayPageUrl,SplitCharacter)
    for PlayPageUrl in Playlistlink:
        PlayRes = requests.get(PlayPageUrl,headers=headers)
        PlaySoup = BeautifulSoup(PlayRes.text,'lxml')
        PlayName = PlaySoup.h1.get_text()
        CurrentName = re.findall('<span class="btn-pc page-title">(.*?)</span>',PlayRes.text)[0]
        M3U8_URL = re.findall('"url":"(.*?)",',PlayRes.text)[0]
        M3U8_URL = unquote(M3U8_URL)
        M3U8_URL = GetNewUrl(M3U8_URL)
        Last(TYPE,M3U8_URL,CurrentName,PlayName)
            
elif 'wxtv.net' in PlayPageUrl:
    SplitCharacter = '-'
    Playlistlink = GenPlayUrl(PlayPageUrl,SplitCharacter)
    for PlayPageUrl in Playlistlink:
        PlayRes = requests.get(PlayPageUrl,headers=headers)
        PlaySoup = BeautifulSoup(PlayRes.text,'lxml')
        PlayName = PlaySoup.h3.get_text()
        CurrentName = re.findall('data-part="(.*?)"></span>',PlayRes.text)[0]
        M3U8_URL = re.findall(r'https:\\/\\/[vod2.buycar5.cn丨4.mhbobo.com].*?index.m3u8',PlayRes.text)[0]
        M3U8_URL = M3U8_URL.replace('\\','')
        M3U8_URL = GetNewUrl(M3U8_URL)
        Last(TYPE,M3U8_URL,CurrentName,PlayName)
            
elif 'pilipali.cc' in PlayPageUrl:
    SplitCharacter = '/'
    Playlistlink = GenPlayUrl(PlayPageUrl,SplitCharacter)
    for PlayPageUrl in Playlistlink:
        PlayRes = requests.get(PlayPageUrl,headers=headers)
        PlaySoup = BeautifulSoup(PlayRes.text,'lxml')
        Title = PlaySoup.title.get_text()
        PlayName = Title.split('-')[0]
        CurrentName = re.findall('-(.*?)在线播放',Title)[0]
        M3U8_URL = re.findall('"url":"(.*?)"',PlayRes.text)[1]
        M3U8_URL = GetPass(M3U8_URL)
        M3U8_URL = GetNewUrl(M3U8_URL)
        Last(TYPE,M3U8_URL,CurrentName,PlayName)

elif 'pianku.li' in PlayPageUrl:
    SplitCharacter = '_'
    Playlistlink = GenPlayUrl(PlayPageUrl,SplitCharacter)
    for PlayPageUrl in Playlistlink:
        PlayRes = requests.get(PlayPageUrl,headers=headers)
        PlaySoup = BeautifulSoup(PlayRes.text,'lxml')
        Title = PlaySoup.title.get_text()
        PlayName = Title.split('_')[0]
        CurrentName = re.findall('_(.*?)在线播放',Title)[0]
        M3U8_URL = re.findall("geturl(.*?);",PlayRes.text)[0]
        M3U8_URL = M3U8_URL.split('\'')[1]
        M3U8_URL = GetNewUrl(M3U8_URL)
        Last(TYPE,M3U8_URL,CurrentName,PlayName)

elif 'yunbtv.com' in PlayPageUrl:
    SplitCharacter = '-'
    Playlistlink = GenPlayUrl(PlayPageUrl,SplitCharacter)
    for PlayPageUrl in Playlistlink:
        PlayRes = requests.get(PlayPageUrl,headers=headers)
        PlaySoup = BeautifulSoup(PlayRes.text,'lxml')
        Title = PlaySoup.title.get_text()
        PlayName = Title.split('_')[0]
        CurrentName = Title.split('_')[1]
        M3U8_URL = re.findall('"url":"(.*?)",',PlayRes.text)[1]
        M3U8_URL = M3U8_URL.replace('\\','')
        M3U8_URL = GetNewUrl(M3U8_URL)
        Last(TYPE,M3U8_URL,CurrentName,PlayName)

elif 'agefans.org' in PlayPageUrl:
    BaseUrl = PlayPageUrl.split('#')[0]
    Res = requests.get(PlayPageUrl,headers=headers)
    Soup = BeautifulSoup(Res.text,'lxml')
    PlayName = Soup.title.get_text()
    PlayName = PlayName.split('-')[0]
    PlayName = PlayName.replace(' ','')
    print(PlayName)
    PlaylistlinkSoup = Soup.find_all('ul',class_='row list-unstyled my-gutters-2')[0]
    Playlistlink = PlaylistlinkSoup.find_all('a', href=True)
    Playlistlink = [BaseUrl+Pagelink['href'] for Pagelink in Playlistlink]
    print('共检测到%s集'%len(Playlistlink))
    for PlayUrl in Playlistlink:
        Play_Url = PlayUrl.split('_')
        VidoId = re.findall('watch/(.*?)#',PlayUrl)[0]
        PlayJsonUrl = 'https://agefans.org/myapp/_get_ep_plays?ep=%s&anime_id=%s'%(Play_Url[-1],VidoId)
        PlayJson = requests.get(PlayJsonUrl,headers=headers)
        PlayJson = PlayJson.json()
        VidoName = PlayJson['result'][0]['name']
        if len(VidoName)<3:
            VidoName='第%s集'%VidoName
        for Dic in PlayJson['result']:
            Id = Dic['id']
            VidoApi = 'https://agefans.org/myapp/_get_raw?id=%s'%Id
            ApiRes = requests.get(VidoApi,headers=headers)
            VidoUrl = ApiRes.text
            if not 'http' in VidoUrl:
                VidoUrl = 'https:' + VidoUrl
            if '.m3u8' in VidoUrl:
                pass
            else:
                continue
            try:
                M3U8_URL = GetNewUrl(VidoUrl)
            except:
                print('获取新链接失败，用旧链接。')
            Last(TYPE,M3U8_URL,VidoName,PlayName)
            break

elif 'yzbang.cc' in PlayPageUrl:
    time.sleep(5)
    print('支持播放源是-百度云.m3u8')
    SplitCharacter = '-'
    Playlistlink = GenPlayUrl(PlayPageUrl,SplitCharacter)
    for PlayUrl in Playlistlink:
        Res = requests.get(PlayUrl,headers=headers)
        try:
            M3U8_URL = re.findall('"url":"(.*?)","url_next',Res.text)[0]
        except:
            print('好像集数检测错了，到此为止……')
            break
        M3U8_URL = M3U8_URL.replace('\\','')
        M3U8_URL = GetNewUrl(M3U8_URL)
        CurrentName = re.findall("vod_part='(.*?)'",Res.text)[0]
        PlayName = re.findall("vod_name = '(.*?)'",Res.text)[0]
        Last(TYPE,M3U8_URL,CurrentName,PlayName)

elif 'cechiyy5.com' in PlayPageUrl:
    SplitCharacter = '-'
    Playlistlink = GenPlayUrl(PlayPageUrl,SplitCharacter)
    for PlayUrl in Playlistlink:
        Res = requests.get(PlayUrl,headers=headers)
        PlaySoup = BeautifulSoup(Res.text,'lxml')
        Play_Name = PlaySoup.h2.get_text()
        PlayName = Play_Name.split(' ')[1]
        VidoName = Play_Name.split(' ')[2]
        M3U8_URL = re.findall('"url":"(.*?)","url_next',Res.text)[0]
        M3U8_URL = M3U8_URL.replace('\\','')
        Last(TYPE,M3U8_URL,VidoName,PlayName)
