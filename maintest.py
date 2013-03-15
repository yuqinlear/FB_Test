'''
Created on Feb 22, 2013

@author: Paul
'''


import FBlogin,os,photosRE

#username='gter07@gmail.com'
##    username='1085767795@qq.com'
#password='33333366'
#FBlogin(username,password)

#    login_id=100003950175394 #shirley.cia.9

#login_id=100003948798862 #huanhuan.xie
login_id=100003950175394 #shirley.cia.9
profile_id=100001976748804       #788133694 


directory='../facebook_output/FB_photos_test/'    
if not os.path.exists(directory):
        os.makedirs(directory)
htmlFile=directory+'photos_%d'%(profile_id)
photoLinkFile=directory+'linkfile_%d'%(profile_id)

opener=FBlogin.getOpener()
photosRE.crawlPhotos(opener,login_id,profile_id,'AXj75IihobOKGn3A',100,True,htmlFile) 
photosRE.crawlPhotos(opener,login_id,profile_id,'AXj75IihobOKGn3A',100,False,htmlFile) 
#    
links=photosRE.parsePhotoLink(htmlFile)
for link in links:
    with open(photoLinkFile,"ab") as tempFile:
        tempFile.write(link+'\r\n')
print len(links)

print "done"



