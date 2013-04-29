'''
Created on 2012-8-30
This module is used to crawl down and parse the user's friend page
@author: lear
'''
import re,csv,sys,FBlogin
from FBlib import *

friend_num_re=re.compile(r"<div class=\"_qy\">(.*?)</div><div class=\"_qz\">Friends")
friendlist_re = re.compile(r"data-hovercard=\\\"\\/ajax\\/hovercard\\/user.php\?id=(\d+)") 

#def parseFriendsStr(frdFile,outputCSV):
#    friendlist_re2=re.compile(r"http:(.*?) data-hovercard=\\\"\\/ajax\\/hovercard\\/user.php\?id=1415712234")
#    #  friendlist_re2=r"href=\\\"http:(.*?)\" data-hovercard=\\\"\\/ajax\\/hovercard\\/user.php\?id="
#    fcsv=open(outputCSV,'ab')
#    fread=open(frdFile,'rb')
#    cw = csv.writer(fcsv)
#    fcsv.truncate()
#    counter=0  
#    readData=fread.read()
#    #  result=re.match(friendlist_re2,readData)
#    result=findByRE(friendlist_re2,readData)
#    print result
#    for element in result:
#        counter+=1
#        cw.writerow([element])  
#    fcsv.close()
#    fread.close()
#    return counter

def parseFriends(frdFile): 
    with open(frdFile,'rb') as fread:
        readData=fread.read()
        return findByRE(friendlist_re,readData)
  
    
def parseFriendsToCSV(frdFile,outputCSV):
    friendlist_re = re.compile(r"data-hovercard=\\\"\\/ajax\\/hovercard\\/user.php\?id=(\d+)")  
    try:
        fcsv=open(outputCSV,'ab')
        fread=open(frdFile,'rb')
        cw = csv.writer(fcsv)
        fcsv.truncate()
        counter=0  
        readData=fread.read()
        result=findByRE(friendlist_re,readData)
        for element in result:
            counter+=1
            cw.writerow([element])  
        return counter
    except:
        writeLog(sys.exc_info())    
    finally:
        fcsv.close()
        fread.close()

'''crawl the friend page and return the number of photos if it is applicable '''
def parseFriendNum(opener,uid):
    url="http://www.facebook.com/profile.php?id={uid}&sk=friends&v=friends".format(uid=uid)
    html=getHtml(opener,url)
    return int(findByRE(friend_num_re,html)[0])

def crawlFriends(opener,login_id,uid):
    frdNum=parseFriendNum(uid)  
    try:
        tempFile=open("./FB/%d_frd"%(uid),'ab')
        tempFile.truncate()
        start=0
        while (start<=frdNum):
            url="http://www.facebook.com/ajax/browser/list/allfriends/?uid=%d&infinitescroll=1&"\
                "location=friends_tab_tl&start=%d&__user=%d&__a=1" % (uid,start,login_id)
            #    params=urllib.urlencode({'__a':1,'__user':100004271103398,'fb_dtsg':fb_dtsg,'phstamp':phstamp})
            #    req=urllib2.Request(url,params)
            #    buf = opener.open(req)
            print url
            writeLog(url)
            friendHtml=getHtml(opener,url)
            tempFile.write(friendHtml)
            start+=24
    except:
        writeLog(sys.exc_info())
    finally:
        tempFile.close()  
  




if __name__=='__main__':
#    uid=100003950175394 #shirley.cia.9
    uid=100003948798862 #huanhuan.xie.9
#    login_id=100003948798862 #huanhuan.xie.9
    login_id=100003950175394
    opener=FBlogin.getOpener()
    print parseFriendNum(opener,uid)
    

#    crawlFriends(opener,login_id,uid)
#    
#    f1="../facebook_output/%d_frd"%(uid)
#    fcsv="../facebook_output/%d_frd.csv"%(uid)
#    print parseFriendsToCSV(f1,fcsv)
#    
    print "done"
  
#friendNum_re=re.compile("\(<span class=\"fsxl\">([,\d]+)</span>\)")
#friendlist_re = re.compile(r"data-hovercard=\"/ajax/hovercard/user.php\?id=(\d+)")
#friendlist_browser_re=re.compile("<div class=\"fbProfileBrowser\">(.*)</div>")
#friendlist_re_old = re.compile(r"engagement&quot;:&#123;&quot;eng_type&quot;:&quot;1&quot;,&quot;eng_src&quot;:&quot;2&quot;,&quot;eng_tid&quot;:&quot;(\d+)&quot;,&quot;eng_data&quot;:\[\]")
#friendlist_re_old = re.compile(r"<div class=\"fsl fwb fcb\"><a href=\".*?\" data-gt=\"&#123;&quot;engagement&quot;:&#123;&quot;eng_type&quot;:&quot;1&quot;,&quot;eng_src&quot;:&quot;2&quot;,&quot;eng_tid&quot;:&quot;(\d+)&quot;,&quot;eng_data&quot;:\[\]")
#friendlist_re_old = re.compile(r"<div class=\"fsl fwb fcb\"><a href=\".*?\" data-gt=\"&#123;\";engagement\";:&#123;\";eng_type\";:\";1\";,\";eng_src\";:\";2\";,\";eng_tid\";:\";(\d+)\";,\";eng_data\";:\[\]") 