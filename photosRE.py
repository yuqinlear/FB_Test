'''
Created on 2012-9-24

@author: Paul
'''

import os,re,urllib,time
import FBlib,FBlogin

lastFbid_re=re.compile(r"\\\"last_fbid\\\":\\\"(\d+)\\\"|\\\"last_fbid\\\":(\d+)")
cursor_re=re.compile(r"enableContentLoader(\S+?)]]")
cursor_re2=re.compile(r"},\"(\S+)\"")
photos_re=re.compile(r"data-starred-src=\\\"(\S+)\"")
#photos_re2=re.compile(r"style=\\\"background-image: url\((\S+)\);\\\" class=\\\"uiMediaThumbImg\\\"")
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
taggedPhotos:True for column of "photo of 'user's name'" , False for column of "photos"
allPhotos: not all the photos of the user, but all photos the user uploaded
dyn: temporary generated token 
'''
def crawlPhotos(opener,login_id,profile_id,tagged_photos,fileName,dyn):
    if tagged_photos==True :
#        url_base="https://www.facebook.com/ajax/pagelet/generic.php/TaggedPhotosAppCollectionPagelet?ajaxpipe=1&ajaxpipe_token={token}&no_script_path=1&data=%7B%22scroll_load%22%3Atrue%2C%22last_fbid%22%3A%22{last_fbid}%22%2C%22fetch_size%22%3A{fetch_size}%2C%22profile_id%22%3A{profile_id}%2C%22tab_key%22%3A%22photos%22%2C%22sk%22%3A%22photos%22%2C%22pager_fired_on_init%22%3Atrue%7D&__user={user}&__a=1&__adt={adt}"
        url_base="https://www.facebook.com/ajax/pagelet/generic.php/TaggedPhotosAppCollectionPagelet?data=%7B%22collection_token%22%3A%22{profile_id}%3A2305272732%3A4%22%2C%22cursor%22%3A%22{encoded_cursor}%22%2C%22tab_key%22%3A%22photos%22%2C%22profile_id%22%3A{profile_id}%2C%22overview%22%3Afalse%2C%22ftid%22%3Anull%2C%22sk%22%3A%22photos%22%7D&__user={user}&__a=1&__dyn={dyn}"
    elif tagged_photos==False:
#        url_base="https://www.facebook.com/ajax/pagelet/generic.php/AllPhotosAppCollectionPagelet?ajaxpipe=1&ajaxpipe_token={token}&no_script_path=1&data=%7B%22scroll_load%22%3Atrue%2C%22last_fbid%22%3A%22{last_fbid}%22%2C%22fetch_size%22%3A{fetch_size}%2C%22profile_id%22%3A{profile_id}%2C%22tab_key%22%3A%22photos_stream%22%2C%22sk%22%3A%22photos_stream%22%2C%22pager_fired_on_init%22%3Atrue%7D&__user={user}&__a=1&__adt={adt}"
        url_base="https://www.facebook.com/ajax/pagelet/generic.php/AllPhotosAppCollectionPagelet?data=%7B%22collection_token%22%3A%22{profile_id}%3A2305272732%3A5%22%2C%22cursor%22%3A%22{encoded_cursor}%22%2C%22tab_key%22%3A%22photos%22%2C%22profile_id%22%3A{profile_id}%2C%22overview%22%3Afalse%2C%22ftid%22%3Anull%2C%22sk%22%3A%22photos%22%7D&__user={user}&__a=1&__dyn={dyn}"
    else:
        print "Bad parameter"
        FBlib.writeLog("Bad parameter")
        exit(1)
    with open(fileName,'ab') as tempFile:
#        tempFile.truncate()
        encoded_cursor=0
        url=url_base.format(dyn=dyn,profile_id=profile_id,user=login_id,encoded_cursor=encoded_cursor)
        print url
        readHtml=FBlib.getHtml(opener,url)   
        tempFile.write(readHtml)
        reResult1=cursor_re.findall(readHtml)
        if reResult1:
            reResult2=cursor_re2.findall(reResult1[0])
        '''use reResult to test if there is the token of cursor which decides if we need send more ajax-request'''
        while reResult1:
            print reResult2[0]
            encoded_cursor=urllib.urlencode({1:reResult2[0]})[2:]
            url=url_base.format(dyn=dyn,profile_id=profile_id,user=login_id,encoded_cursor=encoded_cursor)
            print url
            readHtml=FBlib.getHtml(opener,url)  
            reResult1=cursor_re.findall(readHtml)
            if reResult1:
                reResult2=cursor_re2.findall(reResult1[0])
            tempFile.write(readHtml)
    
def parsePhotoLink(inputFileName,outputFileName):
    with open(inputFileName,'r') as inputF, open(outputFileName,'ab')as outputF:
        readData=inputF.read()
        parseResult=FBlib.findByRE(photos_re,readData)
        for index,link in enumerate(parseResult):
            parseResult[index]=link.translate(None,'\\')
            outputF.write(parseResult[index]+'\r\n')
        return parseResult
    
'''urlretrieve is not good'''
def imageRetrieve(url,fileName):      
    f=open(fileName,'wb')
    f.write(urllib.urlopen(url).read())
    f.close()



if __name__=='__main__':  
#    login_id=100003948798862 #huanhuan.xie
#    login_id=100003950175394 #shirley.cia.9
    login_id=100004271103398 #david.pon
#    profile_id=573372729304       #788133694 
    profile_id=100001371438020        
    opener=FBlogin.getOpener()
    
    '''download photo'''
    profile_id_file="../facebook_output/image_ids_to_be_retrieve"
    with open(profile_id_file,'r') as id_file:  
        lines=id_file.readlines()
        for line in lines:
            profile_id=line.rstrip()
            directory='../facebook_output/FB_photos_fof/'  
            if not os.path.exists(directory):
                os.makedirs(directory)            
            sumPhotoLinkFile=directory+'SumPhotoLinks_%s'%(profile_id)
            print profile_id
            directory+='images/%s/'%(profile_id)
            if not os.path.exists(directory):
                os.makedirs(directory)          
            with open(sumPhotoLinkFile,'r') as linkFile:
                urls=linkFile.readlines()
                for url in urls:
                    temp_url=''.join(url.split('/p417x417'))
                    print temp_url
                    imageRetrieve(temp_url,directory+url.split('/')[-1].rstrip())
            
    
    '''crawl the photolinks for both fof and strangers '''
#    directory='../facebook_output/FB_photos_fof/'
#    profileIdFile='../facebook_output/profile_id.txt'
#    with open(profileIdFile,'r') as idFile :
#        for line in idFile:
#            time.sleep(1)
#            profile_id=line.rstrip()
#            print profile_id
#
#            sumPhotoLinkFile=directory+'SumPhotoLinks_%s'%(profile_id)
#            allPhotoHtmlFile=directory+'AllPhotoHtml_%s'%(profile_id)
#            taggedPhotoHtmlFile=directory+'TaggedPhotoHtmlFile%s'%(profile_id)
#            allPhotoLinkFile=directory+'AllPhotoLinks_%s'%(profile_id)
#            taggedPhotoLinkFile=directory+'TaggedPhotoLinks_%s'%(profile_id)
#            crawlPhotos(opener=opener, login_id=login_id,profile_id=profile_id, tagged_photos=True, fileName=taggedPhotoHtmlFile, dyn='798aD5yqmp5U')     
#            crawlPhotos(opener=opener, login_id=login_id,profile_id=profile_id, tagged_photos=False, fileName=allPhotoHtmlFile, dyn='798aD5yqmp5U')    # 798aD5z5ynU
#            allPhotoLink=parsePhotoLink(allPhotoHtmlFile,allPhotoLinkFile)
#            taggedPhotoLink=parsePhotoLink(taggedPhotoHtmlFile,taggedPhotoLinkFile)
#            sumPhotoLink=allPhotoLink+taggedPhotoLink
#            setPhotoLink=set(sumPhotoLink)
#            FBlib.writeLog(profile_id,len(taggedPhotoLink),len(allPhotoLink),len(setPhotoLink))
#            if len(setPhotoLink)<2:
#                continue
#            with open(sumPhotoLinkFile,'ab') as sumLinkFile:
#                for link in setPhotoLink:
#                    sumLinkFile.write(link+'\r\n')
    print "done"
