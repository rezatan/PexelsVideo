import re
import requests
import pandas as pd
from requests.structures import CaseInsensitiveDict
import os
import json

def getFilename_fromCd(cd):
    """
    Get filename from content-disposition
    """
    if not cd:
        return None
    fname = re.findall('filename=(.+)', cd)
    if len(fname) == 0:
        return None
    return fname[0]

def getCurl(q, p) :
    headers = CaseInsensitiveDict()
    #enter your authorization key from pexels here
    headers['Authorization'] = ''
    link_js = 'https://api.pexels.com/videos/search?query='+ q + '&per_page=80' + '&page=' + p
    response = requests.get(link_js, headers=headers)
    return json.loads(response.content)
def download(links) :
    i=0
    for link in links :
        i+=1
        url = link[:link.find("video/")]
        a= re.search('\d{% s}'% 7, link)
        id = (a.group(0) if a else '')
        url = url + "video/" + id + "/download"
        r = requests.get(url, allow_redirects=True)
        filename = id+'.mp4'
        #File path video save
        open(r'D:/Video/Pexels/'+filename, 'wb').write(r.content)
        print ("Download ",i," Complete", filename)
        print("\n")

x='n'
while x != 'y':
    pil = input("Download json? = ")
    if pil == 'y':
        q = input("Keyword = ")
        p = input("Page = ")
        curl = getCurl(q,p)
        #File path save json
        with open("D:/P/Python/Data/"+q+p+".json", "w") as outfile:
            json.dump(curl, outfile)
        df = pd.json_normalize(curl)
    else :
        path = input("File Name = ")
        #open json file
        df = pd.read_json(r"D:/P/Python/Data/"+path+".json")
    links = []
    for i in range(80) :
        #take only url in json file
        links.append(df.videos[0][i]['url'])
    d=input("Download video? = ")
    if d == 'y' : download(links)
    x = input("Continue? = ")
