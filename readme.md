
# Extreme Vtuber YouTube Community Tab Downloader

This repo is a fork of several repos especially a [bot-jonas/youtube-community-tab](https://github.com/bot-jonas/youtube-community-tab).  Those Source repos are listed below.
First the script a script to scrape and dump community tab posts as .json files, along with all attached images and thumbnails.

## Reference Repos
[bot-jonas/youtube-community-tab](https://github.com/bot-jonas/youtube-community-tab)


## Setup / Update

Since this version of the youtube-community-tab package is slightly modified, you will need to install/update it from this repo to guarantee compatibility.
Then you cd your way back up.
```sh
cd youtube-community-tab
pip install .
cd .. 
```

## Example Usage

```sh
python ytct.py --cookies cookies-youtube-com.txt -d "./Ninomae Ina_nis Ch. hololive-EN" https://www.youtube.com/channel/UCMwGHR0BTZuLsmjY_NT5Pwg/community
OR
./ytct.py --cookies cookies-youtube-com.txt -d "./Ninomae Ina_nis Ch. hololive-EN" https://www.youtube.com/@NinomaeInanis/community

python ytct.py --cookies youtube-cookies.txt -d "./YozoraMel" https://www.youtube.com/@YozoraMel/community

```

## Arguments

```
-h, --help                    show this help message and exit
--cookies COOKIES FILE        a Netscape format cookies file, allows the script to
                              retrieve Membership-only posts
-d, --directory DIRECTORY     save directory (defaults to current)
--post-archive FILE           download only posts not listed in the archive file
                              and record the IDs of newly downloaded posts
--dates                       write information about the post publish date
```
