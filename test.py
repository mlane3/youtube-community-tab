
cookie_jar_path = "youtube-cookies.txt"

# execute command for interactive is exec(open('test.py').read())
from selenium import webdriver
from selenium.webdriver.common.by import By
import re
import copy
import json
import time
import hashlib
import requests
from http import cookiejar
from selenium.webdriver.common.keys import Keys

driver = webdriver.Firefox()

#from http import cookiejar
#cookie_jar = cookiejar.MozillaCookieJar(cookie_jar_path)


##put in main
#parser = argparse.ArgumentParser()
#args = get_arguments()