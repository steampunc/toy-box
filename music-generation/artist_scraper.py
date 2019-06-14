import subprocess
from pyquery import PyQuery as pq
import string
import time

artist_links = []

def ParseArtistLinks(html):
    parsed_html = pq(html)


    has_artists = False
    for a_link in parsed_html("span.KMjmU").items('a'):
        has_artists = True
        artist_links.append(a_link.attr("href"))
    return has_artists

reset_vpn_counter = 1
subprocess.call(["windscribe", "connect"])

urls_to_search = [char for char in string.ascii_lowercase] + ["0-9"]
for url_modifier in urls_to_search:
    has_artists = True
    i = 0
    while has_artists:
        url = 'https://www.ultimate-guitar.com/bands/'+ str(url_modifier) + str(i) + '.htm'
        print(url)

        subprocess.call(["node", "scraper.js", url ])

        with open("temp.html") as html_file:
            html = html_file.read()

        has_artists = ParseArtistLinks(html)
        print(has_artists)

        i += 1

        if (reset_vpn_counter % 25 == 0):
            subprocess.call(["windscribe", "disconnect"])
            subprocess.call(["windscribe", "connect"])

        reset_vpn_counter += 1

    with open("artist_links.txt", "w") as link_file:
        link_file.write(str(artist_links))

with open("artist_links.txt", "w") as artist_link_file:
    artist_link_file.write(str(artist_links))
