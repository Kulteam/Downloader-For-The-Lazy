#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from ast import Pass
import string
from distutils import extension
from distutils.errors import LinkError
from fileinput import filename
from genericpath import isfile
from shutil import which
import sqlite3 as lite
import shutil
import subprocess
import urllib
from urllib import request
from urllib.request import HTTPDefaultErrorHandler, urlopen ,urlretrieve
from urllib.parse import quote, urlparse,urlsplit, unquote
from requests.sessions import session   
import youtube_dl
import logging
import boto3
from botocore.exceptions import ClientError
from ntpath import join
from bs4 import BeautifulSoup
import requests
import re
import random
import time
from requests_toolbelt import MultipartEncoder, MultipartEncoderMonitor
import json
from tqdm import tqdm 
from sys import exit
import sys
import posixpath
import os
import platform
from fsplit.filesplit import Filesplit
import cgi
import hashlib

from pathlib import Path
import libtorrent as torrent
from requests.exceptions import RequestException

#list_links=[]

#file = open("link.txt", "r")

#file_link = file.read()
def get_digest(file_path):
    h = hashlib.sha256()

    with open(file_path, 'rb') as file:
        while True:
            # Reading is buffered, so we can read smaller chunks.
            chunk = file.read(h.block_size)
            if not chunk:
                break
            h.update(chunk)

    return h.hexdigest()


def Get_urls_from_local_file(filename):
    file =open(filename)
    file_link = file.read()
    # findall() has been used 
    # with valid conditions for urls in string
    url = "([\w+]+\:\/\/)?([\w\d-]+\.)*[\w-]+[\.\:]\w+([\/\?\=\&\#.]?[\w-]+)*\/?"
    magnet = "magnet:\?xt=urn:btih:[a-zA-Z0-9]*"
    regex=f"({url}|{magnet})"
    urls = re.findall(regex,file_link)      
    return urls
#[x[0] for x in urls]

def Get_urls_from_string(string):
    url = "([\w+]+\:\/\/)?([\w\d-]+\.)*[\w-]+[\.\:]\w+([\/\?\=\&\#.]?[\w-]+)*\/?"
    magnet = "magnet:\?xt=urn:btih:[a-zA-Z0-9]*"
    regex=f"({magnet}|{url})"
    urls = re.findall(regex,string)      
    return [x[0] for x in urls]
 
def Get_urls_from_remote_file(url):
    file_link = requests.get(url).text
    # with valid conditions for urls in string
    url = "([\w+]+\:\/\/)?([\w\d-]+\.)*[\w-]+[\.\:]\w+([\/\?\=\&\#.]?[\w-]+)*\/?"
    magnet = "magnet:\?xt=urn:btih:[a-zA-Z0-9]*"
    regex=f"({magnet}|{url})"
    urls = re.findall(regex,file_link)      
    return [x[0] for x in urls] 
      


def Get_link_anonfiles(list_link):
     r=re.compile("^https?://anonfiles.com")
     list_link_anonfiles = list(filter(r.match,list_link))
     return list_link_anonfiles
 
def Get_link_bayfiles(list_link):
     r=re.compile("^https?://bayfiles.com")
     list_link_bayfiles = list(filter(r.match,list_link))
     return list_link_bayfiles 

def Get_link_SiaSky(list_link):
     r=re.compile("^https?://siasky.net")
     list_link_siasky = list(filter(r.match,list_link))
     return list_link_siasky

def Get_link_SolidFiles(list_link):
     r=re.compile("^https?:\/\/(www.)*solidfiles.com/v/")
     
     list_link_SolidFiles = list(filter(r.match,list_link))
     return list_link_SolidFiles

def Get_link_mediaFire(list_link):
     regex="^https?://(www.)*mediafire.com/file/"    
     r=re.compile(regex)
     list_link_mediaFire = list(filter(r.match,list_link))
     return list_link_mediaFire
 
def Get_link_torrent(list_link):
     regex="magnet:\?xt=urn:btih:[a-zA-Z0-9]*|https?:\/\/[^\s]+\.torrent"
     r=re.compile(regex)
     list_link_torrent = list(filter(r.match,list_link))
    
     return list_link_torrent
 
def Get_link_onedriver(list_link):
    regex="^https?://1drv.ms(/x/|/v/|/w/|/p/|/t/)|^https?://onedrive.live.com/(\?cid|embed\?|view.aspx|\?authkey)"
    r=re.compile(regex)
    list_link_onedriver = list(filter(r.match,list_link))
    return list_link_onedriver
    
     
 
def Get_link_support_by_youtube_dl(list_link):
     youtube="^https?:\/\/(www.)*youtube.com(\/watch\?|\/channel/|\/feed\/explore|\/channels|\/c\/|\/user\/)|(https?://youtu.be/)"
     pornhub="^https?:\/\/(www.)*pornhub.com(\/model\/|\/view_video|\/video|\/pornstar|\/channels|\/users|\/playlist|\/albums|\/recommended|\/explore)"
     facebook="^https?:\/\/(www.)*facebook.com/(watch|[a-zA-Z0-9]*/videos/)"
     bilibili="^https?:\/\/(www.)*bilibili.com(/video/|/[a-zA-Z0-9]*/play/)"
     google_driver="^https?://drive.google.com/file/"
     regex="|".join([youtube,pornhub,facebook,bilibili,google_driver])
     r=re.compile(regex)
     link_support_by_youtube_dl = list(filter(r.match,list_link))
     return link_support_by_youtube_dl
           

