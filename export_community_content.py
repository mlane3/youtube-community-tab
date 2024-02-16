#########
# Description
#  Uses undetected_chromedriver to scrape a YouTube channel's community tab.
#  It is recommended to use a VPN while running this code if you have one.
#
# Output
#  A single HTML file named _Community.html for the community tab page, and a separate HTML file for each post.
#  Each file is a complete community post with all comments and replies expanded.
#########

#########
# Packages
#########
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
import os
import time
import traceback
from pathlib import Path
import argparse

#########
# Methods
#########
def get_arguments():
  parser.add_argument("link", metavar="URL", type=str, help="URL of the YouTube Community page to export")
  parser.add_argument("--comments_newest_first", action="store_true", help="If set, comments will be sorted chronologically")
  parser.add_argument("-d", "--directory", type=str, help="Export path (defaults to current working directory)", default=os.getcwd())
  parser.add_argument("--low_resolution_images", action="store_true", help="If set, posts will be exported with the default image resolution instead of replacing images with a higher resolution version when available")
  parser.add_argument("--script_timeout", type=int, help="How many seconds to wait for scripts to run before throwing an exception (default 60 seconds)", default=300)
  parser.add_argument("--skip_existing", action="store_true", help="If set, pages that have already been exported to the target folder will be skipped, even if those pages have changed since the last export; the community page will always be exported, replacing the old file if it exists")
  parser.add_argument("--timeout", type=int, help="How many seconds to wait for a page to load before timing out and retrying (default 60 seconds)", default=60)
  return parser.parse_args()

def try_execute_script(driver, script):
  try:
    return driver.execute_script(script)
  except:
    return None

def try_execute_async_script(driver, script):
  try:
    return driver.execute_async_script(script)
  except:
    return None

def try_get_page(driver, url):
  failCount = 0
  while True:
    try:
      driver.get(url)
      return True
    except TimeoutException:
      failCount += 1
      if failCount >= 3:
        input("  Failed to load page (TimeoutException) after 3 attempts, press Enter to continue retrying.")
        failCount = 0
      else:
        print("  Failed to load page (TimeoutException), retrying...")
      pass
  return False

def save_current_page(driver, filepath):
    # Remove personal info from the page
    try_execute_script(driver, "document.getElementById('masthead-container').remove();")
    try_execute_script(driver, "document.querySelector('tp-yt-app-drawer').remove();")
    try_execute_script(driver, "document.querySelectorAll('ytd-comments-header-renderer [id=\"simple-box\"]').forEach(e => e.remove());")
    # Convert container from fixed width to relative width so the exported page isn't locked to the current window size of the browser
    try_execute_script(driver, "document.querySelector('ytd-page-manager').style.margin = '0';")
    try_execute_script(driver, "document.querySelector('ytd-two-column-browse-results-renderer').style.setProperty('width', '90%', 'important');")
    # Save the HTML file
    htmlcontent = driver.execute_script("const { content, title, filename } = await singlefile.getPageData({ removeHiddenElements: true, removeUnusedStyles: true, removeUnusedFonts: true, removeImports: true, blockScripts: true, blockAudios: true, blockVideos: true, compressHTML: true, removeAlternativeFonts: true, removeAlternativeMedias: true, removeAlternativeImages: true, groupDuplicateImages: true }); return content;")
    htmlcontent = htmlcontent.replace('http://asdf.replacethislater.com', '.')
    with open(filepath, 'w', encoding="utf8") as outputfile:
      outputfile.write(htmlcontent)

def current_scroll_position(driver):
  return driver.execute_script("return Math.ceil(window.innerHeight + window.pageYOffset);")

def is_bottom_of_page(driver):
  return driver.execute_script("return Math.ceil(window.innerHeight + window.pageYOffset) >= (document.querySelector('body > ytd-app').offsetHeight - 1);")

def scroll_to_more_content(driver):
  return driver.execute_script("var e = document.querySelector('div[id=\"primary\"]>ytd-section-list-renderer ytd-continuation-item-renderer'); if(e != null) { e.scrollIntoView(true); return true; } else { return false; }")

