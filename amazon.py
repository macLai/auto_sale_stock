import urllib
import sys
import random
import urllib2
from bs4 import BeautifulSoup
import re
import time

CN = 0
JP = 1
US = 2
UK = 3
FR = 4
DE = 5
ES = 6
IT = 7
path[US] = "http://www.amazon.cn/s/ref=nb_sb_noss_1?__mk_zh_CN=%E4%BA%9A%E9%A9%AC%E9%80%8A%E7%BD%91%E7%AB%99&url=search-alias%3Daps&field-keywords="
path[JP] = "http://www.amazon.co.jp/s/ref=nb_sb_noss?__mk_ja_JP=%E3%82%AB%E3%82%BF%E3%82%AB%E3%83%8A&url=search-alias%3Daps&field-keywords="
path[US] = "http://www.amazon.com/s/ref=nb_sb_noss_2?url=search-alias%3Daps&field-keywords="
path[UK] = "http://www.amazon.co.uk/s/ref=nb_sb_noss/275-2769705-5891052?url=search-alias%3Daps&field-keywords="
path[FR] = "http://www.amazon.fr/s/ref=nb_sb_noss/277-1824098-6979569?__mk_fr_FR=%C3%85M%C3%85%C5%BD%C3%95%C3%91&url=search-alias%3Daps&field-keywords="
path[DE] = "http://www.amazon.de/s/ref=nb_sb_noss/275-2107536-2628601?__mk_de_DE=%C3%85M%C3%85%C5%BD%C3%95%C3%91&url=search-alias%3Daps&field-keywords="
path[ES] = "http://www.amazon.es/s/ref=nb_sb_noss/275-8162056-7297615?__mk_es_ES=%C3%85M%C3%85%C5%BD%C3%95%C3%91&url=search-alias%3Daps&field-keywords="
path[IT] = "http://www.amazon.it/s/ref=nb_sb_noss/280-7732838-4809540?__mk_it_IT=%C3%85M%C3%85%C5%BD%C3%95%C3%91&url=search-alias%3Daps&field-keywords="


class Amazon:
  country = ""
  keyword = ""
  def __init__(self,country,keyword):
    self.country = country
    self.keyword = keyword
    download(path[country]+keyword)

  def download(url):
    header = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6',
    'Referer':None
    }
    req = urllib2.Request(url, headers=header )
    con = urllib2.urlopen( req )
    doc = con.read()
    con.close()
    return doc
 
  def read(data):
    soup = BeautifulSoup(data)
    productList = soup.find(id = "s-results-list-atf").findAll('li', {"class","s-result-item"})
  
    print len(productList)
    
if __name__ == '__main__':
  data = download(CN+"abc")
  read(data)