def Download_from_anonfiles(list_link):
    for link in list_link:  
        req = requests.get(link)
        soup = BeautifulSoup(req.text, "html.parser")
        #print(soup.title)
        for url in soup.findAll('a', attrs={'href': re.compile("^https://cdn-")}):
            link_direct = (url.get('href'))
            print("Download file of link: "+link)
            filename=Download_file_from_direct_link(link_direct)
            print("Done download filename: "+filename)
            sleep_time=random.randint(1,5)
            print("Pause until next download for %s s" %sleep_time )
            time.sleep(sleep_time)

def Download_from_bayfiles(list_link):
    for link in list_link:  
        req = requests.get(link)
        soup = BeautifulSoup(req.text, "html.parser")
    
        for url in soup.findAll('a', attrs={'href': re.compile("^https://cdn-")}):
            link_direct = (url.get('href'))
            print("Download file of link: "+link)
            filename=Download_file_from_direct_link(link_direct)
            print("Done download filename: "+filename)
            sleep_time=random.randint(1,5)
            print("Pause until next download for %s s" %sleep_time )
            time.sleep(sleep_time)

def Download_from_SiaSky(list_link):
    for link in list_link:
            print("Download file of link: "+link)
            buffer_size = 1024
# download the body of response by chunk, not immediately
            response = requests.get(link, stream=True)
            file_size = int(response.headers.get("Content-Length", 0))
          # get the default filename
            default_filename = link.split("/")[-1]
            # get the content disposition header
            content_disposition = response.headers.get("Content-Disposition")
            if content_disposition:
                value, params = cgi.parse_header(content_disposition)
            # extract filename from content disposition
                filename = params.get("filename", default_filename)
        
            # parse the header using cgi
            else:
                 filename = default_filename
       
           # if content dispotion is not available, just use default from URL
            progress = tqdm(response.iter_content(buffer_size), f"Downloading {filename}", total=file_size, unit="B", unit_scale=True, unit_divisor=1024)
            with open(filename, "wb") as f:
                 for data in progress.iterable:
                     f.write(data)
                     # update the progress bar manually
                     progress.update(len(data)) 
    return filename
                    

def Download_from_mediaFire(list_link,path_folder="."):
    list_file=[]
    list_path_file=[]
    for link in list_link:  
        req = requests.get(link)
        soup = BeautifulSoup(req.text, "html.parser")
       # print(soup.title)
        for url in soup.findAll('a', attrs={'href': re.compile("^https?://download")}):
            link_direct = (url.get('href'))
            print("Download file of link: "+link)
            filename=Download_file_from_direct_link(link_direct)
            print("Done download filename: "+filename)
            list_file.append(filename)
            sleep_time=random.randint(1,5)
            print("Pause until next download for %s s" %sleep_time )
            time.sleep(sleep_time)   
            
    for file in list_file:
        new_path=path_folder+'/'+file
        print(new_path)
        try:
            Path(file).rename(new_path)
            list_path_file.append(new_path)
        except :
            print("The system cannot find the file specified: "+file+"->"+new_path)
            
                     
    return list_path_file   

def Get_list_files_from_folder(path_folder,subdir=False,extensions=[".*"]):
    #Tham số extensions chứa list các file type để lọc ra các path với file type đc chỉ định
    #Ví dụ extensions=[".mp4",".py",".pdf"]
    if os.path.exists(path_folder)==True:
        if subdir==False:
            files = [f for f in os.listdir(path_folder) if os.path.isfile(f)]
        elif subdir==True:
            files = [os.path.join(path, name) for path, subdirs, files in os.walk(path_folder) for name in files]
        if (extensions==[""]or(extensions==["."])or(extensions==[".*"])):
            return files
        else:
            extensions = [extension.lower() for extension in extensions]
            list_path = [s for s in files if any(xs in s for xs in extensions)]
            return list_path
    print("Something is wrong or Path folder is incorrect")
    return False



def Get_direct_link_SolidFiles(url):
     headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36'
        }
     pageSource = requests.get(url, headers = headers).text
     if 'Page not found | SolidFiles' in pageSource:
         print("Link die: "+url)
         print("Check the URL again manually please.")
         exit(0)
                
     else:
          mainOptions = str(re.search(r'viewerOptions\'\,\ (.*?)\)\;', pageSource).group(1))
          jsonString = json.loads(mainOptions)
          downloadUrl = jsonString["downloadUrl"]
          nodeName = jsonString["nodeName"]
          filetype = jsonString["filetype"]
          return(downloadUrl)

def Download_file_from_MagnetLink(url,path_folder="."):
    session = torrent.session()
    session.listen_on(6881, 6891)
    params = {   
        'save_path': path_folder,
        'storage_mode': torrent.storage_mode_t(2),
       #'paused': False,
       #'auto_managed': True,
       #'duplicate_is_error': True
    
    }
    link = url
    handle = torrent.add_magnet_uri(session, link, params)
    session.start_dht()
    print ('Downloading Metadata...')
    while (not handle.has_metadata()):
        time.sleep(1)
    print ('Got metadata, starting torrent download...')
    while (handle.status().state != torrent.torrent_status.seeding):
        s = handle.status()
        state_str = ['queued', 'checking', 'downloading metadata', \
            'downloading', 'finished', 'seeding', 'allocating']
        print ('%.2f%% Complete (Down: %.1f kb/s Up: %.1f kB/s Peers: %d) %s' % \
            (s.progress * 100, s.download_rate / 1000, s.upload_rate / 1000, \
            s.num_peers, state_str[s.state]))  
        time.sleep(5)      
    print(handle.status().name, 'Complete')
    path=(path_folder+'/'+handle.status().name)
    try:
        list_path_file=Get_list_files_from_folder(path,".mp4")
    except :
        print("Cannot get list files from folder.Something is wrong, please check ! ")
        
    return list_path_file
   