def scroll_full_page(driver):
  # Scroll to top of page first
  driver.find_element(By.TAG_NAME, "html").send_keys(Keys.HOME)
  time.sleep(0.5)
  # Now keep sending Page Down until the bottom of the page is reached
  while not is_bottom_of_page(driver):
    driver.find_element(By.TAG_NAME, "html").send_keys(Keys.PAGE_DOWN)
    time.sleep(0.1)

def scroll_to_bottom_of_content(driver):
  # Check for a rare edge case where the page doesn't load at all; if that happens, refresh the page and check again
  retryCount = 0
  while driver.execute_script("return document.querySelector('div[id=\"contents\"]') == null;"):
    print("  Page load appears to have failed, refreshing...")
    driver.refresh()
    retryCount += 1
    time.sleep(5 * retryCount)
  
  tries = 0
  stuckCount = 0
  lastPos = 0
  while tries < 10:
    # First click any buttons that load more content
    try_execute_script(driver, "document.querySelectorAll(\"[id='more'], [id='more-replies'], button[aria-label='Show more replies']\").forEach(e => e.click());")
    time.sleep(0.25)
    # Now try scrolling to the next continuation element to start loading it
    if scroll_to_more_content(driver):
      # In some edge cases scroll_to_more_content will get stuck; if the scroll position hasn't changed for a few seconds, manually scroll the entire page to try to force elements to load
      scrollPos = current_scroll_position(driver)
      if scrollPos == lastPos:
        stuckCount += 1
        if stuckCount > 5:
          scroll_full_page(driver)
          stuckCount = 0
      else:
        stuckCount = 0
      tries = 0
    else:
      # If no continuation elements were found, just scroll to the end of the page
      driver.find_element(By.TAG_NAME, "html").send_keys(Keys.END)
      tries += 1
    time.sleep(0.25)
  
  # Split image albums to ensure that all images are displayed
  try_execute_script(driver, "document.querySelectorAll('#items.ytd-post-multi-image-renderer').forEach(e => { e.style.whiteSpace = 'initial'; e.style.width = '100%'; }); var first = true; document.querySelectorAll('#items.ytd-post-multi-image-renderer #image-container').forEach(e => { if(first) { first = false; } else { e.style.marginTop = '10px'; } }); document.querySelectorAll('ytd-post-multi-image-renderer .arrow-container').forEach(e => { e.remove(); }); document.querySelectorAll('ytd-post-multi-image-renderer #image-icon-container').forEach(e => { e.remove(); });");
  
  # One final pass scrolling from top to bottom; this ensures that all elements have been in view at least once, otherwise some elements such as profile pictures may not be loaded
  scroll_full_page(driver)
  time.sleep(0.5)

