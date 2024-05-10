import os.path
import json
from web_crawl import WebCrawl
from load_index import LoadIndex
from find_query_phase import FindQueryPhase

# a list of all the commands
build = "build"
load = "load"
print_cmd = "print"
find = "find"

global data_dict
data_dict = {}

print("Please enter one of the following commands: build, load, print, find, or quit")
# takes in the first input
client_input = input().lower()

# checks that the input isn't quit to stop the command prompt
while client_input.lower() != "quit":
    # makes the input all lowercase
    client_input = client_input.lower()
    # splits apart the inputs by spaces
    commands = client_input.split()

    # checks if the command is build
    if build == commands[0]:
        # initilizes the BuildIndex class
        webpage = WebCrawl("https://quotes.toscrape.com/")
        # calling the function to crawl the webpage
        crawl = webpage.crawl()

    # checks if the command is load
    elif load == commands[0]:
        # checks if the index file exists
        if os.path.exists("index_file.json"):
            print('The index file exists.')
            # opens the index file
            f = open('index_file.json')
            # loads the index file
            data_dict = json.load(f)
        else: 
            print('The index file does not exist. The file needs to be built before loading.')
        
    # checks if the command is print
    elif print_cmd == commands[0]:
        # extracts the word from the command
        print_word = commands[1]
        print("\n")

        if len(data_dict) == 0:
            print("You need to load the index file first.")
        else:
            # initializes the LoadIndex class
            load_index = LoadIndex(print_word.lower(), data_dict)
            # calls the function to print the inverted index for the specificed word
            indexed_word = load_index.retrieve_index()

            # checks if a message stating that the inputted word does not exist
            if "does not exist in the inverted index" in indexed_word:
                print(indexed_word)
            else:
                # prints out the inverted index file
                print("Printing inverted index for " + print_word + ".")
                # retrieves the keys from the nested dictionary
                urls = indexed_word.keys()
                # loops through each url to print out the word's positions in that url
                for url in urls:
                    # retrieves the word's positions
                    word_positions = indexed_word[url]
                    # changes the int in the word positions to be str
                    word_positions_str = map(str, word_positions)
                    print("The word's positions in {} are {}.".format(url, (', ').join(word_positions_str)))

    # checks if the command is find
    elif find == commands[0]:
        query_phase = commands[1:]
        # checks if the inverted index file was loaded
        if len(data_dict) == 0:
            print("You need to load the index file first.")
        else:
            # initializes the FindQueryPhase class with the dictionary containing the inverted index
            find_query_phase = FindQueryPhase(data_dict)
            # calls the query function to list of all the pages containing the query phrase
            query_func = find_query_phase.query(query_phase)

    print("\n")
    print("Please enter one of the following commands: build, load, print, find, or quit")
    client_input = input()