def Download_file_from_TorrentFile(url,path_folder="."):
    
    filetorrent=Download_file_from_direct_link(url)
    ses = torrent.session({'listen_interfaces': '0.0.0.0:6881'})

    info = torrent.torrent_info(filetorrent)
    h = ses.add_torrent({'ti': info, 'save_path': path_folder})
    s = h.status()
    print('starting', s.name)

    while (not s.is_seeding):
        s = h.status()
        print('\r%.2f%% Complete (Down: %.1f kB/s Up: %.1f kB/s Peers: %d) %s' % (
            s.progress * 100, s.download_rate / 1000, s.upload_rate / 1000,
            s.num_peers, s.state), end=' ')
        alerts = ses.pop_alerts()
        for a in alerts:
             if a.category() & torrent.alert.category_t.error_notification:
                  print(a)
           
        sys.stdout.flush()
        time.sleep(1)
    print(h.status().name, 'Complete')
    if os.path.isfile(h.status().name)==True:
        return h.status().name
    elif os.path.isdir(h.status().name)==True:
        path=Get_list_files_from_folder(h.status().name,subdir=True)
        return path

def Get_direct_link_onedriver(list_link):
    new_list=[]  
    for link in list_link:
        if 'http://1drv.ms' in link:
            new_url=urllib.request.urlopen(link)
            new_list.append(new_url.url) 
    for link in list_link:
        if 'https://1drv.ms' in link:
            new_url=urllib.request.urlopen(link)
            new_list.append(new_url.url)             
    
    for link in list_link:
        if re.match(r'^https?://onedrive.live.com/(redir\?|embed\?|view.aspx)', link):
            new_list.append(link)
    return new_list
            

def Download_from_OneDriver(list_link):
    list_link_onedriver=Get_direct_link_onedriver(list_link)
    direct_links = list(map(lambda item: item.replace("redir","download"), list_link_onedriver))
    direct_links = list(map(lambda item: item.replace("view.aspx","download.aspx"), direct_links))
    direct_links = list(map(lambda item: item.replace("embed","download"), direct_links))
    for link in direct_links:
        print("Download file of link: "+link)
        filename=Download_file_from_direct_link(link)
        print("Done download filename: "+filename)
        sleep_time=random.randint(1,5)
        print("Pause until next download for %s s" %sleep_time )
        time.sleep(sleep_time)     
       
def Download_from_SolidFiles(list_link):
    for link in list_link:
        direct_link=Get_direct_link_SolidFiles(link)
        print("Download file of link: "+link)
        filename=Download_file_from_direct_link(direct_link)
        print("Done download filename: "+filename)
        sleep_time=random.randint(1,5)
        print("Pause until next download for %s s" %sleep_time )
        time.sleep(sleep_time)
        
def Download_url_support_by_youtube_dl(list_link):
    try:
        ydl_opts = {}
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
             link=ydl.download(list_link)
             return link
    except youtube_dl.DownloadError:
        print("Youtube-dl only support download videos \n Please manually download or try other way If you want download other type file \n" 
              "Host support by this script: \n-Youtube (Only Video)\n-Facebook (Only Video) \n-BiliBili (Only Video)\n-PornHub (Only Video)\n-AnonFiles\n-BayFiles"
              "\n-mediaFire\n-SolidFiles")   


def Download_from_Torrent(list_link,path_folder="."):
    for link in list_link:
         if 'http' in link :
             try:
                Path_file=Download_file_from_TorrentFile(link,path_folder)
                return Path_file
             except:
                print("Your url: "+link+" is not support \n Please check! ")
              
         elif 'magnet' in link:
             try:
                Path_file= Download_file_from_MagnetLink(link,path_folder)
                return Path_file
             except:
                print("Your url: "+link+" is not support \n Please check! ")
            

def Get_filename_from_url(url):
    try:
        with requests.get(url) as r:
            filename = ''
        if "Content-Disposition" in r.headers.keys():
            filename = re.findall("filename=(.+)", r.headers["Content-Disposition"])[0]
            filename=filename.replace('"', '')
        else:
            urlpath = urlsplit(url).path
            filename = posixpath.basename(unquote(urlpath))
            if (os.path.basename(filename) != filename or
                unquote(posixpath.basename(urlpath)) != filename):
                raise ValueError
            return filename
            
        return filename
    except RequestException as error:
        print(error)
                    

def Upload_to_DooStream(path_file,api_key):
    
    fields = {
    "api_key": api_key,
  
    }
    
    if is_video_file(path_file)==True:
        if os.path.exists(path_file)==True:
            path = Path(path_file) 
            total_size = path.stat().st_size
            filename = path.name
      
            with tqdm(
              desc=filename,
              total=total_size,
              unit="B",
              unit_scale=True,
              unit_divisor=1024,
            ) as bar:
                with open(path_file, "rb") as f:
                   fields["file"] = (path_file, f)
                   e = MultipartEncoder(fields=fields)
                   m = MultipartEncoderMonitor(
                   e, lambda monitor: bar.update(monitor.bytes_read - bar.n)
                   )
                   headers = {"Content-Type": m.content_type}
                   url=('https://doodapi.com/api/upload/server?key='+api_key)
                   response=requests.get(url).text
                   server_upload = json.loads(response)["result"]
                   upload_url=(server_upload+'?'+api_key)
                   response=requests.post(upload_url, data=m, headers=headers)
                   try:
                        return json.loads(response.text)["result"][0]["protected_embed"]
                   except:
                       print("Something wrong \n File error")
    return False

