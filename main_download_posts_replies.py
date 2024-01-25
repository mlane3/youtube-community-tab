
######
# Description:  Uses advanced webscraping methods prior to poetry etc. to webscrape.
# particularly selenium-wire and undetected_chromedriver. It is recommended if you have a VPN to
# turn it on while running this code. Because You can never be too careful.
# They will download based on the postid and in reverse chronological order.
######

# TO DO:
# I need to write instructions so a normal human who doesn't work for in Taxes can install this
# I need to convert a cookie jar to a simple dictionary or list.... so I can string import into the next package.

# python ytct.py --cookies youtube-cookies.txt -d "./Yao" https://www.youtube.com/@ShioriNovella/community
# ./ytct.py --cookies youtube-cookies.txt -d "./Ninomae Ina_nis Ch. hololive-EN" https://www.youtube.com/@NinomaeInanis/community

#########
# Output
########

""""
 Hundreds of html files that are saved to your "default folder".  Each file is a complete community
 post with all replies opened.  I have not figured out how to change the folder location.
 Its probably the standard selenium 4.0 methodology.
 It only downloads the first 60 seconds of posts (less than 10000)
"""

#########
# Input and Directions
#########

def main():
  """
  Step 1
  For BOTH community posts and memember only stream you will need to download your youtube cookies file.
  Just use this extension to get it:
    * https://chromewebstore.google.com/detail/get-cookiestxt-locally/cclelndahbckbenkjhflpdbgdldlbecc?pli=1
    * https://addons.mozilla.org/en-US/firefox/addon/cookies-txt/
    1) Login into Youtube.  If you don't want member only content then don't log into youtube.
    2) Click the extension.  Use NETSCAPE and .txt file format if the browser asks.
    3) Save as "youtube-cookies.txt in the github repo
  """
  cookie_jar_path = "youtube-cookies.txt"
  """
  Step 2 Install all the imported packages files after running this code below
  
  cd youtube-community-tab
  pip install .
  cd ..
  
  You may get an error about chrome driver being the wrong version.  Just change the number  below
  """

  version = 126

  """"
  Step 3 Get all community posts
    run the Hololive downloader using your code below
  
  python ytct.py --cookies youtube-cookies.txt -d "./YozoraMel" https://www.youtube.com/@YozoraMel/community
  """

  # Step 4 Change inputs for this file
  # Enter the profile name and change these variables.
  # Either change the directly to the location where you downloaded this git hub or make your own
  # chrome profile with require extensions
  # the profile is stored in the folder:  '%LOCALAPPDATA%\Google\Chrome\User Data' (search by date)
  # The profile name is what chrome names it in the above folder.  In my case it case called "Profile 7"

  fullpathlocationofprofile = 'D:/Github/youtube-community-tab/profiles'
  profilename = 'Profile 7'

  # Variables are set for YozoraMel
  savefolder = './YozoraMel'
  youtubecommunitypage = 'https://www.youtube.com/@YozoraMel/community'
  yt_handle = '@YozoraMel'
  smalllist = ['UgkxU64EHq6IHW8QFEyDFZdMTtcRc4NwZaed', 'Ugkx9nqwAp9R6jRDZ9kHILY3LymWvvGTPKQl']
  myurl = youtubecommunitypage

  """
  Step 6
  # run this file.
  """

  # smalllist = get_community(limit = 99999,savefolder)
  get_posts(fullpathlocationofprofile,profilename,myurl,smalllist)

#########
# Packages
#########

#from seleniumwire import webdriver
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
import re
import os
import time
from glob import glob
from http import cookiejar
import pyautogui

# Unused
import copy
import json
import sys
import hashlib
import requests
import urllib.parse as urlparse
from youtube_community_tab.requests_handler import requests_cache
from ytct import get_channel_id_from_handle
# sys.path.insert(1, 'youtube-community-posts-main')
# from yTposts import YT_Posts
# exec(open('main_download_posts_replies.py').read())

def get_community(limit,savefolder):
  # load all community posts
  mypath = os.path.join(savefolder + '/', "*.json")
  stuff = list(glob(mypath))
  smalllist = stuff[0:limit]
  smalllist = [re.sub(r'.json', '', file) for file in smalllist]
  smalllist = [re.sub(savefolder, '', file) for file in smalllist]
  smalllist = [re.sub('\\\\', '', file) for file in smalllist]
  return smalllist

