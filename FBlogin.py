'''
Created on Feb 21, 2013

@author: Paul
'''
import urllib2, cookielib
import mechanize


def getOpener():
    cookiefile ="../facebook_output/cookies.txt"   
    cookies = cookielib.MozillaCookieJar()
    cookies.load(cookiefile, ignore_discard=True, ignore_expires=True)
    opener=urllib2.build_opener(urllib2.HTTPCookieProcessor(cookies))
    return opener

def FBlogin(username,password):
    
    br=mechanize.Browser()
    #br.set_handle_equiv(True)
    #br.set_handle_gzip(True)
    br.set_handle_redirect(True)
    br.set_handle_referer(True)
    br.set_handle_robots(False)
    cookiefile ="../facebook_output/cookies.txt" 
    cookiejar = mechanize.MozillaCookieJar()
    br.set_cookiejar(cookiejar)
    br.addheaders=[("User-Agent","Mozilla/5.0 (Windows NT 5.1; rv:15.0) Gecko/20100101 Firefox/15.0")]
    br.open('https://login.facebook.com/login.php?login_attempt=1')
    br.select_form(nr=0)
    br.form['email']=username
    br.form['pass']=password
    response=br.submit().read()

    with open('../facebook_output/loginlog.txt','wb') as loginlog:
        loginlog.write(response)
        if response.find("Log Out") == False:
            print 'cannot login'
            open(cookiefile,'w').close()
            return -1  
        else:  
            cookiejar.save(cookiefile,ignore_discard=True, ignore_expires=True)
            print 'login successfully'
            return 1

if __name__=='__main__':
#    username='gter07@gmail.com'
    username='1085767795@qq.com'
    password='33333366'
    print FBlogin(username,password)