def Upload_to_Wasabi(file_name,bucket,access_key_id,secret_access_key,endpoint_url='https://s3.ap-northeast-1.wasabisys.com',  object_name=None):
    
    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = os.path.basename(file_name)

    # Upload the file
    s3_client = boto3.client('s3',
                 endpoint_url= endpoint_url,
                 aws_access_key_id=access_key_id,
                 aws_secret_access_key=secret_access_key)
    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
       
    except ClientError as e:
        logging.error(e)
        return False
    return True

   
def Uploads_to_DooStream(list_files,api_key):
    list_results=[]
    fields = {
    "api_key": api_key,
  #"field2": value2
    }
    extensions_video_file = ['.mp4','.flv','.h264','.avi','.mkv','.mpeg','.mpg','.mov','.m4v','.3gp','.wmv','.vob']
    list_path_video = [s for s in list_files if any(xs in s for xs in extensions_video_file)]
    for path_video in list_path_video:
        path = Path(path_video)
        total_size = path.stat().st_size
        filename = path.name

        with tqdm(
             desc=filename,
             total=total_size,
             unit="B",
             unit_scale=True,
             unit_divisor=1024,
        ) as bar:
            with open(path_video, "rb") as f:
                fields["file"] = (path_video, f)
                e = MultipartEncoder(fields=fields)
                m = MultipartEncoderMonitor(
                    e, lambda monitor: bar.update(monitor.bytes_read - bar.n)
                )
                headers = {"Content-Type": m.content_type}
                url=('https://doodapi.com/api/upload/server?key='+api_key)
                response=requests.get(url).text
                server_upload = json.loads(response)["result"]
                upload_url=(server_upload+'?'+api_key)
                response=requests.post(upload_url, data=m, headers=headers)
                link_embed=json.loads(response.text)["result"][0]["protected_embed"]
                list_results.append(link_embed)
        
    return list_results
            
def Download_file_from_direct_link(url,path_folder=".",filename=None):
    if filename==None:
        local_filename = Get_filename_from_url(url)
    else:
        local_filename=filename    
        
    # NOTE the stream=True parameter
    
    if path_folder=="." :
      local_filename=path_folder+"/"+local_filename
    else :
        if os.path.isdir(path_folder)==True :
            local_filename= path_folder+"/"+local_filename   
        else :
            print("The specified path not an existing directory: "+path_folder)
            return False
    r = requests.get(url, stream=True)
    total_size_in_bytes= int(r.headers.get('content-length', 0))
    #block_size = 1024 #1 Kibibyte
    progress_bar = tqdm(total=total_size_in_bytes, unit='iB', unit_scale=True)    
    with open(local_filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024): 
            progress_bar.update(len(chunk))
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)
    
    progress_bar.close()  
    if total_size_in_bytes != 0 and progress_bar.n != total_size_in_bytes:
        print("ERROR, something went wrong")
        print("Check the direct link again manually please.")
        return False
    return local_filename


def Get_GeckoDriver(path_dir="./web_driver"):
    if platform.system()=='Windows':
                if os.path.exists(path_dir+"/geckodriver.exe")==True:
                    return path_dir+"/geckodriver.exe"
                else :    
                    os.makedirs(path_dir)
                    if os.path.exists(path_dir)!=True:
                      print("Cannot create folder to download Gecko Driver \n Please check! ") 
                      return False
                url_file_gecko="https://github.com/Kulteam/AutoLazy/blob/main/driver/firefox/win/chromedriver.exe?raw=true"
                filename=Download_file_from_direct_link(url_file_gecko,path_folder=path_dir)
                while get_digest(filename)!="c578a1899bfde2733424ba8b180b76826e62ba354206c322d4986ad854c35cf8":
                    filename=Download_file_from_direct_link(url_file_gecko,path_folder=path_dir)
                cmd="set PATH %PATH%;"+path_dir
                subprocess.run(cmd,shell=True) 
                if shutil.which("geckodriver")!=None:
                       print("Install Gecko Driver for Firefox on your Windows computer is successfully")
                       return filename
                else:
                        print("Somthing wrong while try to install Gecko Driver for Firefox on your Windows computer")   
                        return False    
    
    if platform.system()=='Linux':  
                if os.path.exists(path_dir+"/geckodriver")==True:
                    if os.access(path_dir+"/geckodriver", os.X_OK)!=True:
                        try:
                            path_file=path_dir+"/geckodriver"
                            os.chmod(path_file, 0o777)
                        except:
                            print("Cannot Chmod File \"geckodriver\" \n Please check! ")
                            return False
                    return path_dir+"/geckodriver"
                else :    
                    os.makedirs(path_dir)
                    if os.path.exists(path_dir)!=True:
                        print("Cannot create folder to download Gecko Driver \n Please check! ") 
                        return False
                    url_gecko_file="https://github.com/Kulteam/AutoLazy/blob/main/driver/firefox/linux/geckodriver?raw=true"
                    filename=Download_file_from_direct_link(url_gecko_file,path_folder=path_dir)
                    while get_digest(filename)!="ad3f822b64b91d91b913a26be958bf4aca7adc51c830623b220b689397150115":
                        filename=Download_file_from_direct_link(url_gecko_file,path_folder=path_dir)
                    chmod="chmod +x "+filename      
                    subprocess.run(chmod,shell=True) 
                    set_path="export PATH=$PATH:"+filename
                    subprocess.run(set_path,shell=True)
                    if shutil.which("geckodriver")!=None:
                       print("Install Gecko Driver for Firefox on your Linux computer is successfully")
                       return filename
                    else:
                        print("Somthing wrong while try to install Gecko Driver for Firefox on your Linux computer")  
                        return False  
    else:
        print("Your system computer not support by this Script \n System Support: \n -Windows \n -Linux ")
        return False    