def hold_W(key,hold_time,number,interval):
    start = time.time()
    while time.time() - start < hold_time:
      pyautogui.press(key)

def get_posts(fullpathlocationofprofile,profilename,myurl,smalllist):
  profilelocation = "--user-data-dir=" + fullpathlocationofprofile
  name = "--profile-directory=" + profilename
  # Define a custom user agent
  options = uc.ChromeOptions()
  options.add_argument(name)
  options.add_argument(profilelocation)
  my_user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36"
  options.add_argument(f"user-agent={my_user_agent}")
  driver = uc.Chrome(options=options,seleniumwire_options={},version_main=120)
  driver.get("https://youtube.com")
  time.sleep(1)
  waitforuser = input(
    'Please log into youtube.  The automation has difficulty bypassing the authenticators\n and I dont want to save peoples passwords.  Enter any word when you are done.'
  )
  waitforuseragain = input(
    'No really log into youtube. Make sure your download folder is set to what you wants. This will be using key commands. So besides closing python you will not be able to stop the app!'
  )
  driver.get(myurl)
  time.sleep(5)
  driver.switch_to.window(driver.current_window_handle)
  for postid in smalllist:
    communitypost = os.path.join('https://youtube.com/post/',postid)
    time.sleep(3)
    driver.get(communitypost)
    time.sleep(3)
    driver.switch_to.window(driver.current_window_handle)
    checkbox = driver.findelement(By.XPATH,'//*[@id="checkboxContainer"]')
    # hold the scroll key for 60 seconds
    driver.switch_to.window(driver.current_window_handle); hold_W('end', 60, 2, 1)
    driver.switch_to.window(driver.current_window_handle); pyautogui.hotkey('ctrl', 'shift', 'Y')
    time.sleep(40)
  driver.close()
  print("done")
"""
# Failed code
# this attempt to use the 
def get_posts_ascsv(yt_handle):
  from http import cookiejar
  cookie_jar_binary = cookiejar.MozillaCookieJar(cookie_jar_path)
  # cookie_jar = cookiejar.MozillaCookieJar(cookie_jar_path)
  # try:
  #   cookie_jar.load()
  #   print("ytct", f"loaded cookies from {cookie_jar_path}")
  # except FileNotFoundError:
  #   print("ytct", f"could not find cookies file {cookie_jar_path}, continuing without cookies...")
  # requests_cache.cookies = cookie_jar
  my_channel_id = get_channel_id_from_handle(yt_handle)
  yt = YT_Posts(cookie_jar)
  my_community_posts = yt.fetchPosts(my_channel_id, limit=2)
  single_community_post = yt.fetchPost(my_channel_id, my_community_posts[0]["postParams"])
  my_comments = yt.fetchComment(single_community_post["commentToken"], limit=999)
  replies_to_comment = yt.fetchComment(my_comments["comments"][0]["replyToken"], reply=True)

# Automating youtube login would require would me refactoring the extensions... 
# and people might not want because its harder to use
# so to be safer... I just have people manually login. :D
# That way you can solve your on capche's :D
def login_youtube(driver,username,password,my_url):
  driver.get(r'https://accounts.google.com/signin/v2/identifier?continue=' + \
             'https%3A%2F%2Fmail.google.com%2Fmail%2F&service=mail&sacu=1&rip=1' + \
             '&flowName=GlifWebSignIn&flowEntry = ServiceLogin')
  driver.implicitly_wait(10)
  loginBox = driver.find_element(By.XPATH,'//*[@id ="identifierId"]')
  loginBox.send_keys(username)
  driver.implicitly_wait(2)
  nextButton = driver.find_element(By.XPATH,'//*[@id ="identifierNext"]')
  nextButton[0].click()
  driver.implicitly_wait(2)
  passWordBox = driver.find_element(By.XPATH,'//*[@id ="password"]/div[1]/div / div[1]/input')
  passWordBox.send_keys(password)
  driver.implicitly_wait(2)
  nextButton = driver.find_elements_by_xpath('//*[@id ="passwordNext"]')
  nextButton[0].click()
"""

if __name__ == '__main__':
  main()

####
# small note: This is the same style of script the government uses to audit corporations when
#   they try to hide information during forensic investigations.
####