import bs4
import codecs
from bs4 import BeautifulSoup as soup
import requests
from timeit import default_timer as timer
import time
import csv
import re
import json
from selenium import webdriver 
import random
driver=webdriver.Chrome()
from selenium.webdriver.common.by import By

def loadtxt():
  q = []
  with open("query.txt", "r") as f:
    q = [x.strip() for x in f.readlines()]
  return q

def jsonWriter(file, filename):
  with open(filename+'.json', 'a') as f:
      json.dump(file, f, ensure_ascii=False)

def newWriter(paper_list, filename):
  result_file = open(filename+".csv",'a', newline='', encoding="utf-8")
  wr = csv.writer(result_file, dialect='excel')
  wr.writerow([paper_list[0], paper_list[1]])

def write_to_csv(paper_list, filename):
  with open(filename+".csv", "a", newline="") as f:
      writer = csv.writer(f, delimiter='\n')
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

def parse_selenium_text(whole_text):
  new_list = []
  lo = whole_text.splitlines()
  for item in lo:
    if re.search(r'(vulnerability)', item):
      new_list.append([item, 'sciencedirect'])
  return new_list

def randomize_user_agent():
  user_agent_list = [
  'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15',
  'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
  'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
  'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0',
  'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
  ]

  for i in range(4):
    user_agent = random.choice(user_agent_list)
  
  headers = {'User-Agent': user_agent}
  return headers

def parseIEEE(pager_number, pgsize, init_url, keyword):
  print('I am analyzing this page:', pgsize)

  llist = []

  driver.get(init_url)

  time.sleep(2)
  # bidy = driver.find_element_by_class_name('main-section')
  # a = bidy.find_element_by_tag_name('xpl-results-list')
  # time.sleep(5)
  # b = a.find_elements_by_class_name('List-results-items')
  
  # bidy = driver.find_element(By.CLASS_NAME,'col')
  a = driver.find_element(By.ID,'xplMainContent')
  b = a.find_element(By.TAG_NAME,'xpl-results-list')
  #llist = parse_selenium_text(a.text)
  b = re.split(r'[\n\r]+', a.text)
  for item in b:
    if re.findall(r"(vulnerability|Vulnerability|bug|defect|detection|Detection)", item):
    #splited = item.text.split('\n')
      llist.append([item, 'IEEE'])

  for item in llist:
    newWriter(item, 'IEEEpaperslist')

  myurl = 'https://ieeexplore.ieee.org/search/searchresult.jsp?queryText='+keyword+'&highlight=true&returnType=SEARCH&matchPubs=true&ranges=2022_2024_Year&returnFacets=ALL&rowsPerPage='+str(pgsize)+'&pageNumber='+str(pager_number)
  print('Analysis of page {} finished'.format(pager_number))
  print('Total number of papers extracted so far:', len(llist))
  pager_number += 1
  # pgsize += 100
  parseIEEE(pager_number, pgsize, myurl, keyword)


def googleScholarScraper(pager_number, scholar_pgsize, init_url):
#   print('I am analyzing this page:', scholar_pgsize)
  current_header = randomize_user_agent()
  llist = []
  time.sleep(2)
  content = requests.get(init_url, headers=current_header)

  page_soup = soup(content.text, "html.parser")

  try:
    paper_list = page_soup.contents[1].contents[1].contents[0].contents[13].contents[1].contents[2].contents[1]
    for item in paper_list.contents:
      if isinstance(item, bs4.element.Tag):
        if len(item.contents) > 1:
          if len(item.contents[1].contents[0].contents) == 3:
            for i, sub_item in enumerate(item.contents[1].contents[0].contents[2].contents):
              if isinstance(sub_item, bs4.element.Tag):
                item.contents[1].contents[0].contents[2].contents[i] = sub_item.contents[0]
            _ttl = ' '.join(item.contents[1].contents[0].contents[2].contents)
            # print(_ttl)
            llist.append([_ttl, item.contents[1].contents[1].contents[-1]])
          else:
            if len(item.contents[1].contents[0].contents[0].contents) == 1:
              if isinstance(item.contents[1].contents[0].contents[0].contents[0], bs4.element.Tag):
                llist.append(item.contents[1].contents[0].contents[0].contents[0].contents[0])
                # print(item.contents[1].contents[0].contents[0].contents[0].contents[0])
              else:
                llist.append(item.contents[1].contents[0].contents[0].contents[0])
                # print(item.contents[1].contents[0].contents[0].contents[0])
            if len(item.contents[1].contents[0].contents[0].contents) > 1:
              for i, sub_item in enumerate(item.contents[1].contents[0].contents[0].contents):
                if isinstance(sub_item, bs4.element.Tag):
                  item.contents[1].contents[0].contents[0].contents[i] = sub_item.contents[0]
              _ttl = ' '.join(item.contents[1].contents[0].contents[0].contents)
              # print(_ttl)
              llist.append([_ttl, item.contents[1].contents[1].contents[- 1]])
              
    write_to_csv(llist, 'scholar3')

    # print('Analysis of page {} finished'.format(pager_number))
    # print('Total number of papers extracted so far:', len(paper_list))
  except Exception as e:
    print(e)
  pager_number += 1
  scholar_pgsize += 10

  next_page = 'https://scholar.google.com/scholar?start='+str(scholar_pgsize)+'&q=vulnerability+detection+on+source+code+using+deep+learning&hl=en&as_sdt=0,5&as_ylo=2010&as_yhi=2021'
  
  #time.sleep((130-5)*np.random.random()+5)
  googleScholarScraper(pager_number, scholar_pgsize, next_page)
      