def Get_FFMPEG(path_dir="./ffmpeg"):
    if platform.system()=='Windows':
                if os.path.exists(path_dir+"/ffmpeg.exe")==True:
                    return path_dir+"/ffmpeg.exe"
                else :    
                    os.makedirs(path_dir)
                    if os.path.exists(path_dir)!=True:
                      print("Cannot create folder to download FFMPEG \n Please check! ") 
                      return False
                    urls_file_ffmpeg=(["https://github.com/Kulteam/AutoLazy/blob/main/ffmpeg/win/ffmpeg_1.exe?raw=true","https://github.com/Kulteam/AutoLazy/blob/main/ffmpeg/win/ffmpeg_2.exe?raw=true","https://github.com/Kulteam/AutoLazy/blob/main/ffmpeg/win/ffmpeg_3.exe?raw=true","https://github.com/Kulteam/AutoLazy/blob/main/ffmpeg/win/ffmpeg_4.exe?raw=true","https://github.com/Kulteam/AutoLazy/blob/main/ffmpeg/win/ffmpeg_5.exe?raw=true","https://github.com/Kulteam/AutoLazy/blob/main/ffmpeg/win/ffmpeg_6.exe?raw=true","https://raw.githubusercontent.com/Kulteam/AutoLazy/main/ffmpeg/win/fs_manifest.csv"])
                    for path in urls_file_ffmpeg:
                         Download_file_from_direct_link(path,path_dir)
                    while get_digest(path_dir+"/ffmpeg_1.exe")!="a6bead48a441b829f384405e2fba1f210ccfd5360a5c5486ddfa4018b003f1f8":
                          Download_file_from_direct_link("https://github.com/Kulteam/AutoLazy/blob/main/ffmpeg/win/ffmpeg_1.exe?raw=true",path_dir)
                    while get_digest(path_dir+"/ffmpeg_2.exe")!="4ea4fbb104a2aabab639e31b12e2a9b34f03b384137ecb523854e3fcc68d0cfd":
                        Download_file_from_direct_link("https://github.com/Kulteam/AutoLazy/blob/main/ffmpeg/win/ffmpeg_2.exe?raw=true",path_dir)
                    while get_digest(path_dir+"/ffmpeg_3.exe")!="b07361114ec08a740159594cca0963e84d7b866460a63f4bfd9aa1ce5992aee6":
                        Download_file_from_direct_link("https://github.com/Kulteam/AutoLazy/blob/main/ffmpeg/win/ffmpeg_3.exe?raw=true",path_dir)
                    while get_digest(path_dir+"/ffmpeg_4.exe")!="77f1a97b4d601c60de21dd213a7fd9f8b525ea93d610b9c69c352ff92e3d6c5d":
                        Download_file_from_direct_link("https://github.com/Kulteam/AutoLazy/blob/main/ffmpeg/win/ffmpeg_4.exe?raw=true",path_dir)
                    while get_digest(path_dir+"/ffmpeg_5.exe")!="414847e555d5f8ece255440738e95acefc2ef6f2b4c1d3be2270c299014f7e81":
                        Download_file_from_direct_link("https://github.com/Kulteam/AutoLazy/blob/main/ffmpeg/win/ffmpeg_5.exe?raw=true",path_dir)
                    while get_digest(path_dir+"/fs_manifest.csv")!="4db8a65d5442cd00465c40df1dcefc882f24473999e9961919473a9a89f3f59d":
                        Download_file_from_direct_link("https://github.com/Kulteam/AutoLazy/blob/main/ffmpeg/win/fs_manifest.csv?raw=true",path_dir)  
                    fs = Filesplit()
                    path_ffmpeg=path_dir+"/ffmpeg.exe"
                    fs.merge(path_dir,path_ffmpeg)
                    while get_digest(path_ffmpeg)!="5ee9f2d89fc5115839a1826f0cb06c52c0ce6bcd0ee76f6f822aa54d14670338":
                       print("Hash wrong \n Merge again ! ")
                       fs.merge(path_dir,path_ffmpeg)
                    cmd="set PATH %PATH%;"+path_dir
                    subprocess.run(cmd,shell=True) 
                    if shutil.which("ffmpeg")!=None:
                       print("Install FFMPEG on your Windows computer is successfully")
                       return path_ffmpeg
                    else:
                        print("Somthing wrong while try to install FFMPEG on your Windows computer")   
                        return False
                         
    if  platform.system()=='Linux':
                if os.path.exists(path_dir+"/ffmpeg")==True:
                    return path_dir+"/ffmpeg"
       
                else :
                   os.makedirs(path_dir)
                   if os.path.exists(path_dir)!=True:
                      print("Cannot create folder to download FFMPEG \n Please check! ") 
                      return False 
                   urls_file_ffmpeg=(["https://github.com/Kulteam/AutoLazy/blob/main/ffmpeg/linux/ffmpeg_1?raw=true","https://github.com/Kulteam/AutoLazy/blob/main/ffmpeg/linux/ffmpeg_2?raw=true","https://github.com/Kulteam/AutoLazy/blob/main/ffmpeg/linux/ffmpeg_3?raw=true","https://github.com/Kulteam/AutoLazy/blob/main/ffmpeg/linux/ffmpeg_4?raw=true","https://raw.githubusercontent.com/Kulteam/AutoLazy/main/ffmpeg/linux/fs_manifest.csv"])
                   for path in urls_file_ffmpeg:
                       Download_file_from_direct_link(path,path_dir)
                    
                   while get_digest(path_dir+"/ffmpeg_1")!="beb3b8b3aa72ef1088f8f6be16379177bad2a88801cadf76ed39672394d2198c":
                        Download_file_from_direct_link("https://github.com/Kulteam/AutoLazy/blob/main/ffmpeg/linux/ffmpeg_1?raw=true",path_dir)
                   while get_digest(path_dir+"/ffmpeg_2")!="0bd6504d35c6ab140e04d0e6c657efc0e1cc4ec05222a258a413a090076919d0":
                        Download_file_from_direct_link("https://github.com/Kulteam/AutoLazy/blob/main/ffmpeg/linux/ffmpeg_2?raw=true",path_dir)
                   while get_digest(path_dir+"/ffmpeg_3")!="8a365dbe28680de1c3b41b37fb7f6c1df2a980331638430d9e1a868f3f28b42f":
                        Download_file_from_direct_link("https://github.com/Kulteam/AutoLazy/blob/main/ffmpeg/linux/ffmpeg_3?raw=true",path_dir)
                   while get_digest(path_dir+"/ffmpeg_4")!="ee116f1b63d4d0ccd8aee0811627e5aae3f2bdb66da98854dd19606a411230d9":
                        Download_file_from_direct_link("https://github.com/Kulteam/AutoLazy/blob/main/ffmpeg/linux/ffmpeg_4?raw=true",path_dir)
                   while get_digest(path_dir+"/fs_manifest.csv")!="58627b1b80094a841630c95a8695a5c488421e42b0de4d9d2b9069c21f1f7be3":
                        Download_file_from_direct_link("https://github.com/Kulteam/AutoLazy/blob/main/ffmpeg/win/fs_manifest.csv?raw=true",path_dir)  
                   fs = Filesplit()
                   path_ffmpeg=path_dir+"/ffmpeg"
                   fs.merge(path_dir,path_ffmpeg)
                   while get_digest(path_ffmpeg)!="3ea58083710f63bf920b16c7d5d24ae081e7d731f57a656fed11af0410d4eb48":
                         print("Hash wrong \n Merge again ! ")
                         fs.merge(path_dir,path_ffmpeg)
                   
                   chmod="chmod +x "+path_ffmpeg      
                   subprocess.run(chmod,shell=True) 
                   if os.path.exists(path_ffmpeg)==True:
                       print("Install FFMPEG on your Linux computer is successfully")
                       return path_ffmpeg
                   else:
                        print("Somthing wrong while try to install FFMPEG on your Linux computer")  
                        return False  
    else:
        print("Your system computer not support by this Script \n System Support: \n -Windows \n -Linux ")
        return False

