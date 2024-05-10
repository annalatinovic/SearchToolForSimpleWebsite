class LoadIndex:
    def __init__(self, word, index_file_dict):
        self.word = word
        self.index_file_dict = index_file_dict
        self.index_file_name = "index_file.json"

    # prints the inverted index for the specified word, if the word exists in the inverted index
    def retrieve_index(self):
        # retrieves all the keys in the index_file dictionary
        index_file_keys = self.index_file_dict.keys()
        # checks if the word exists in the inverted index
        if self.word not in index_file_keys:
            return "{} does not exist in the inverted index.".format(self.word)
        else:
            # finds the inverted index for the specified word
            word_dict = self.index_file_dict[self.word]
            return word_dict
        