def parse_scienceDirect(init_pgsize, pager_number, myurl, keyword):
  
  paper_list = []
  
  headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:63.0) Gecko/20100101 Firefox/63.0'}
 
  content = requests.get(myurl, headers=headers)
  driver.get(myurl)
  
  time.sleep(2)
  bidy = driver.find_element(By.CLASS_NAME, 'col-xs-24')
  # bidy = driver.find_elements_by_class_name('col-xs-24')
  a = bidy.find_element(By.ID, 'srp-results-list')
  b = a.find_element(By.CLASS_NAME, 'search-result-wrapper')
  #a = bidy.find_elements_by_id('srp-results-list')
  #b = a[0].find_element_by_class_name('search-result-wrapper')
  
  list = parse_selenium_text(b.text)

  for item in list:
    newWriter(item, 'scienceDirectPaperList')

  myurl = 'https://www.sciencedirect.com/search?qs='+ keyword +'&date=2010-2021&offset='+ str(init_pgsize)
  print('Analysis of page {} finished'.format(pager_number))
  print('Total number of papers extracted so far:', len(list))
  pager_number += 1
  init_pgsize += 100
  parse_scienceDirect(init_pgsize, pager_number, myurl, keyword)


def parse_acm(pager_number, myurl):
  paper_list = []
  content = requests.get(myurl)

  page_soup = soup(content.text, "html.parser")
 
  current_page = page_soup.contents[2].contents[2].contents[9].contents[1].contents[3].contents[1].contents[0].contents[1].contents[3].contents[3]
  # current_page = page_soup.contents[2].contents[2].contents[9].contents[1].contents[3].contents[1].contents[0].contents[1].contents[3].contents[1].contents
  if len(current_page) == 2:
    return None
  for item in current_page:
    if isinstance(item, bs4.element.Tag):
      if bool(item.attrs) == False:
        continue 
      if item.attrs['class'][0] == 'search__item':
        try:
          110
          # current_paper = item.contents[3].contents[3].contents[1].contents
          # raw_title_info = current_paper[1].contents[0].contents[0].contents
          # doi = current_paper[5].contents[0].attrs['href']
          # pub_place = current_paper[5].contents[0].attrs['title']
          title = item.contents[1].contents[1].contents[0].contents[0].text
          # title = parse_title(title)
          detail = item.contents[1].contents[1].contents[0].contents[2].text
          print(title)
          paper_list.append([title, detail])
        except:
          print('Parse Error!')

  write_to_csv(paper_list, 'ACMPaperList')

  if pager_number == 1:
    myurl = page_soup.contents[2].contents[2].contents[9].contents[1].contents[3].contents[1].contents[0].contents[1].contents[3].contents[4].contents[2].contents[0].attrs['href']
  else:
    myurl = page_soup.contents[2].contents[2].contents[9].contents[1].contents[3].contents[1].contents[0].contents[1].contents[3].contents[4].contents[2].contents[0].attrs['href']
  
  print('Analysis of page {} finished'.format(pager_number))
  print('Total number of papers extracted so far:', len(paper_list))
  pager_number += 1
  parse_acm(pager_number, myurl)

def parseIEEErecursive(pager_number, myurl):
  paper_list = []
  content = requests.get(myurl)

  page_soup = soup(content.text, "html.parser")
  current_page = page_soup.contents[2].contents[2].contents[9].contents[1].contents[3].contents[1].contents[0].contents[1].contents[3].contents[3]
  parseIEEErecursive()


def parseIEEEBs4(pageNumber, myurl):
  content = requests.get(myurl)

  page_soup = soup(content.text, "html.parser")
  print('')

def main():
  start = timer()
  pager_number = 1
  init_pgsize = 100
  scholar_pgsize = 450

  # queries = loadtxt()
  queries = [
            # 'Vulnerability+detection',
            'Deep+Transfer+Learning+Vulnerability+Detection',
            'Transfer+Learning+Software+Vulnerability+Detection',
            'Transfer+Learning+Software+Bug+Detection',
            # 'Software+vulnerability+detection',
            # 'Vulnerability+detection+using+deep+learning',
            # 'Source+code+security+bug+prediction',
            # 'Source+code+vulnerability+detection',
            # 'Source+code+bug+detection',
            # 'Vulnerability+detection+on+source+code+using+deep+learning'
    ]
  for title in queries:
    print(title)
    # init_url = 'https://scholar.google.com/scholar?q='+title+'&hl=en&as_sdt=0%2C5&as_ylo=2011&as_yhi=2024'
    # googleScholarScraper(pager_number, scholar_pgsize, init_url)

    # acm_url = 'https://dl.acm.org/action/doSearch?AllField='+title+'&pageSize=100&startPage=1'
    # parse_acm(pager_number, acm_url)

    # sd_url = 'https://www.sciencedirect.com/search?qs='+title+'&date=2010-2022'
    # parse_scienceDirect(init_pgsize, pager_number, sd_url, title)

    ieee_link = 'https://ieeexplore.ieee.org/search/searchresult.jsp?queryText='+title+'&highlight=true&returnType=SEARCH&matchPubs=true&ranges=2022_2024_Year&returnFacets=ALL&rowsPerPage=100&pageNumber=1'
    # parseIEEE(pager_number, init_pgsize, ieee_link, title)
    parseIEEEBs4(pager_number, ieee_link)
  end = timer()
  print(end-start)

if __name__ == '__main__':
    main()