def is_image_file(path_file):
    if os.path.isfile(path_file):
        file_extension = os.path.splitext(path_file)[1]
        if file_extension.lower() in {'.jpg','.png','.gif','.jpeg','.cr2','.tiff','.webp'}:
                return True
        return False
    return False

def is_video_file(path_file):
        if os.path.isfile(path_file):
            file_extension = os.path.splitext(path_file)[1]
            if file_extension.lower() in {'.mp4','.flv','.h264','.avi','.mkv','.mpeg','.mpg','.mov','.m4v','.3gp','.wmv','.vob'}:
                return True
            return False
        return False
def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def is_same_type_file(list_path,extension=None):
    if extension==None:
        extension=Path(list_path[0]).suffix
    else:
        extension=extension
    for path in list_path:
        if Path(path).suffix!=extension:
            return False
    return True

def Join_video(list_path,output="out_",path_ffmpeg="ffmpeg"):
    
    def run_ffmpeg():
        #Tạo tập tin với tên ngẫu nhiên chứa danh sách video file cần nối
        filename=id_generator()+".txt"
        with open(filename,'w+',encoding = 'utf-8') as file:
            for path in list_path:
                path=("file '{}' \n").format(path)
                file.write(path)
        file.close()
        if platform.system()=='Linux':    
            cmd=("'{}' -y -f concat -safe 0 -i '{}' -c copy '{}'").format(path_ffmpeg,filename,output)
        elif platform.system()=='Windows': 
            cmd=("\"{}\" -y -f concat -safe 0 -i \"{}\" -c copy \"{}\"").format(path_ffmpeg,filename,output)  
        else:
            print("You system not support by this script \n System support: \n -Linux -Windows")
            return False
        
        try:
            subprocess.run(cmd,shell=True)
            os.remove(filename)
        except :
            print("Somthing wrong.Please check !")
            return False    
        if os.path.exists(output)==True:
            return os.path.normpath(output)
        return False
   
    list_video=[]
    for path in list_path:
        if is_video_file(path)==True:
            if os.path.exists(path)==True:
                list_video.append(path)
                
               
    if is_same_type_file(list_video)==True:
        list_path=list_video
       
        if len(list_path)==1:
            print("You need 2 or more videos to join")
            return list_path[0]
        elif len(list_path)==None:
              print("No videos to join")  
              return False
    if output=="out_":
        output="out_"+Path(list_path[0]).suffix       
    elif os.path.isfile(output)==True:
         output=output
    elif os.path.isdir(output)==True:
        if os.path.exists(output)!=True:
            try:
                os.makedirs(output)
            except:
                print("Something is wrong while try create path to save output video file ")       
                return False
        output=os.path.join(output,"output"+Path(list_path[0]).suffix)    
    else:
        print("Somthing is wrong \n Output file/Folder is incorrect \n Please check")
        return False

    if path_ffmpeg=="ffmpeg":
        if shutil.which(path_ffmpeg)!=None:
            return run_ffmpeg()
           
        else:
            print("FFMPEG not install on your computer \n Down and install FFMPEG: ")
            path_ffmpeg=Get_FFMPEG()
            if path_ffmpeg!=False:
                return run_ffmpeg() 
            return False             
    else:
            path_ffmpeg=path_ffmpeg
            return run_ffmpeg()

