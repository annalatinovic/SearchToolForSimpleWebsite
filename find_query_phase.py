from collections import Counter

class FindQueryPhase:
    def __init__(self, index_dict):
        # initializes the inverted index dictionary that was loaded in from the file
        self.index_dict = index_dict
        self.url_count_dict = {}

    # finds the query for one word
    def query_one_word(self, query_phase):
        word = query_phase[0]
        try:
            # indexes the inverted index dictionary with the inputted word 
            dict_keys = self.index_dict[word]
        except:
            # if the word does not exist in the inverted index, then an empty list is returned
            dict_keys = []

        # ranks the word occurences in the dictionary so web pages that have higher frequences of the word are ordered first
        word_occurence_ranking = sorted(dict_keys, key=lambda url: len(dict_keys[url]), reverse=True)
        
        return word_occurence_ranking

    # finds the query for two consecutive words
    def query_two_consecutive_words(self, query_phase):
        words = query_phase

        # an empty list to store urls that contain the query
        result_urls = []

        # an empty list to store the order of query phase frequencies in a web page
        # higher frequencies of the query phase in the web page appear first
        consecutive_word_ranking_lst = []

        # a dictionary to store positions of words in urls
        word_positions = {}

        # iterates through each word in the query
        for word in words:
            if word in self.index_dict:
                # if the term exists in index_dict, then retrieve the nested dictionary containing the urls and word positions
                url_list = self.index_dict[word]
                # loops through the key and value from the nested dictionary
                for url, positions in url_list.items():
                    # checks if the url was not already added to word_positions dictionary
                    if url not in word_positions:
                        word_positions[url] = {word: positions}
                    else:
                        word_positions[url][word] = positions

        # loops through the urls and checks for consecutive word positions
        for url, positions_dict in word_positions.items():
            positions_lists = list(positions_dict.values())
            # checks if there are consecutive positions for each word
            consecutive_positions = [sorted(positions) for positions in positions_lists]

            # loops through the word positions of the first word in the query phase
            for i in range(len(consecutive_positions[0])):
                # loops through the word positions of the second word in the query phase
                for second_term_index in range(1, len(consecutive_positions)):
                    # adds 1 to the current word's position from the first word (in the query phase) to see if the value exists in the list of the second word's word positions 
                    if (consecutive_positions[0][i] + 1 in consecutive_positions[second_term_index]):
                        result_urls.append(url)
        
        # uses the Counter function to create a dictionary where the key is the url and the value is the number of occurences the query phase appears
        url_counts = Counter(result_urls)
        # ranks the word occurences in the dictionary so web pages that have higher frequences of the query phase are printed ordered first
        consecutive_word_ranking_lst = sorted(url_counts, key=lambda url: url_counts[url], reverse=True)
        return consecutive_word_ranking_lst

    # finds the query for three consecutive words
    def query_three_consecutive_words(self, query_phase):
        words = query_phase

        # an empty list to store urls that contain the query
        result_urls = []

        # a dictionary to store positions of words in urls
        word_positions = {}

        # iterates through each word in the query
        for word in words:
            if word in self.index_dict:
                # if the term exists in index_dict, then retrieve the nested dictionary containing the urls and word positions
                url_list = self.index_dict[word]
                # loops through the key and value from the nested dictionary
                for url, positions in url_list.items():
                    # checks if the url was not already added to word_positions dictionary
                    if url not in word_positions:
                        word_positions[url] = {word: positions}
                    else:
                        word_positions[url][word] = positions
         
        # loops through the urls and checks for consecutive word positions
        for url, positions_dict in word_positions.items():
            positions_lists = list(positions_dict.values())
            # checks if there are consecutive positions for each word
            consecutive_positions = [sorted(positions) for positions in positions_lists]

            # loops through the word positions of the first word in the query phase
            for i in range(len(consecutive_positions[0])):
                # loops through the word positions of the second word in the query phase
                for second_term_index in range(1, len(consecutive_positions)):
                    # adds 1 to the current word's position from the first word (in the query phase) to see if the value exists in the list of the second word's word positions 
                    if (consecutive_positions[0][i] + 1 in consecutive_positions[second_term_index]) and (url not in result_urls):
                        # if the first two words in the query are consecutive, then it checks if the third word is after the second word in the web page
                        # loops through the word positions of the third word in the query phase
                        for third_term_index in range(2, len(consecutive_positions)):
                            # adds 1 to the current word's position from the second word (in the query phase) to see if the value exists in the list of the third word's word positions 
                            if (consecutive_positions[1][i] + 1 in consecutive_positions[third_term_index]):
                                # if there are consecutive words in the web page, then the url is added to the list of urls where all three words are consecutive
                                result_urls.append(url)
        
        # uses the Counter function to create a dictionary where the key is the url and the value is the number of occurences the query phase appears
        url_counts = Counter(result_urls)
        # ranks the word occurences in the dictionary so web pages that have higher frequences of the query phase are printed ordered first
        consecutive_word_ranking_lst = sorted(url_counts, key=lambda url: url_counts[url], reverse=True)
        return consecutive_word_ranking_lst
    
    def query_two_scattered_words(self, query_phase):
        scattered_word_dict = {}
        first_word = query_phase[0]
        second_word = query_phase[1]

        if first_word in self.index_dict and second_word in self.index_dict:
            url_lst = self.index_dict[first_word].keys()
            for url in url_lst:
                first_word_positions = self.index_dict[first_word].get(url, [])
                
                second_word_positions = self.index_dict[second_word].get(url, [])
            
                # checks if the first word comes before the second word in the document
                if first_word_positions and second_word_positions:
                    for pos_second in second_word_positions:
                        for pos_first in first_word_positions:
                            # checks if the first word comes before the second word and the difference is greater than 1
                            if (pos_first < pos_second) and ((pos_second - pos_first) > 1):
                                result = pos_second - pos_first
                                # adds to the dictionary containing the word position differences in the web pages
                                if url in scattered_word_dict.keys():
                                    differences = scattered_word_dict[url]
                                    differences.append(result)
                                    scattered_word_dict[url] = differences
                                else:
                                    scattered_word_dict[url] = [result]
        
        # ranks the word occurences in the dictionary so web pages that have higher frequences of the query phase are printed ordered first
        scattered_word_ranking_lst = sorted(scattered_word_dict, key=lambda url: scattered_word_dict[url], reverse=True)

        return scattered_word_ranking_lst
    
    def query_three_scattered_words(self, query_phase):
        scattered_word_dict = {}
        first_word = query_phase[0]
        second_word = query_phase[1]
        third_word = query_phase[2]

        if first_word in self.index_dict and second_word in self.index_dict and third_word in self.index_dict:
            url_lst = self.index_dict[first_word].keys()
            for url in url_lst:
                first_word_positions = self.index_dict[first_word].get(url, [])
                
                second_word_positions = self.index_dict[second_word].get(url, [])

                third_word_positions = self.index_dict[third_word].get(url, [])

            
                # checks if the first word comes before the second word in the document
                if first_word_positions and second_word_positions and third_word_positions:
                    for pos_third in third_word_positions:
                        for pos_second in second_word_positions:
                            for pos_first in first_word_positions:
                                # checks if the first word comes before the second word and the difference is greater than 1
                                if (pos_first < pos_second) and (pos_second - pos_first) > 1 and (pos_second < pos_third) and (pos_third-pos_second) > 1:
                                    result = pos_third - pos_second - pos_first
                                    # adds to the dictionary containing the word position differences in the web pages
                                    if url in scattered_word_dict.keys():
                                        differences = scattered_word_dict[url]
                                        differences.append(result)
                                        scattered_word_dict[url] = differences
                                    else:
                                        scattered_word_dict[url] = [result]
            
        # ranks the word occurences in the dictionary so web pages that have higher frequences of the query phase are printed ordered first
        scattered_word_ranking_lst = sorted(scattered_word_dict, key=lambda url: scattered_word_dict[url], reverse=True)

        return scattered_word_ranking_lst

    # creates the print statements for the queries
    def print_word_query_result(self, query_phase, query_result, consecutive = False, three_words = False, scattered = False):
        # prints messages stating that no queries were found, depending on the query phase
        # consecutive parameter is for query phases that are two consecutive words
        # three_words parameter is for query phases that are for triple consecutive words
        print("\n")
        if len(query_result) == 0 and consecutive == False and three_words == False and scattered == False:
            print("No query results for {}.".format(query_phase[0]))
        elif len(query_result) == 0 and consecutive == True:
            print("No query results for {} {} consecutively.".format(query_phase[0], query_phase[1]))
        elif len(query_result) == 0 and len(query_phase) == 2 and scattered == True:
            print("No query results for {} {} scattered.".format(query_phase[0], query_phase[1]))
        elif len(query_result) == 0 and three_words == True:
            print("No query results for {} {} {} consecutively.".format(query_phase[0], query_phase[1], query_phase[2]))
        elif len(query_result) == 0 and len(query_phase) == 3 and scattered == True:
            print("No query results for {} {} {} scattered.".format(query_phase[0], query_phase[1], query_phase[2]))
        else:
            # prints the query results depending on the query phase abd if the query phase is for consecutive words or not
            if len(query_phase) == 1:
                print("The following pages contain '{}':".format(query_phase[0]))
            elif len(query_phase) == 2 and consecutive == True:
                print("The following pages contain '{} {}' consecutively:".format(query_phase[0], query_phase[1]))
            elif len(query_phase) == 2 and scattered == True:
                print("The following pages contain '{} {}' scattered:".format(query_phase[0], query_phase[1]))
            elif len(query_phase) == 3 and three_words == True:
                print("The following pages contain '{} {} {}' consecutively:".format(query_phase[0], query_phase[1], query_phase[2]))
            elif len(query_phase) == 3 and scattered == True:
                print("The following pages contain '{} {} {}' scattered:".format(query_phase[0], query_phase[1], query_phase[2]))            
    
            for query in query_result:
                print(query)
                    
    # queries depending on the number of words
    def query(self, query_phase):
        # query for one word
        if len(query_phase) == 1:
            # queries and prints results for one word
            one_query_result = self.query_one_word(query_phase)
            self.print_word_query_result(query_phase, one_query_result)
        # query for two words
        elif len(query_phase) == 2:
            # queries and prints results for two consecutive words
            two_query_result = self.query_two_consecutive_words(query_phase)
            self.print_word_query_result(query_phase, two_query_result, consecutive=True)

            #queries and prints results for two scattered words
            two_scattered_query_result = self.query_two_scattered_words(query_phase)
            self.print_word_query_result(query_phase, two_scattered_query_result, scattered=True)

            # queries and prints results for the first word in the query phase
            first_word_query_result = self.query_one_word([query_phase[0]])
            self.print_word_query_result([query_phase[0]], first_word_query_result)

            # queries and prints results for the second word in the query phase
            second_word_query_result = self.query_one_word([query_phase[1]])
            self.print_word_query_result([query_phase[1]], second_word_query_result)
        # query for three words
        elif len(query_phase) == 3:
            # queries and prints results for three consecutive words
            three_query_result = self.query_three_consecutive_words(query_phase)
            self.print_word_query_result(query_phase, three_query_result, three_words = True)
            
            #queries and prints results for three scattered words
            three_scattered_query_result = self.query_three_scattered_words(query_phase)
            self.print_word_query_result(query_phase, three_scattered_query_result, scattered=True)

            # queries and prints results for first two consecutive words from the query phase
            first_two_query_result = self.query_two_consecutive_words(query_phase[0:2])
            self.print_word_query_result(query_phase[0:2], first_two_query_result, consecutive=True)

            # queries and prints results for last two consecutive words from the query phase
            second_two_query_result = self.query_two_consecutive_words(query_phase[1:len(query_phase)])
            self.print_word_query_result(query_phase[1:len(query_phase)], second_two_query_result, consecutive=True)

            # queries and prints results for the first two words scattered from the query phase
            first_two_scattered_query_result = self.query_two_scattered_words(query_phase[0:2])
            self.print_word_query_result(query_phase[0:2], first_two_scattered_query_result, scattered=True)

            # queries and prints results for the last two words scattered from the query phase
            second_two_scattered_query_result = self.query_two_scattered_words(query_phase[1:len(query_phase)])
            self.print_word_query_result(query_phase[1:len(query_phase)], second_two_scattered_query_result, scattered=True)

            # queries and prints results for the first word in the query phase
            first_word_query_result = self.query_one_word([query_phase[0]])
            self.print_word_query_result([query_phase[0]], first_word_query_result)

            # queries and prints results for the second word in the query phase
            second_word_query_result = self.query_one_word([query_phase[1]])
            self.print_word_query_result([query_phase[1]], second_word_query_result)

            # queries and prints results for the third word in the query phase
            third_word_query_result = self.query_one_word([query_phase[2]])
            self.print_word_query_result([query_phase[2]], third_word_query_result)       




