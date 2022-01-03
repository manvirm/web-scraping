# Note: on gitbash, must run export PYTHONIOENCODING=utf-8 to avoid UnicodeEncodeError
# In this program we scrape http://quotes.toscrape.com for quotes 

import requests
from bs4 import BeautifulSoup
from time import sleep

base_url = "http://quotes.toscrape.com"
url="/page/1"
all_quotes=[]

#keep updating the url to go the next page
#to retrieve new quotes, until we have all quotes
while url:

    response = requests.get(f"{base_url}{url}")
    response.encoding = 'utf-8'
    print(f"Now scraping {base_url}{url}...")
    soup = BeautifulSoup(response.text, "html.parser")

    #extract html with class quote
    quotes = soup.find_all(class_="quote")

    #loop through all quotes and find class with text, which gives text of quote
    #do the same for author, and author about page link
    for quote in quotes:
        all_quotes.append({
            "text": quote.find(class_="text").get_text(),
            "author": quote.find(class_="author").get_text(),
            "about-link": quote.find("a")["href"]
        })

    #find the next button to go to next page
    next_btn = soup.find(class_="next")

    #update url (next page), if no next page then break loop
    if next_btn:
        url = next_btn.find("a")["href"]
    else:
        url = None

    #take time in between scraping each page, wait 2 seconds before requesting again to avoid overloading the server
    sleep(2)

print(all_quotes)
    