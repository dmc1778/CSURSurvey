from timeit import default_timer as timer
import csv, re, time, requests, sys, bs4, argparse, datetime
from selenium import webdriver 
from selenium.webdriver.common.by import By
driver=webdriver.Chrome()
from bs4 import BeautifulSoup as soup
now = datetime.datetime.now()
driver.get("https://www.facebook.com/")

def loadQuery():
  q = []
  with open("query.txt", "r") as f:
    q = [x.strip() for x in f.readlines()]
  return q


def parse_selenium_text(whole_text, keyword):
  new_list = []
  lo = whole_text.splitlines()
  ss = keyword.split('+')
  ss = '|'.join(ss)
  for item in lo:
    if re.search(r'('+ss+')', item):
        new_list.append([item, 'ScienceDirect'])
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

def findLink(results):
    meta_data = {'Link':'a', 'Rank': 0}
    for idx, item in enumerate(results):
        if hasattr(item, 'previous') and isinstance(item.previous, str):
            meta_data['Link'] = item.previous
            meta_data['Rank'] = idx
    return meta_data

def newWriter(paper_list, filename):
  result_file = open(filename+".csv",'a', newline='', encoding="utf-8")
  wr = csv.writer(result_file, dialect='excel')
  #wr.writerows([[item] for item in paper_list])
  wr.writerow([paper_list[0], paper_list[1]])

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

  myurl = 'https://www.sciencedirect.com/search?qs='+ keyword +'&date=2011-2024&offset='+ str(init_pgsize)
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
  bidy = driver.find_element(By.ID,'xplMainContent')
  a = bidy.find_element(By.TAG_NAME,'xpl-results-list')
  # time.sleep(5)
  # b = a.find_element(By.CLASS_NAME,'List-results-items')
  # title_ = b.find_element(By.CLASS_NAME, 'text-md-md-lh')

  res = parse_selenium_text(a.text, keyword, 'IEEEXplore')
  print(res)
  # llist.append([splited[0], splited[2]])

  # for item in llist:
  #   newWriter(item, 'IEEEpaperslist')

  myurl = 'https://ieeexplore.ieee.org/search/searchresult.jsp?queryText='+keyword+'&highlight=true&returnType=SEARCH&matchPubs=true&ranges=2010_2021_Year&returnFacets=ALL&rowsPerPage='+str(pgsize)+'&pageNumber='+str(pager_number)
  print('Analysis of page {} finished'.format(pager_number))
  print('Total number of papers extracted so far:', len(llist))
  pager_number += 1
  pgsize += 100
  parseIEEE(pager_number, pgsize, myurl, keyword)

def ScrapeACM(search_term, url, pager_number):
  print('I am analyzing this page:', pager_number)

  llist = []

  driver.get(url)

  time.sleep(2)
  mainContent = driver.find_element(By.ID,'pb-page-content')
  # searchContent = mainContent.find_element(By.CLASS_NAME,'search-result')
  searchXSLbody = mainContent.find_element(By.CLASS_NAME,'search-result__xsl-body')
  split_items = searchXSLbody.text.split('RESEARCH-ARTICLE')

  ss = search_term.split('+')
  ss = '|'.join(ss)
  
  for item in split_items:
    if item:
      item_split = item.split('\n')
      # for com in item_split:
        #if re.search(r'('+ss+')', com):
      result_file = open("ACMPaperList.csv",'a', newline='', encoding="utf-8")
      wr = csv.writer(result_file)
          #wr.writerows([[item] for item in paper_list])
      wr.writerow([item])
  pager_number += 1
  # url = f'https://dl.acm.org/action/doSearch?AllField={search_term}&pageSize=100&startPage={pager_number}'
  # ScrapeACM(search_term, url, pager_number)

  

def main():
    start = timer()
    pager_number = 1
    init_pgsize = 500

    # queries = queries.strip('[]').split(',')
    queries = loadQuery()
    start_date = 2011
    end_date = 2024
    queries = [
            # 'Vulnerability+detection',
            # 'Deep+Transfer+Learning+Vulnerability+Detection',
            # 'Software+vulnerability+detection',
            # 'Vulnerability+detection+using+deep+learning',
            # 'Source+code+security+bug+prediction',
            # 'Source+code+vulnerability+detection',
            # 'Source+code+bug+detection',
            'Vulnerability+detection+on+source+code+using+deep+learning'
    ]
    for title in queries:
        print(title)
        # _url = f'https://www.sciencedirect.com/search?qs={title}&date={start_date}-{end_date}'
        _url = f'https://www.sciencedirect.com/search?qs={title}&date=2011-2024&offset='+ str(init_pgsize)
        parse_scienceDirect(init_pgsize, pager_number, _url, title)

        #_url = f'https://ieeexplore.ieee.org/search/searchresult.jsp?queryText={title}&highlight=true&returnType=SEARCH&matchPubs=true&ranges={start_date}_{end_date}_Year&returnFacets=ALL&rowsPerPage={init_pgsize}&pageNumber={pager_number}'
        #ScrapeIEEEBS4(title, acm_url)

        # acm_url = f'https://dl.acm.org/action/doSearch?AllField={title}&pageSize={init_pgsize}&startPage=1'
        # ScrapeACM(title, acm_url, pager_number)
    end = timer()
    print(end-start)

if __name__ == '__main__':
    # Epilog = """An example usage: scrape.py --query="[llm, software]" --start_date=2015 --ending_date=2022"""
    # parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
    #         description='This program will automatically scrape sicenceDirect articles based on your custom queries.', epilog=Epilog)
    
    # parser.add_argument('--queries', required=True, type=str, help='List of your queries separated by spaces')
    # parser.add_argument('--start_date', default=2020 , type=int, help='Please specify a start date for article collection.')
    # parser.add_argument('--ending_date', default=now.year , type=int, help='Please specify an ending date for article collection.')
    # args = parser.parse_args()
    # if args.queries == None or args.start_date == None or args.ending_date == None:
    #     parser.print_help()
    #     sys.exit(-1)
    main()