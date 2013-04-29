import urllib2,random,time,csv
from datetime import datetime

def sleepRandom(int1,int2):
    randomInt=random.randint(int1,int2)
    time.sleep(randomInt) 

headers = {
    "User-Agent" : "Mozilla/5.0 (Windows NT 5.1; rv:15.0) Gecko/20100101 Firefox/15.0",
    "Accept" : "text/xml,application/xml,application/xhtml+xml,text/html;q=0.9,text/plain;q=0.8,text/png,*/*;q=0.5",
    "Accept-Language" : "en-us,en;q=0.5",
    "Accept-Charset" : "ISO-8859-1",
    "Content-type": "application/x-www-form-urlencoded",
    "Host": "m.facebook.com"
}


def getVersion(opener,fb_id):
    url = "http://www.facebook.com/profile.php?id=%d" % (fb_id)  
    req = urllib2.Request(url)
    buf = opener.open(req)
    versionHtml = buf.read()
    if(versionHtml.find("Timeline, a new kind of profile.")!=-1):
        isNewVersion = 1  #found
    else:
        isNewVersion = 0
    return isNewVersion
  
def getRedirUrl(opener,url):  
    response=opener.open(url)
    redirectUrl = response.geturl()
    return redirectUrl
  
def getAbout(opener,url):
    url = url+"/info" 
    req = urllib2.Request(url)
    buf = opener.open(req)
    aboutHtml = buf.read()
    print url
    return aboutHtml

def getHtml(opener,url):
    req = urllib2.Request(url)
    buf = opener.open(req)
    aboutHtml = buf.read()
    return aboutHtml

def findByRE(regexp,source):
    return regexp.findall(source) 


def writeLog(*args):
    with open('../facebook_output/log.csv','ab') as flog:
        content=[datetime.now()]+list(args)
        cw = csv.writer(flog)
        cw.writerow(content)   
    
    
def clearLog():
    open('../facebook_output/log.csv','w').close()
