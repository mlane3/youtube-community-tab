


## Based on the code found on this page
## https://www.reddit.com/r/webscraping/comments/153nqc2/is_there_a_python_library_to_scrape_twitter/
## run_both.bat

searchurl = 'https://nitter.net/PomuRainpuff/search?f=tweets&q=&since=2022-07-28&until=2024-10-22&near=Virtual+Neverland'
cutoff = 600 # because there are 443 days between the two dates
#cutoff = cutoff*3

from bs4 import BeautifulSoup
from selenium import webdriver
import time


# gives the cursor, for the next page
def add_next_cursor(my_url):
  driver.get(my_url)
  time.sleep(5)

  if count == 1:
    print("waiting")
    time.sleep(60)

  resp = driver.page_source
  soup = BeautifulSoup(resp, 'html.parser')

  show_more_divs = soup.find_all("div", {"class": "show-more"})
  if len(show_more_divs) >= 2:
    profile_header = show_more_divs[1]
    cursor = profile_header.find('a').get('href')
    return cursor
  else:
    profile_header = soup.find("div", {"class": "show-more"})
    cursor = profile_header.find('a').get('href')
  return cursor


if __name__ == "__main__":
  my_list = []
  my_url = searchurl #"https://nitter.net/"  # the URL of the profile that you want to extract the tweets of.
  my_list.append(my_url)
  checkpoint = True
  count = 1
  cursor = ""
  driver = webdriver.Chrome()
  while (checkpoint == True):
    try:
      cursor = add_next_cursor(my_url + cursor)
      my_list.append(my_url + cursor)
      print(f"Page no. {count} added! - ", my_url + cursor)
      count += 1
      if count >= cutoff:
        break
    except:
      print("Reached the end, ending the program…")
      checkpoint = False
  driver.close()

  my_list.pop()
  print(my_list)

  with open('output4.txt', 'w') as file:
    for string in my_list:
      file.write(string + '\n')

