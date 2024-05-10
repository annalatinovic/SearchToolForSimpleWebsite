import json

class BuildIndex:
    def __init__(self):
        # initializes the index dictionary containing all the words
        self.index_dict = {}
        
    # checks if the word exists in the dictionary
    def word_exists(self, word):
        # retrieves all the keys in the from the index dictionary
        index_dict_keys = self.index_dict.keys()
        # checks if the word is in the dictionary
        if word in index_dict_keys:
            return True
        else:
            return False

    # builds that dictionary of all the words and its respective urls and positions
    def build_dict(self, word, url, positions_lst):
        url_dict = {}
        positions = []
        # checks if the dictionary is empty
        if len(self.index_dict) == 0:
            # creates the dictionary that contains the url as the key and the position as the respective value
            for p in positions_lst:
                positions.append(p)
            url_dict[url] = positions
            # creates the dictionary that contains the word as the key and the url_dict as the value  
            self.index_dict[word] = url_dict
        # checks if the word exists in the dictionary
        elif self.word_exists(word):
            # retrieves the values from the indexed word
            urls_dict = self.index_dict[word]
            # checks if the url is in the dictionary
            if url in urls_dict.keys():
                # retrieves all the word's position in the specified url
                positions_in_url = urls_dict[url]
                # checks if there are duplicate values, where the same word, url, and position exist in the dictionary
                for p in positions_lst:
                    # if the word's position from the parameter values does not exist in the web page's text, then it is added to the dictionary
                    if p not in positions_in_url:
                        positions_in_url.append(p)
                # sets the updated list of word positions to be the new value for the specified url in urls_dict
                urls_dict[url] = positions_in_url
            else:
                # adds all the positions to the list
                for p in positions_lst:
                    positions.append(p)
                # creates the urls_dict for the existing word but new url and adds it to the index_dict
                urls_dict[url] = positions
                # updates the index_dict with the urls_dict
                self.index_dict[word].update(urls_dict)
        elif not self.word_exists(word):
            # adds the word plus its url and position if the word doesn't already exist in the index_dict
            for p in positions_lst:
                positions.append(p)
            # creates the url_dict for the new word
            url_dict[url] = positions
            # sets the index_dict where the word is the key and the url_dict is the value 
            self.index_dict[word] = url_dict

    # builds the index file to be saved
    def build_index_file(self):
        outfile = open("index_file.json", "w")
        json.dump(self.index_dict, outfile)
        outfile.close()
