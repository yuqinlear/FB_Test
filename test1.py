'''
Created on Feb 24, 2013

@author: Paul
'''
import mechanize,urllib2,urllib,threading,thread,random,FBlib,csv,re
from photosRE import *

headers = {
    "User-Agent" : "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:20.0) Gecko/20100101 Firefox/20.0",
    "Accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language" : "zh,en-us;q=0.7,en;q=0.3",
    "Host": "www.facebook.com"
}
token=176502172502252
for x in range(100):
    token+=1
    url="https://www.facebook.com/"+str(token)
    request=urllib2.Request(url=url,headers=headers)
    opener=FBlogin.getOpener()
    try:
        response=opener.open(request) 
        print url
    except urllib2.HTTPError,err:
        print err.code
    finally:
        FBlib.sleepRandom(1, 5)

##profileIdFile='../facebook_output/profile_id.txt'
#directory='../photolink_penetrating/'    
#if not os.path.exists(directory):
#        os.makedirs(directory)
#
##link_re=re.com
#file=directory+'100004271103398.txt'
#
#with open(file,'r') as inputfile:
#    urls=inputfile.readlines()
#    for url in urls:
#        print re.findall('_(.*?)\_',url)[0]
    
#dirs = os.listdir( directory )
#for dir in dirs:
#    FBlib.writeLog(dir,len([name for name in os.listdir(directory+dir)]))
#print "done"

#with open(photoLinkFile,'rb') as linkfile,open(photoLinkFile+'_','wb') as linkfile2 :
#    urls=linkfile.readlines()
#    for url in urls:
#        linkfile2.write(''.join(url.split('/p206x206')))

#def  urlPost():
#    url='http://xsrm43.b146y4.dfces.asia/233dfger/'
#    opener = urllib2.build_opener()
#    headers = {
#    "Host": "xsrm43.b146y4.dfces.asia",
#    "User-Agent" : "Mozilla/5.0 (Windows NT 5.1; rv:15.0) Gecko/20100101 Firefox/15.0",
#    "Accept" : " text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
#    "Accept-Language" : "zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3",
#    "Content-type": "application/x-www-form-urlencoded",
#    "Connection": "keep-alive"
#    }
#    
#    while True:
#        randomInt=random.randint(11112,11111110)
#        data = urllib.urlencode({'username':randomInt,'pwd':randomInt<<2})
#        opener.open(urllib2.Request(url,data,headers))
#        
#threading.Thread(target=urlPost).start()
#threading.Thread(target=urlPost).start()
#threading.Thread(target=urlPost).start()
#threading.Thread(target=urlPost).start()
#threading.Thread(target=urlPost).start()
#threading.Thread(target=urlPost).start()
#threading.Thread(target=urlPost).start()
#threading.Thread(target=urlPost).start()
#threading.Thread(target=urlPost).start()
#threading.Thread(target=urlPost).start()
#threading.Thread(target=urlPost).start()
#threading.Thread(target=urlPost).start()