'''
Created on Feb 24, 2013

@author: Paul
'''

profile_id=100001976748804
directory='./FB_photos_test/' 
photoLinkFile=directory+'linkfile_%d'%(profile_id)


with open(photoLinkFile,'rb') as linkfile,open(photoLinkFile+'_','wb') as linkfile2 :
    urls=linkfile.readlines()
    for url in urls:
        linkfile2.write(''.join(url.split('/p206x206')))

