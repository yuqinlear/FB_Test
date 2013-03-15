'''
Created on 2012-9-24

@author: Paul
'''
'''
Created on 2012-9-4

@author: lear
'''
import os,re
import FBlib,FBlogin


lastFbid_re=re.compile(r"\\\"last_fbid\\\":\\\"(\d+)\\\"|\\\"last_fbid\\\":(\d+)")
photos_re2=re.compile(r"style=\\\"background-image: url\((\S+)\);\\\" class=\\\"uiMediaThumbImg\\\"")
def getLastFbid(fileName):
    fread=open(fileName,'r')
    readData=fread.read()
    result=re.search(lastFbid_re,readData)
    if result is None:
        return
    elif result.group(1):
        print "group 1"
        return result.group(1)
    else: 
        print "group 2"
        return result.group(2)

'''
crawl photos either belonging to column of "photo of 'user's name'" or column of "photos".
is_photosstream: False for column of "photo of 'user's name'" , True for column of "photos"
'''
def crawlPhotos(opener,login_id,profile_id,token,fetch_size,is_photosstream,filename):
    if is_photosstream==False :
        url_base="https://www.facebook.com/ajax/pagelet/generic.php/TimelinePhotosPagelet?ajaxpipe=1&ajaxpipe_token={token}&no_script_path=1&data=%7B%22scroll_load%22%3Atrue%2C%22last_fbid%22%3A%22{last_fbid}%22%2C%22fetch_size%22%3A{fetch_size}%2C%22profile_id%22%3A{profile_id}%2C%22tab_key%22%3A%22photos%22%2C%22sk%22%3A%22photos%22%2C%22pager_fired_on_init%22%3Atrue%7D&__user={user}&__a=1&__adt={adt}"
    elif is_photosstream==True:
        url_base="https://www.facebook.com/ajax/pagelet/generic.php/TimelinePhotosStreamPagelet?ajaxpipe=1&ajaxpipe_token={token}&no_script_path=1&data=%7B%22scroll_load%22%3Atrue%2C%22last_fbid%22%3A%22{last_fbid}%22%2C%22fetch_size%22%3A{fetch_size}%2C%22profile_id%22%3A{profile_id}%2C%22tab_key%22%3A%22photos_stream%22%2C%22sk%22%3A%22photos_stream%22%2C%22pager_fired_on_init%22%3Atrue%7D&__user={user}&__a=1&__adt={adt}"
    else:
        print "Bad is_photosstream parameter"
        FBlib.writeLog("Bad is_photosstream parameter")
        exit(1)
    with open(filename,'ab') as tempFile:
#        tempFile.truncate()
        last_fbid=0
        adt=1
        url=url_base.format(token=token,last_fbid=last_fbid,fetch_size=fetch_size,profile_id=profile_id,user=login_id,adt=adt)
        print url
        readHtml=FBlib.getHtml(opener,url)   
        tempFile.write(readHtml)
        reResult=re.search(lastFbid_re,readHtml)
        '''use reResult to test if there is lastFbid which decides if we need send more ajax-request'''
    while reResult:
        adt+=1
        if reResult.group(1):
            last_fbid=reResult.group(1)
        else: last_fbid=reResult.group(2)
        url=url_base.format(token=token,last_fbid=last_fbid,fetch_size=fetch_size,profile_id=profile_id,user=login_id,adt=adt)
        print url
        readHtml=FBlib.getHtml(opener,url)  
        reResult=re.search(lastFbid_re,readHtml)
        tempFile.write(readHtml)
    
def parsePhotoLink(fileName):
    with open(fileName,'r') as fread:
        readData=fread.read()
        parseResult=FBlib.findByRE(photos_re2,readData)
        for index,link in enumerate(parseResult):
            parseResult[index]=link.translate(None,'\\')
        return parseResult


if __name__=='__main__':  
#    login_id=100003948798862 #huanhuan.xie
    login_id=100003950175394 #shirley.cia.9
    profile_id=510139179       #788133694 
    
    directory='../facebook_output/FB_photos_test/'    
    if not os.path.exists(directory):
            os.makedirs(directory)
    htmlFile=directory+'photosstream_%d'%(profile_id)
    photoLinkFile=directory+'linkfile_%d'%(profile_id)

    opener=FBlogin.getOpener()
    crawlPhotos(opener,login_id,profile_id,'AXj75IihobOKGn3A',100,True,htmlFile) 
#    
    links=parsePhotoLink(htmlFile)
    for link in links:
        with open(photoLinkFile,"ab") as tempFile:
            tempFile.write(link+'\r\n')
    print len(links)
    
    print "done"