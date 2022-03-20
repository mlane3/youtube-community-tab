# YouTube Community Tab

This repo includes a fork of [bot-jonas/youtube-community-tab](https://github.com/bot-jonas/youtube-community-tab), as well as a script to scrape and dump community tab posts as .json files, along with all attached images and thumbnails.

## Setup

```sh
cd youtube-community-tab
pip install .
```

## Example Usage

```sh
python ytct.py --cookies cookies-youtube-com.txt -d "./Ninomae Ina_nis Ch. hololive-EN" https://www.youtube.com/channel/UCMwGHR0BTZuLsmjY_NT5Pwg/community
```

## Arguments

```
-h, --help                    show this help message and exit
--cookies COOKIES FILE        a Netscape format cookies file, allows the script to
                              retrieve Membership-only posts
-d, --directory DIRECTORY     save directory (defaults to current)
--write-viewer                copy the viewer file and create an index of downloaded
                              posts to be viewed (not yet complete)
--post-archive FILE           download only posts not listed in the archive file
                              and record the IDs of newly downloaded posts
--dates                       write as much information about the publishing date as
                              possible, as well as attempting to update dates for
                              prior posts based on new information (this feature is experimental and may not work                                 as intended)

```