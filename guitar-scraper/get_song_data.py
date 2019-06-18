import os
import requests
import re
import json
import math

def ScrapeForSongLinks(url):
    page = requests.get(url)
    json_file = json.loads(re.search("window.UGAPP.store.page =.*", page.text).group(0)[26:-1])["data"]
    num_pages = math.ceil(json_file["tabs_count"] / json_file["tabs_per_page"])

    song_urls = []

    for i in range(0, num_pages):
        page = requests.get(url + "?page=" + str(i+1))
        json_file = json.loads(re.search("window.UGAPP.store.page =.*", page.text).group(0)[26:-1])["data"]
        for tab in json_file["other_tabs"]:
            song_urls.append(tab["tab_url"])
    return song_urls

artist_links = []
with open("artist_links.txt", "r") as artisturls:
    artist_links = eval(artisturls.read())

for artist_link in artist_links:
    artist_file_name = artist_link.split("/")[2]
    if not os.path.exists("song_urls/" + artist_file_name):
        song_urls = []
        num_tries = 0
        while song_urls == []:
            with open("song_urls/" + artist_file_name, "w") as artist_file:
                url = "https://www.ultimate-guitar.com" + artist_link
                print(url)
                song_urls = ScrapeForSongLinks(url)
                print(song_urls)
                artist_file.write(str(song_urls))
                num_tries += 1
            if num_tries > 1: 
                print("Failed to scrape " + artist_file_name)
                break
