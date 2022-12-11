# TamilYogi movie downloader

NOTE: This no longer works since Tamil Yogi has updated how they load movies!!! So archiving this project as of Dec 2022.

This is a python executable to download movies via TamilYogi links

Example:

```bash
python main.py http://tamilyogi.cool/imsai-arasan-23am-pulikesi-2006-tamil-movie-watch-online-dvdrip/
```

It will request you to select the available resolutions before downloading the file

## Install all the dependencies

```bash
pip install -r requirements.txt
```

 or

```bash
pip install -r requirements.txt --user
```

### Chromium Webdrivers

Chromium Webdriver for Chrome 87 is included in this repository.

If you are facing issues with the chromedriver.exe, then download the suitable chrome webdriver from below URL
[https://sites.google.com/a/chromium.org/chromedriver/downloads]

For other browser drivers
[https://selenium-python.readthedocs.io/installation.html#drivers]

### FFmpeg

~~You will need [FFmpeg](https://ffmpeg.org/) library to convet m3u8 to mp4 file format~~

1) ~~Download [FFmpeg](https://www.gyan.dev/ffmpeg/builds/packages/ffmpeg-4.3.1-2020-11-19-essentials_build.7z) here~~
2) ~~Extract the file using [7-zip utility](https://www.7-zip.org)~~
3) ~~Add the bin directory into your Environment Vairable PATH~~
