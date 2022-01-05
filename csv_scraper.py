import requests
import random
from bs4 import BeautifulSoup
from time import sleep
from csv import DictWriter

base_url = "http://quotes.toscrape.com"

#retrieve quotes, the authors for the quotes, and authors about pages
def scrape_quotes():

    all_quotes=[]
    url="/page/1"

    #keep updating the url to go the next page
    #to retrieve new quotes, until we have all quotes
    while url:

        #parse html with beautifulsoup
        response = requests.get(f"{base_url}{url}")
        print(f"Now scraping {base_url}{url}...")
        soup = BeautifulSoup(response.text, "html.parser")

        #find all html with class quote
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
        
    return all_quotes


#write quotes to csv file so don't have to scrape every time
def write_quotes(quotes):

    with open("quotes.csv", "w", encoding="utf-8") as file:

        #set header in file
        headers = ["text", "author", "about-link"]
        csv_writer = DictWriter(file, fieldnames=headers)
        csv_writer.writeheader()

        #write quotes,author,author about link in rows
        for quote in quotes:
            csv_writer.writerow(quote)

quotes = scrape_quotes()
write_quotes(quotes)