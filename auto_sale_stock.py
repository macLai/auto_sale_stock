import urllib
import sys
import random
import urllib2
from bs4 import BeautifulSoup
import re
def analysis(data):
 startDay = random.randint(20,len(data)-1)
 data_gupiao = data[startDay].findAll('td')
 print data_gupiao[1].div.string
 money_now = float(data_gupiao[1].div.string)
 money_start = money_now
 min_out = money_now*0.96
 now = startDay - 1
 while (now > 1):
  data_gupiao = data[now].findAll('td')
  if(money_now < float(data_gupiao[1].div.string)): min_out = float(data_gupiao[1].div.string)*0.96
  money_now = float(data_gupiao[1].div.string)
  if(money_now < min_out): break
  now = now - 1
 print money_now/money_start
 return money_now/money_start


def readDoc(doc):
 soup = BeautifulSoup(doc, from_encoding = 'utf8')
 str_id = soup.title.string #soup.body.find_all('')
 if(str_id.split('(')[0] == ''): return 0
 print str_id.split('(')[0]
 str_data = soup.body.find('table',attrs={'id':'FundHoldSharesTable'}) #id="FundHoldSharesTable" class="table" cellpadding="0" cellspacing="0"
 if(str_data == None): return 0
 return analysis(str_data.findAll('tr'))



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
  sys.setdefaultencoding( "utf-8" )
  count = 0
  startMoney = 1;
  nowMoney = 1;
  while (count < 50):
        gupiaoNum = random.randint(600000,601999)
        startYear = random.randint(2000,2013)
        startSeason = random.randint(1,4)
        print 'http://money.finance.sina.com.cn/corp/go.php/vMS_MarketHistory/stockid/%d.phtml?year=%d&jidu=%d'%(gupiaoNum,startYear,startSeason)
        nowMoney = readDoc(download('http://money.finance.sina.com.cn/corp/go.php/vMS_MarketHistory/stockid/%d.phtml?year=%d&jidu=%d'%(gupiaoNum,startYear,startSeason)))
        if(nowMoney != 0):
         startMoney = startMoney*nowMoney
         print startMoney
         count = count + 1







