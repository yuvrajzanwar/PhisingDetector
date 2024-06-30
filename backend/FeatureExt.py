import ipaddress
import re
from bs4 import BeautifulSoup
import requests
from googlesearch import search
import whois
from datetime import date, datetime
import time
from dateutil.parser import parse as date_parse
from urllib.parse import urlparse,urlencode
import numpy as np
import pickle
from xgboost import XGBClassifier

def FeatureExt(url):
  feature=[]
  feature.append(UsingIp(url))
  feature.append(longUrl(url))
  feature.append(shortUrl(url))
  feature.append(symbol(url))
  feature.append(prefixSuffix(url))
  feature.append(SubDomains(url))
  feature.append(Hppts(url))
  feature.append(Favicon(url))
  feature.append(RequestURL(url))
  feature.append(AnchorURL(url))
  feature.append(LinksInScriptTags(url))
  feature.append(DisableRightClick(url))
  feature.append(AgeofDomain(url))
  feature.append(GoogleIndex(url))
  feature.append(LinksPointingToPage(url))
  return np.array(feature).reshape(1,15)
#1
def UsingIp(url):
    try:
        ipaddress.ip_address(url)
        
        return -1
    except:
        return 1

#2
def AnchorURL(url):
    try:
        
        urlp = urlparse(url)
        #print(urlp,'s')
        domain = urlp.netloc
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        i,unsafe = 0,0
        for a in soup.find_all('a', href=True):
            if "#" in a['href'] or "javascript" in a['href'].lower() or "mailto" in a['href'].lower() or not (url in a['href'] or domain in a['href']):
                unsafe = unsafe + 1
            i = i + 1

        try:
            percentage = unsafe / float(i) * 100
            if percentage < 31.0:
                return 1
            elif ((percentage >= 31.0) and (percentage < 67.0)):
                return 0
            else:
                return -1
        except:
            return -1

    except:
        return -1
    
#3
def longUrl(url):
    if len(url) < 54:
        return 1
    if len(url) >= 54 and len(url)<=75:
        return 0
    return -1

#4
def shortUrl(url):
    match = re.search('bit\.ly|goo\.gl|shorte\.st|go2l\.ink|x\.co|ow\.ly|t\.co|tinyurl|tr\.im|is\.gd|cli\.gs|'
                'yfrog\.com|migre\.me|ff\.im|tiny\.cc|url4\.eu|twit\.ac|su\.pr|twurl\.nl|snipurl\.com|'
                'short\.to|BudURL\.com|ping\.fm|post\.ly|Just\.as|bkite\.com|snipr\.com|fic\.kr|loopt\.us|'
                'doiop\.com|short\.ie|kl\.am|wp\.me|rubyurl\.com|om\.ly|to\.ly|bit\.do|t\.co|lnkd\.in|'
                'db\.tt|qr\.ae|adf\.ly|goo\.gl|bitly\.com|cur\.lv|tinyurl\.com|ow\.ly|bit\.ly|ity\.im|'
                'q\.gs|is\.gd|po\.st|bc\.vc|twitthis\.com|u\.to|j\.mp|buzurl\.com|cutt\.us|u\.bb|yourls\.org|'
                'x\.co|prettylinkpro\.com|scrnch\.me|filoops\.info|vzturl\.com|qr\.net|1url\.com|tweez\.me|v\.gd|tr\.im|link\.zip\.net', url)
    if match:
        return -1
    return 1
    
#5
def prefixSuffix(url):
    try:
      domain=urlparse(url).netloc
      match = re.findall('\-',domain)
      if match :
          return -1 
      return 1           
    except:
      return -1
  
#6
def SubDomains(url):
    dot_count = len(re.findall("\.", url))
    if dot_count == 1:
        return 1
    elif dot_count == 2:
        return 0
    return -1

#7
def Hppts(url):
    try:
        urlparse=urlparse(url)
        https = urlparse.scheme
        if 'https' in https:
            return 1
        return -1
    except:
        return 1

#8
def symbol(url):
    if re.findall("@",url):
        return -1
    return 1
    
