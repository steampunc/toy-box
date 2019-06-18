from selenium import webdriver
import os
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec

profile = webdriver.FirefoxProfile()
desired_caps = webdriver.common.desired_capabilities.DesiredCapabilities().FIREFOX
profile.set_preference("permissions.default.image", 2)
desired_caps["pageLoadStrategy"] = "none"

driver = webdriver.Firefox(desired_capabilities=desired_caps, firefox_profile=profile)

def ScrapeForSongLinks(url):
    driver.get(url)
    time.sleep(2.5)
    url_elements = driver.find_elements_by_xpath("//span[@class='evjXG']/a")

    song_urls = []
    for url in url_elements:
        song_urls.append(url.get_attribute("href"))

    print(song_urls)
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
                artist_file.write(str(song_urls))
                num_tries += 1
            if num_tries > 1: 
                break

driver.quit()



