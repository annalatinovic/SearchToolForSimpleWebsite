import requests 
import queue
import time
import numpy as np
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from bs4 import BeautifulSoup

from build_index import BuildIndex

nltk.download('stopwords')
nltk.download('punkt')

class WebCrawl:

    def __init__(self, initial_url):
        # initializes the first url
        self.initial_url = initial_url
        # creates the queue for all the urls that need to be visisted
        self.url_queue = queue.Queue()
        # adds the first url in url_queue
        self.url_queue.put(self.initial_url)
        # creates an empty list for all the visited urls when crawling the webpages
        self.visited_urls = []
        # initializes the class to build the index file
        self.index_file = BuildIndex()
        # initializes the stop words
        self.stop_words = set(stopwords.words('english'))
        # initializes a variable of all the potential punctuation
        self.punctuation = '!"#$%&()*+,./:;<=>?@[\]^_`{|}~'

    # retrieves the quotes inside the HTML tags that contain text
    def retrieve_text(self, tag_txt):
        txt = tag_txt.get_text()
        # removes the quotation marks from the text, depending on the type of quotation marks
        try: 
            # “ and ” are different from the regular keyboard quotation marks, so they are copied and pasted from the HTML code
            txt = txt.replace('“','')
            txt = txt.replace('”','')
        except:
            txt = txt.replace('"','')
            txt = txt.replace('"','') 
        finally:           
            # checks if there is a newline character in the text - this mostly applies for author descriptions
            if "\n" in txt:
                txt = txt.replace("\n","")
        return txt
    
    # filters each word
    def filter_words(self, word):
        # checks if the word is longer than 2 characters
        if len(word) <= 2:
            return None
        # checks if the word is a stop word
        elif "http:" in word:
            return None
        # checks if the word is a stopword
        elif word in self.stop_words:
            return None
        # checks if the word is just a hyphen
        elif word == "-":
            return None
        # checks if the characters are numbers
        elif word.isnumeric():
            return None
        # checks if there is a period in the word
        elif "." in word:
            # removes the period at the end
            if word.index(".") == len(word):
                return word[:-1]
            else:
                # splits the word into two by the period
                split_words = word.split(".")
                word_lst = []
                # iterates through each word from the split words
                for word in split_words:
                    # checks each letter in the word to see if it is a punctuation
                    for w in str(word):
                        # if the character is punctuation, then removes the punctuation
                        if w in self.punctuation and w != "'":
                            word = word.replace(w, '')
                    # checks if the word doesn't only contain letters, 2 characters or shorter, or it is a stop word
                    if not word.isalpha() or len(word) <= 2 or (word in self.stop_words):
                        word_lst.append("")
                    # returns the word if the word is longer than 2 characters and the word is not a stop word
                    elif len(word) > 2 and (word not in self.stop_words):
                        word_lst.append(word)
                # loops through the split words by period to return the words that are valid
                for w in word_lst:
                    if w != "":
                        return w
        else:
            # loops through the characters of the word to remove any punctuation
            for w in str(word):
                if w in self.punctuation and w != "'":
                    word = word.replace(w, '')
            # checks if the filtered word does not only contain letters
            if not word.isalpha():
                return None
            # checks if the word is longer than 2 characters and is not a stopword
            elif len(word) > 2 and (word not in self.stop_words):
                return word
            # checks if the word is shorter than 2 characters and is a stopword
            elif len(word) <= 2 or (word in self.stop_words):
                return None
        return word
    
    # a function that removes stopwords for quotes and author descriptions
    def remove_stopwords(self, text):
        filtered_words_lst = []
        # loops through the quotes
        for t in range(0, len(text)):
            # makes all the words lowercase
            line = text[t].lower()
            # tokenizes the string into individual words
            doc = nltk.WhitespaceTokenizer().tokenize(line)
            # filters the tokenized quotes for specific words
            filtered_stopwords = map(self.filter_words, doc)
            # removes 'None' in the lists of filtered words
            filtered_words = [w for w in list(filtered_stopwords) if w is not None]            
            # adds each list of tokenized and filtered words to the main list of all the quotes or author description from the current webpage
            filtered_words_lst.append(filtered_words)
        return filtered_words_lst
    
    def build_index_dict(self, url, txt_lst, filtered_words_lst):
        # combines the list of text into one big text
        big_txt = ' '.join(txt_lst)
        # makes all the words to be lowercase
        big_txt = big_txt.lower()
        # creates a list of words by splitting the big text
        doc = re.findall(r"\b\w+(?:'\w+)?\b", big_txt)   
        # loops through the initial filtered words to retrieve 
        for i in range(0, len(filtered_words_lst)):
            lst_words = filtered_words_lst[i]
            for word in lst_words:
                if word != '' or len(word) > 2:
                    doc_lst = [d for d in doc if d != ' ']
                    # word_position = doc_lst.index(word, 0, len(doc_lst))
                    word_positions = [index for (index, item) in enumerate(doc_lst) if item == word]

                    self.index_file.build_dict(word, url, word_positions)
    
    # filters for hypertext reference in the domain
    def filter_links(self, element):
        link = element.get('href')
        if "https://www." in link:
            return False
        else:
            return True

    # retrieves the hypertext reference from the HTML code and creates the full url 
    def create_url(self, filtered_link):
        link = filtered_link.get('href')
        url = self.initial_url[:-1] + link
        return url
    
    # filters for any duplicates, such as cases where https://quotes.toscrape.com/tag/choices/page/1/ (longer url)
    # and https://quotes.toscrape.com/tag/choices/ (shorter url) are not both added to the queue list
    # both these urls are the same web page
    def filter_duplicates(self, queue_lst, url):
        # searchs for page/1/ in the current url
        page_one = re.findall("^.*(?=(page\/1\/))", url)
        # checks if the current url is in the queue list
        if url in queue_lst:
            return False
        # checks if the current url is the longer url and the shorter url is in the queue list 
        elif len(page_one) == 1 and url[:-7] in queue_lst:
            return False
        # checks if the current url is the longer url and the shorter url is not in the queue list 
        elif len(page_one) == 1 and url[:-7] not in queue_lst:
            return True
        # checks if the current url is the shorter url and the longer url is in the queue list
        elif len(page_one) != 1 and (url + "page/1/") in queue_lst:
            return False
        # checks if the current url is the shorter url and the longer url is not in the queue list
        elif len(page_one) != 1 and (url + "page/1/") not in queue_lst:
            return True        
        # checks if the current url is in the visited url list
        elif url in self.visited_urls:
            return False
        else:
            return True
    
    def search_and_add_links(self, links):
        # filters for links in the domain
        filtered_links = filter(self.filter_links, list(links))
        # creates a list from the filtered object
        filtered_links_lst = list(filtered_links)
        # applies the domain of the initial url to the filtered links
        retrieved_urls = map(self.create_url, filtered_links_lst)
        # removes any duplicates in the list by using the set() function
        url_retrieved_links_set = set(retrieved_urls)                    
        # creates a list from all the current items in the queue
        url_queue_lst = list(self.url_queue.queue)

        # adds all the urls retrieved from the current web page to the queue
        _ = list(map(lambda x: self.url_queue.put(x) if (self.filter_duplicates(url_queue_lst, x) == True) else False, url_retrieved_links_set))        


    def crawl(self):
        # checks if the all the urls were visited by checking if the size is 0
        while self.url_queue.qsize() != 0:
            # retrieves the url in url_queue
            url = self.url_queue.get()
            # checks if the url was not already visited
            if url not in self.visited_urls: 
                try:
                    # sends a get request to the current url
                    response = requests.get(url)
                    # retrives the HTML code of the website
                    html_doc = response.text

                    print(url + " is being crawled right now.")

                    # initializes the BeautifulSoup class
                    soup = BeautifulSoup(html_doc, 'html.parser')
                    
                    # EXTRACTING WORDS 

                    # extracts all the HTML code with <span class="text".... since those contain the quotes
                    span_quote_lst = soup.find_all('span', class_='text')

                    # if the length is not 0 in this list, then the page is a quotes web page, otherwise, it is an author description web page
                    if len(span_quote_lst) != 0:
                        # extracts the quotes inside the span tags
                        quotes = map(self.retrieve_text, span_quote_lst)
                        quote_lst = list(quotes)
                        filtered_words = self.remove_stopwords(quote_lst)
                        
                        # builds the index file
                        filtered_words_lst = list(filtered_words)
                        build_index_word = self.build_index_dict(url, quote_lst, filtered_words_lst)
                    else:
                        # extracts all the HTML code with <div class="author-description".... since those contain the quotes
                        div_descrpt_lst = soup.find_all('div', class_='author-description')
                       
                        # extracts the quotes inside the span tags
                        descrpt_words = map(self.retrieve_text, div_descrpt_lst)
                        descrpt_word_lst = list(descrpt_words)
                        
                        # removes the stop words
                        filtered_words = self.remove_stopwords(descrpt_word_lst)
                        filtered_words_lst = list(filtered_words)
                        build_index_word = self.build_index_dict(url, descrpt_word_lst, filtered_words_lst)
 
                    # EXTRACTING LINKS

                    # finds all the tags that have 'a'
                    links = soup.find_all('a')
                    # filters the current web page's HTML code to find the next links for the web crawler
                    self.search_and_add_links(links)

                    # adds the current url to the list of visited urls
                    self.visited_urls.append(url)
                    print("Finished crawling " + url)
                except Exception as e:
                    print("An error occurred crawling " + url + ": " + str(e))
                finally:
                    print("Waiting 6 seconds.")
                    # observes a politness window of 6 seconds
                    time.sleep(6)
                    print("Waited 6 seconds.")
        
        time.sleep(3)
        print("Saving the index file.")
        # saves the index dictionary to a file
        self.index_file.build_index_file()
        print("Finished web crawling all the links.")
        