#9
def Favicon(url):
    try:
        urlp = urlparse(url)
        domain = urlp.netloc
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        #print('soup',soup)

        for head in soup.find_all('head'):
            for head.link in soup.find_all('link', href=True):
                dots = [x.start(0) for x in re.finditer('\.', head.link['href'])]
                if url in head.link['href'] or len(dots) == 1 or domain in head.link['href']:
                    return 1
        return -1
    except:
        return -1

#10
def LinksPointingToPage(url):
    try:
        response=requests.get(url)
        number_of_links = len(re.findall(r"<a href=", response.text))
        if number_of_links == 0:
            return 1
        elif number_of_links <= 2:
            return 0
        else:
            return -1
    except:
        return -1

#11
def AgeofDomain(url):
    try:
        urlp = urlparse(url)
        
        
        domain = urlp.netloc
        
        
        whois_response = whois.whois(domain)
        #print("wois=",whois_response)
        
        
        creation_date = whois_response.creation_date
        
        try:
            if(len(creation_date)):
                creation_date = creation_date[0]
        except:
            pass

        today  = date.today()
        age = (today.year-creation_date.year)*12+(today.month-creation_date.month)
        #print('age',age)
        if age >=6:
            return 1
        return -1
    except:
        return -1

#12
def RequestURL(url):
    try:
        i=0
        success=0
        urlp = urlparse(url)
        domain = urlp.netloc
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        #print(soup)

        for img in soup.find_all('img', src=True):
            dots = [x.start(0) for x in re.finditer('\.', img['src'])]
            if url in img['src'] or domain in img['src'] or len(dots) == 1:
                success = success + 1
            i = i+1

        for audio in soup.find_all('audio', src=True):
            dots = [x.start(0) for x in re.finditer('\.', audio['src'])]
            if url in audio['src'] or domain in audio['src'] or len(dots) == 1:
                success = success + 1
            i = i+1

        for embed in soup.find_all('embed', src=True):
            dots = [x.start(0) for x in re.finditer('\.', embed['src'])]
            if url in embed['src'] or domain in embed['src'] or len(dots) == 1:
                success = success + 1
            i = i+1

        for iframe in soup.find_all('iframe', src=True):
            dots = [x.start(0) for x in re.finditer('\.', iframe['src'])]
            if url in iframe['src'] or domain in iframe['src'] or len(dots) == 1:
                success = success + 1
            i = i+1

        try:
            #print(i,success)
            percentage = success/float(i) * 100
            
            if percentage < 22.0:
                return 1
            elif((percentage >= 22.0) and (percentage < 61.0)):
                return 0
            else:
                return -1
        except:
            return 0
    except:
        return -1

#13
def LinksInScriptTags(url):
    try:
        i,success = 0,0
        urlp = urlparse(url)
        domain = urlp.netloc
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
    
        for link in soup.find_all('link', href=True):
            dots = [x.start(0) for x in re.finditer('\.', link['href'])]
            if url in link['href'] or domain in link['href'] or len(dots) == 1:
                success = success + 1
            i = i+1

        for script in soup.find_all('script', src=True):
            dots = [x.start(0) for x in re.finditer('\.', script['src'])]
            if url in script['src'] or domain in script['src'] or len(dots) == 1:
                success = success + 1
            i = i+1

        try:
            percentage = success / float(i) * 100
            #print(percentage)
            if percentage < 17.0:
                return 1
            elif((percentage >= 17.0) and (percentage < 81.0)):
                return 0
            else:
                return -1
        except:
            return 0
    except:
        return -1


#14
def DisableRightClick(url):
    try:
        response = requests.get(url)
        if re.findall(r"event.button ?== ?2", response.text):
            return 1
        else:
            return -1
    except:
            return -1

#15
def GoogleIndex(url):
    try:
        site = search(url, 5)
        if site:
            return 1
        else:
            return -1
    except:
        return 1
        

#URL FROM FROM END HERE

feat=FeatureExt(url)

model =pickle.load(open('Phishing Model 96.pkl','rb'))
pred=model.predict(feat)
if pred ==1 :
    print(url ,"is SAFE")
else:
    print(url ,"is NOT SAFE!")