def Add_logo_to_video(path_input_video,path_logo,path_output="out_",option="5:5",path_ffmpeg="ffmpeg"):
    def run_ffmpeg() :
        if platform.system()=='Linux':
            cmd =(("'{}' -y -i '{}' -i '{}' -filter_complex \"overlay={}\" -codec:a copy '{}'").format(path_ffmpeg,path_input_video,path_logo,option,path_output))
        elif platform.system()=='Windows':
            cmd =(("\"{}\" -y -i \"{}\" -i \"{}\" -filter_complex \"overlay={}\" -codec:a copy \"{}\"").format(path_ffmpeg,path_input_video,path_logo,option,path_output))
        else:
            print("You system not support by this script \n System support: \n -Linux -Windows")
            return False

        try:
            subprocess.run(cmd,shell=True)
        except :
            print("Somthing wrong.Please check !")
            return False    

        if os.path.exists(path_output)==True:
            return os.path.normpath(path_output)
                
        return False
    
    #Kiểm tra xem tệp video đầu vào có hợp lệ k
    if is_video_file(path_input_video)==True:
        if os.path.exists(path_input_video)==True:
            path_input_video=path_input_video
    else:
        print("File video not exists or incorrect")
        return False
    
    if is_image_file(path_logo)==True:
        if os.path.exists(path_logo)==True:
            path_logo=path_logo
    else:
        print("File image not exists or incorrect")
        return False
    
    if path_output=="out_":
        path_output=(path_output+Path(path_input_video).name)
    elif os.path.isfile(path_output)==True:
        path_output=path_output
    elif os.path.isdir(path_output)==True:
            if os.path.exists(path_output)==True:
                path_output=os.path.join(path_output,Path(path_input_video).name)
            else:
                os.makedirs(path_output)
                if os.path.exists(path_output)==True:
                   path_output=os.path.join(path_output,Path(path_input_video).name)
                else:
                    print("Cannot create path or folder to save output file")    
                    return False
    
    if path_ffmpeg=="ffmpeg":
        if shutil.which(path_ffmpeg)!=None:
            return run_ffmpeg()
           
        else:
            print("FFMPEG not install on your computer \n Down and install FFMPEG: ")
            path_ffmpeg=Get_FFMPEG()
            if path_ffmpeg!=False:
                return run_ffmpeg() 
            return False             
    else:
            path_ffmpeg=path_ffmpeg
            return run_ffmpeg()

def Add_logo_to_videos(list_path_input_or_folder_video,path_logo,folder_output=".",option="5:5",path_ffmpeg="ffmpeg"):

   
    list_result=[]   
    for path_file_or_folder in list_path_input_or_folder_video:
        if os.path.isdir(path_file_or_folder)==True:
            list_files=[os.path.join(path, name) for path, subdirs, files in os.walk(path_file_or_folder) for name in files]
            print(list_files)
            for path in list_files:
                if is_video_file(path)==True:
                    path=os.path.basename(path)
                    print(path)
                    video_path=(Add_logo_to_video(path,path_logo,path_output=folder_output))
                    list_result.append(video_path)
        else:
             if os.path.isfile(path_file_or_folder)==True:
                  if is_video_file(path_file_or_folder)==True:
                       list_result.append(Add_logo_to_video(path_file_or_folder,path_logo,path_output=folder_output))
           
    return list_result            




def Find_file_torrent_from_url(url):
    try:
       reqs = requests.get(url)
    except :
        return False
    soup = BeautifulSoup(reqs.text, 'html.parser')
    root_url = urlparse(url).scheme + '://' + urlparse(url).hostname
    for link in soup.find_all('a'):
        if link.get('href') is None:
            return False
        if link.get('href').endswith('.torrent')==True:
            if link.get('href').startswith('http')==True:
                return link.get('href')
               
            else:
                 return root_url+link.get('href')
    return False 
           
                
def Find_file_torrent_from_urls(list_url):
    list_urls_file=[]
    for url in list_url:
        torrent_url=Find_file_torrent_from_url(url)
        if torrent_url!=False:
            list_urls_file.append(torrent_url)
    if not list_urls_file:
        return False
    else:
        return list_urls_file      

def Get_basic_info_141JAV(url_141jav_com):
    
    try:
            page = requests.get(url_141jav_com)
            soup = BeautifulSoup(page.content, 'html.parser')
            video_code=soup.find('title').string.replace(" - 141JAV.com - Free JAV Torrents","")
            video_title = soup.find('p', class_="level has-text-grey-dark").string.replace("\n","")
            video_image=soup.find_all(class_="image")[0]['src']
            video_tag=soup.find_all('a',class_="tag is-light")
            video_tags=[]
            for tag in video_tag:
               video_tags.append(tag.string.replace("\n",""))
            actors=soup.find_all('a',class_="panel-block")
            actress=[] 
            for actress_idol in actors:
              actress.append(actress_idol.string.replace("\n",""))
            url_torrent=Find_file_torrent_from_url(url_141jav_com)
            
    except:
        print("Somthing wrong while get infomation from 141jav.com \n Please check again ")
        return False    
    return {"video_title":video_title,"video_code":video_code,"actress":actress,"video_image":video_image,"video_tags":video_tags,"video_torrent_url":url_torrent}

