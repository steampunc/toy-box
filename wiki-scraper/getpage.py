import os
import requests
import re

def Linkify(title):
    title = re.sub(' ', '_', title)
    return "/wiki/" + title

def Titleify(link):
    assert link.startswith("/wiki/")
    link = link[6:]
    return re.sub('_', ' ', link);

def GetTitleFromUrl(url):
    assert url.startswith("https://en.wikipedia.org")
    url = url[24:]
    return Titleify(url)

def Dehtml(string):
    return re.sub("<\s*[^>]*>", "", string)

def GetUrls(url):
    page = requests.get(url)
    sublist = page.text.split('<h1 id="firstHeading" class="firstHeading" lang="en">', 1)[1]
    title = sublist.split("</h1>")[0]
    if ("Special:Random" not in url and (Dehtml(title) != GetTitleFromUrl(url))):
        print("UH OH, PAGE SEEMS TO BE REDIRECT")
        print("SCANNING REDIRECTED PAGE INSTEAD")
        return
    contents = page.text.split('<div class="mw-parser-output">', 1)[1].split("<noscript>",1)[0]
    if '<span id="redirectsub">Redirect page</span>' in contents:
        print("UH OH, PAGE IS REDIRECT")
        return
    contents = re.sub('<table class="box.*<\/table>?', '', contents)
    links = re.findall('(\/wiki\/.*?)"', contents)

    print(contents)
    print(title)
    print(links)

GetUrls("https://en.wikipedia.org/wiki/Amine_Bermak")
#GetUrls("https://en.wikipedia.org/wiki/Special:Random")
