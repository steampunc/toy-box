import subprocess
from pyquery import PyQuery as pq
import os

def ParseSongURLs(html):
    song_urls = []
    parsed_html = pq(html)
    for a_link in parsed_html("span.evjXG").items('a'):
        song_urls.append(a_link.attr("href"))
    return song_urls


# filesystem will be song_links/artisturls
artist_links = []
with open("artist_links.txt", "r") as artisturls:
    artist_links = eval(artisturls.read())

for artist_link in artist_links:
    artist_file_name = artist_link.split("/")[2]
    if not os.path.exists("song_urls/" + artist_file_name.encode("utf-8")):
        song_urls = []
        while song_urls == []:
            with open("song_urls/" + artist_file_name.encode("utf-8"), "w") as artist_file:
                url = "https://www.ultimate-guitar.com" + artist_link
                subprocess.call(["node", "scraper.js", url ])

                html = ""
                with open("scraper_files/" + artist_file_name.encode("utf-8") + ".html") as html_file:
                    html = html_file.read()

                song_urls = ParseSongURLs(html)
                artist_file.write(str(song_urls))
                os.remove("scraper_files/" + artist_file_name.encode("utf-8") + ".html")


