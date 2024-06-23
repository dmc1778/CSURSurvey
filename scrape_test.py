import random
# driver=webdriver.Chrome()
# driver.get("https://www.facebook.com/")
from selenium.webdriver.common.by import By
# from util import io
from urllib.parse import urlencode, urlparse, parse_qs
from lxml.html import fromstring
from requests import get
import urllib.request
from xml.etree.ElementTree import XML, fromstring
import time
import csv
import re
import json
from selenium import webdriver 
import requests
import bs4
import codecs

driver=webdriver.Chrome()

driver.get("https://www.facebook.com/")



def parse_selenium_text(whole_text, keyword):
  new_list = []
  lo = whole_text.splitlines()
  ss = keyword.split('+')
  ss = '|'.join(ss)
  for item in lo:
    if re.search(r'('+ss+')', item):
        new_list.append([item, 'sciencedirect'])
  return new_list

def write_to_csv(paper_list, filename):
  with open(filename+".csv", "a", newline="") as f:
      writer = csv.writer(f, dialect='excel', delimiter='\n')
      writer.writerow(paper_list)

def parse_title(title_list):
  string_list = []
  for item in title_list:
    if isinstance(item, bs4.element.Tag):
      string_list.append(item.contents[0])
    if isinstance(item, bs4.element.NavigableString):
      string_list.append(item)
  string_list = ' '.join(string_list)
  return string_list



def newWriter(paper_list, filename):
  result_file = open(filename+".csv",'a', newline='', encoding="utf-8")
  wr = csv.writer(result_file, dialect='excel')
  #wr.writerows([[item] for item in paper_list])
  wr.writerow([paper_list[0], paper_list[1]])


def parse_acm(pager_number, myurl):
  paper_list = []
  content = requests.get(myurl)

  page_soup = soup(content.text, "html.parser")

  current_page = page_soup.contents[2].contents[2].contents[9].contents[1].contents[3].contents[1].contents[0].contents[1].contents[3].contents[3].contents
  if len(current_page) == 2:
    return None
  for item in current_page:
    if isinstance(item, bs4.element.Tag):
      if bool(item.attrs) == False:
        continue 
      if item.attrs['class'][0] == 'search__item':
        try:
          current_paper = item.contents[3].contents[3].contents[1].contents
          raw_title_info = current_paper[1].contents[0].contents[0].contents
          doi = current_paper[5].contents[0].attrs['href']
          pub_place = current_paper[5].contents[0].attrs['title']
          title = parse_title(raw_title_info)
          print(title)
          paper_list.append([title, pub_place])
        except:
          print('Parse Error!')

  write_to_csv(paper_list, 'ACMPaperList')



def parse_scienceDirect(init_pgsize, pager_number, myurl, keyword):
  headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:63.0) Gecko/20100101 Firefox/63.0'}
 
  content = requests.get(myurl, headers=headers)
  driver.get(myurl)
  
  time.sleep(2)
  bidy = driver.find_element(By.CLASS_NAME, 'col-xs-24')
  a = bidy.find_element(By.ID, 'srp-results-list')
  b = a.find_element(By.CLASS_NAME, 'search-result-wrapper')
  print(b)
  
  list = parse_selenium_text(b.text, keyword)

  for item in list:
    newWriter(item, 'scienceDirectPaperList')

  myurl = 'https://www.sciencedirect.com/search?qs='+ keyword +'&date=2010-2021&offset='+ str(init_pgsize)
  print('Analysis of page {} finished'.format(pager_number))
  print('Total number of papers extracted so far:', len(list))
  pager_number += 1
  init_pgsize += 100
  parse_scienceDirect(init_pgsize, pager_number, myurl, keyword)


def parseIEEE(pager_number, pgsize, init_url, keyword):
  print('I am analyzing this page:', pgsize)

  llist = []

  driver.get(init_url)

  time.sleep(2)
  bidy = driver.find_element(By.CLASS_NAME,'main-section')
  a = bidy.find_element(By.TAG_NAME,'xpl-results-list')
  time.sleep(5)
  b = a.find_element(By.CLASS_NAME,'List-results-items')

  for item in b:
    splited = item.text.split('\n')
    llist.append([splited[0], splited[2]])

  for item in llist:
    newWriter(item, 'IEEEpaperslist')

  myurl = 'https://ieeexplore.ieee.org/search/searchresult.jsp?queryText='+keyword+'&highlight=true&returnType=SEARCH&matchPubs=true&ranges=2010_2021_Year&returnFacets=ALL&rowsPerPage='+str(pgsize)+'&pageNumber='+str(pager_number)
  print('Analysis of page {} finished'.format(pager_number))
  print('Total number of papers extracted so far:', len(llist))
  pager_number += 1
  pgsize += 100
  parseIEEE(pager_number, pgsize, myurl, keyword)


  def main():
    start = timer()
    pager_number = 1
    init_pgsize = 100

    queries = loadtxt()
    for title in queries:
        # acm_url = 'https://dl.acm.org/action/doSearch?AllField='+title+'&pageSize='+str(init_pgsize)+'&startPage=1'
        # acm_url = f"https://dl.acm.org/action/doSearch?AllField={title}&pageSize={init_pgsize}&startPage={pager_number}"
        # parse_acm(pager_number, acm_url)

        # sd_url = 'https://www.sciencedirect.com/search?qs='+title+'&date=2022-2024'
        # parse_scienceDirect(init_pgsize, pager_number, sd_url, title)

        ieee_link = f'https://ieeexplore.ieee.org/search/searchresult.jsp?queryText={title}&highlight=true&returnType=SEARCH&matchPubs=true&ranges=2022_2024_Year&returnFacets=ALL&rowsPerPage=100&pageNumber=1'
        parseIEEE(pager_number, init_pgsize, ieee_link, title)
    end = timer()
    print(end-start)

if __name__ == '__main__':
    main()