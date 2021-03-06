# Note: on gitbash, must run export PYTHONIOENCODING=utf-8 to avoid UnicodeEncodeError
# In this program we scrape http://quotes.toscrape.com for quotes 

import requests
import random
from bs4 import BeautifulSoup
from time import sleep

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

#print hint after each incorrect guess
def print_hint(attempts, author, about):
    #find author birthday and birthplace and display it as hint
    if(attempts == 3):
        res = requests.get(f"{base_url}{about}")
        soup = BeautifulSoup(res.text, "html.parser")
        birth_date = soup.find(class_="author-born-date").get_text()
        birth_location = soup.find(class_="author-born-location").get_text()
        print(f"Hint #1: This author was born on {birth_date} {birth_location}")

    #display first name initial as hint
    elif(attempts == 2):
        print(f"Hint #2: The author's first name starts with {author[0]}")

    #display last name initial as hint (since name is in the form Manvir Mann, we can use split)
    elif(attempts == 1):
        last_initial = author.split(" ")[1][0]
        print(f"Hint #3: The author's last name starts with {last_initial}")

def start_game(all_quotes):

    #get random quote from dict
    num = random.randrange(0, len(all_quotes)-1)
    quote = all_quotes[num].get('text')
    author = all_quotes[num].get('author')
    about = all_quotes[num].get('about-link')

    #promp question to user
    answer = input(f"Guess the author of this quote {quote} (Attempts remaining: 4):\n")
    attempts = 3

    while answer.lower() != author.lower() and attempts > 0:

        print_hint(attempts, author, about)
        
        #promp question to user
        answer = input(f"Try again. Guess the author of this quote {quote} (Attempts remaining: {attempts}):\n")
        attempts -= 1
        
    #check if user answered correct or not
    if(answer.lower() == author.lower()):
        print(f"Congratulations! You are correct! (Answer: {author})")    
    else:
        print(f"Good try! The author was {author}")

    #ask user to play again
    again = ''
    while again not in ('y', 'yes', 'n', 'no'):
        again = input("Would you like to play again (y/n)? ")

    if again.lower() in ('yes', 'y'):
        print("Great, let's play again!")
        return start_game(all_quotes)
    else:
        print("Thanks for playing! Goodbye")

all_quotes = scrape_quotes()
start_game(all_quotes)