def get_posts(communitypage):
  options = uc.ChromeOptions()
  
  # Add arguments that might help to avoid renderer timeout bugs
  options.add_argument("--disable-browser-side-navigation")
  options.add_argument("--disable-gpu")
  
  # Load the Chrome driver
  driver = uc.Chrome(options=options,seleniumwire_options={})
  driver.set_page_load_timeout(args.timeout)
  driver.set_script_timeout(args.script_timeout)
  
  # Maximize the browser window before starting so pages are exported at the correct size
  driver.maximize_window()
  
  # Wait for user to login
  try_get_page(driver, "https://youtube.com")
  time.sleep(1)
  input('Please log in to YouTube before continuing if you want membership content to be included in the exports. Press Enter to start exporting.')
  
  # Make sure the export directory exists
  os.makedirs(download_path, exist_ok=True)
  
  # Set SingleFile scripts to load every time a new page is loaded
  driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', { 'source': Path("single-file-bootstrap.js").read_text(encoding="utf8") });
  driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', { 'source': Path("single-file.js").read_text(encoding="utf8") });
  
  # Get all post links
  print("Loading community page: " + communitypage)
  try_get_page(driver, communitypage)
  time.sleep(5)
  scroll_to_bottom_of_content(driver)
  time.sleep(3)
  # Search the page for all published time texts, then return a list of all of the posts they link to
  # While doing this, also replace all links to the posts with something that can easily be found in the exported HTML; this allows replacing them with local links to the individual post files
  posts = driver.execute_script("var posts = []; document.querySelectorAll('ytd-backstage-post-thread-renderer #published-time-text>a').forEach(e => { posts.push(e.href); var newLink = e.href.replace('https://www.youtube.com/post', 'http://asdf.replacethislater.com') + '.html'; var oldLink = e.href.replace('https://www.youtube.com', ''); document.querySelectorAll('[href=\"' + oldLink + '\"]').forEach(link => link.href = newLink); }); return posts;")
  # Scroll back to the top of the page to keep the header in place
  driver.find_element(By.TAG_NAME, "html").send_keys(Keys.HOME)
  time.sleep(3)
  # Adjust the header to use a static position so it renders properly in the saved file
  try_execute_script(driver, "var header = document.querySelector('#wrapper.tp-yt-app-header-layout > [slot=header]'); header.style.position = 'static'; header.style.transform = 'initial'; document.querySelector('#wrapper.tp-yt-app-header-layout > #contentContainer').style.paddingTop = '0px';")
  # SingleFile for some reason exports this tag incorrectly, so replace it with a different tag name to prevent that (there isn't any relevant CSS, so the tag name shouldn't matter here)
  try_execute_script(driver, "while((e = document.querySelector('__slot-el')) != null) { var frag = document.createDocumentFragment(); while(e.firstChild) { frag.appendChild(e.firstChild); } var newElement = document.createElement('slot-el'); newElement.appendChild(frag); e.parentNode.replaceChild(newElement, e); }")
  time.sleep(1)
  # Save the main community tab
  save_current_page(driver, os.path.join(download_path, "_Community.html"))
  
  # Load and save all community posts
  pageCount = 0
  pagesSaved = 0
  pagesPerBatch = 10
  print("Found " + str(len(posts)) + " pages")
  for posturl in posts:
    filepath = os.path.join(download_path, posturl.split("/post/", 1)[1] + ".html")
    pageCount += 1
    
    if args.skip_existing:
      if os.path.isfile(filepath):
        print("Skipping page #" + str(pageCount) + ": " + posturl + " (already exists)")
        continue
    
    pagesSaved += 1
    # Switch to another page occasionally and wait for Chrome to free memory (workaround for a memory leak that eventually causes the browser tab to crash)
    if (pagesSaved % pagesPerBatch) == 0:
      print("Loading a temporary page and waiting for 60 seconds to allow memory to be cleaned up...")
      driver.get("https://www.google.com/")
      time.sleep(60)
    print("Loading page #" + str(pageCount) + ": " + posturl)
    try_get_page(driver, posturl)
    time.sleep(5)
    if driver.execute_script("if((e = document.getElementById('checkboxContainer')) != null) { e.click(); return true; } else { return false; }"):
      time.sleep(5)
    if args.comments_newest_first:
      try_execute_script(driver, "document.evaluate('//yt-dropdown-menu[@icon-label=\"Sort by\"]//a//div[contains(., \"Newest first\")]', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.closest('a').click();")
      time.sleep(3)
    scroll_to_bottom_of_content(driver)
    if not args.low_resolution_images:
      # Attempt to replace image source paths with the 8192px version; if it fails, revert the source back to the original
      if try_execute_async_script(driver, "var promises = []; var imageFound = false; async function TryLoadImage(imgElem, newSrc) { return new Promise(resolve => { var oldSrc = imgElem.src; if(oldSrc != newSrc) { var failed = false; imgElem.onload = () => { if(failed) { imgElem.src = oldSrc; } else { imageFound = true; } resolve(); }; imgElem.onerror = () => { failed = true; }; imgElem.src = newSrc; } else { resolve(); } }); } document.querySelectorAll('#primary #post #body #main #content-attachment img').forEach(e => { if(!e.src.includes('-fcrop')) { promises.push(TryLoadImage(e, e.src.replace(/=s[0-9]+-/, '=s8192-'))); } }); Promise.all(promises).then(() => { arguments[arguments.length - 1](imageFound); });"):
        time.sleep(3)
    save_current_page(driver, filepath)
  
  driver.quit()
  print(str(pagesSaved) + " page(s) have been exported.")

if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  args = get_arguments()
  download_path = args.directory
  get_posts(args.link)