def is_Upload(video_code,sqlite_file):

    path = os.path.normpath(sqlite_file)
    connect = lite.connect(path)
 
    with connect:
        cur = connect.cursor()    
        sql="SELECT EXISTS(SELECT 1 FROM VIDEO_INFO WHERE CODE=\"{}\");".format(video_code)
        cur.execute(sql)
        data = cur.fetchone()
        if data!=(0,):
            return False
        return True

def Get_MediaInfo(path_dir="./MediaInfo"):
    if platform.system()=='Windows':
                if os.path.exists(path_dir+"/MediaInfo.exe")==True:
                    return path_dir+"/MediaInfo.exe"
                else :    
                    os.makedirs(path_dir)
                    if os.path.exists(path_dir)!=True:
                      print("Cannot create folder to download MediaInfo \n Please check! ") 
                      return False
                url_file="https://github.com/Kulteam/AutoLazy/blob/main/mediainfo/win/MediaInfo_CLI_21.09_Windows_i386.zip?raw=true"
                filename=Download_file_from_direct_link(url_file,path_folder=path_dir)
                while get_digest(filename)!="a8341a4b3db85d55d5ee81b0978b3d801eb221a14f15d0487f92fb7f387a446b":
                    filename=Download_file_from_direct_link(url_file,path_folder=path_dir)
                shutil.unpack_archive(filename,path_dir)
                cmd="set PATH %PATH%;"+path_dir
                subprocess.run(cmd,shell=True) 
                if shutil.which("mediainfo")!=None:
                       print("Install  MediaInfo  on your Windows computer is successfully")
                       return os.path.normpath(path_dir+"/mediainfo")
                else:
                        print("Somthing wrong while try to install MediaInfo on your Windows computer")   
                        return False    
    
    if platform.system()=='Linux':  
                if os.path.exists(path_dir+"/mediainfo")==True:
                    if os.access(path_dir+"/mediainfo", os.X_OK)!=True:
                        try:
                            path_file=path_dir+"/mediainfo"
                            os.chmod(path_file, 0o777)
                        except:
                            print("Cannot Chmod File \"mediainfo\" \n Please check! ")
                            return False
                    return os.path.normpath(path_dir+"/mediainfo")
                else :    
                    os.makedirs(path_dir)
                    if os.path.exists(path_dir)!=True:
                        print("Cannot create folder to download MediaInfo \n Please check! ") 
                        return False
                    url_file="https://github.com/Kulteam/AutoLazy/blob/main/mediainfo/linux/MediaInfo_CLI_21.09_Linux_Portal_x64.zip?raw=true"
                    filename=Download_file_from_direct_link(url_file,path_folder=path_dir)
                    while get_digest(filename)!="fdf7d301597fd9bbc0092acc67d5b053485279e9c072e50903357e91ee01804e":
                        filename=Download_file_from_direct_link(url_file,path_folder=path_dir)
                    shutil.unpack_archive(filename,path_dir)
                    #Set path lib on Linux
                    path_lib="LD_LIBRARY_PATH=$LD_LIBRARY_PATH:{}/.libs".format(path_dir)
                    export="export LD_LIBRARY_PATH"
                    subprocess.run(path_lib,shell=True)  
                    subprocess.run(export,shell=True)  
                    chmod="chmod -R +x {}".format(path_dir)      
                    subprocess.run(chmod,shell=True) 
                    #set_path="export PATH=$PATH:{}/mediainfo".format(path_dir)
                    #subprocess.run(set_path,shell=True)
                    if os.path.exists(path_dir+"/mediainfo")==True:
                       print("Install MediaInfo on your Linux computer is successfully")
                       return os.path.normpath(path_dir+"/mediainfo")
                    else:
                        print("Somthing wrong while try to install MediaInfo on your Linux computer")  
                        return False  
    else:
        print("Your system computer not support by this Script \n System Support: \n -Windows \n -Linux ")
        return False    

def Get_video_stream_duration(path_input,path_mediainfo="mediainfo"):
    def run_mediainfo():
        if platform.system()=='Linux':
            cmd="'{}' --Inform=\"Video;%Duration%\" '{}'".format(path_mediainfo,path_input)
        elif platform.system()=='Windows':
            cmd="\"{}\" --Inform=\"Video;%Duration%\" \"{}\"".format(path_mediainfo,path_input) 
        else:
            print("You system not support by this script \n System support: \n -Linux -Windows")
            return False
        try:
           
            result = subprocess.run(cmd,shell=True,stdout=subprocess.PIPE) 
            result=''.join([n for n in str(result.stdout) if n.isdigit()])
            return (int(result)/1000000)
            
        except :
            print("Somthing wrong.Please check ! \n Video cannot read or other problems")
            return False   



    path_input=os.path.normpath(path_input)
    if os.path.exists(path_input)==True:
        if is_video_file(path_input)==True:
            if path_mediainfo=="mediainfo":
                if shutil.which(path_mediainfo)!=None:
                    return run_mediainfo()
                path_mediainfo=Get_MediaInfo()
                return run_mediainfo
            path_mediainfo=path_mediainfo
            return run_mediainfo()
    return False        


def Find_Infomation_AVMovie(av_code):
    page=requests.get("https://www.javlibrary.com/en/vl_searchbyid.php?keyword="+av_code)
    
    






def Get_info_video_141JAV(url):
    if Find_file_torrent_from_url(url)!=False:
        pass


                                                    
print("Get link from links.txt \n Please wait..")

print(Get_MediaInfo())
print(Get_video_stream_duration("./Lỗi Duyên Tại Ý Trời (Ciray Remix) - TVK x Huỳnh Mộng Như _ Họa giọt lệ buồn xót thương thân em.mkv",path_mediainfo="MediaInfo/mediainfo"))
