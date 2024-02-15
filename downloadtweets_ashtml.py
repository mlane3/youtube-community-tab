

from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import time
import pyautogui
import string



#url = "https://nitter.net/PomuRainpuff/search?f=tweets&q=&since=2021-05-15&until=2022-07-28&?f=tweets&since=2021-05-15&until=2022-07-28&cursor=DAADDAABCgABFYtcfZuWYAIKAAIViNDO6VYgAAAIAAIAAAACCAADAAAAAAgABAAAAAAKAAUYQyF6PAAnEAoABhhDIXo7_9jwAAA"
filepath = "outputmain.txt"

# https://stackoverflow.com/questions/53729201/save-complete-web-page-incl-css-images-using-python-selenium
def single_page(driver,singleurl,i):
  driver.get(singleurl)
  if i == 0:
    print("waiting")
    time.sleep(60)
  time.sleep(3)

  # open 'Save as...' to save html and assets
  try:
    elementdate = driver.find_element(By.XPATH,"(//*[contains(@class, 'tweet-date')])[1]/a")
    firstdate = elementdate.get_attribute("title")
    datestamp = firstdate.translate(str.maketrans('','',string.punctuation))
    pyautogui.hotkey('ctrl', 's')
    time.sleep(2)
    outfile = 'pomutwitter_a' + str(i) + datestamp
    # Save file
    pyautogui.typewrite(outfile + '.html')
    pyautogui.hotkey('enter')
    time.sleep(2)
  except:
    endpage = driver.find_element(By.XPATH, "//*[@class='timeline-end']")
    if endpage == 'No more items':
      sec = input('Pend of page found... contin?\n')
    else:
      print("function stops but there was noo errorlog")


def save_pages(filepath):
  # https://stackoverflow.com/questions/37395881/pandas-read-in-txt-file-without-headers
  files = pd.read_csv(filepath,
                      sep="|",  # or delim_whitespace=True, #separator is whitespace
                      header=None,  # no header
                      names=['file'])  # parse datetime
  driver = webdriver.Chrome()
  tempfiles = files.file

  for i in range(len(tempfiles)):
    print(i)
    singleurl = files.file[i]
    ci = i + 329
    print(singleurl)
    single_page(driver,singleurl,i)
    time.sleep(6)
  print("done")
print("next")

save_pages(filepath)
