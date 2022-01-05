# Note: on gitbash, must run export PYTHONIOENCODING=utf-8 to avoid UnicodeEncodeError
# In this program we scrape http://quotes.toscrape.com for quotes 

import requests
import random
from bs4 import BeautifulSoup
from csv import DictReader

base_url = "http://quotes.toscrape.com"

#read quotes from csv file
def read_quotes(filename):
    with open(filename, "r", encoding="utf-8") as file:
        csv_reader = DictReader(file)
        #covert to list since we want list of dicts
        return list(csv_reader)

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

quotes = read_quotes("quotes.csv")
start_game(quotes)