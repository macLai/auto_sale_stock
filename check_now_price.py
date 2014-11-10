# coding=gbk
import urllib
import sys
import random
import urllib2
from bs4 import BeautifulSoup
import re
import time
def download(url):
 header = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6',
 'Referer':None
 }
 req = urllib2.Request(url, headers=header )
 con = urllib2.urlopen( req )
 doc = con.read()
 con.close()
 return doc
 
    
if __name__ == '__main__':
  reload(sys)
  sys.setdefaultencoding( "gbk" )
  yesterdayPrice = 0;
  #var hq_str_sh601006="大秦铁路,8.03,7.96,8.40,8.54,8.03,8.39,8.40,104467577,872128829,323672,8.39,289100,8.38,903215,8.37,1051300,8.36,1185488,8.35,104926,8.40,800,8.41,331956,8.42,153311,8.43,248993,8.44,2014-11-10,11:35:48,00";
  #sunriseyuan77@icloud.com
  while 1:
    data =  download("http://hq.sinajs.cn/list=sz000568").decode("gbk").encode('utf-8')
    data = data.split('"')[1].split(",")
    nowPrice = float(data[3])
    tempPrice = float(data[2])
    if(yesterdayPrice < tempPrice): yesterdayPrice = tempPrice
    print nowPrice
    if(yesterdayPrice*0.98 >nowPrice):
      #mail
      print 'sell it'
      exit(0)
    time.sleep(60)
  
