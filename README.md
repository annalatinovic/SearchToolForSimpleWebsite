# COMP3011 Coursework 2

### Brief: Develop a search tool that finds web pages containing certain query phases in a website

In order to run the program, search.py must be ran. 

When search.py is ran, there are library messages that are printed, such as “[nltk_data] Downloading package stopwords to C:\Users\Anna.” These are from the nltk library. 

The following commands are: build, load, print [inputted word], find [query phase], and quit

---------------------------------------------------------------------------------------------------------------------------------------------------------------
### build

The build command crawls the website, builds the inverted index, and saves the inverted index into a file. 
As the build command is in progress, there will be print statements about: 
1. what website is being crawled -  " ... is being crawled right now."
2. when the website finishes crawling - "Finished crawling ..."
3. any errors that occur - "An error occurred crawling ... "
4. when a politeness window of 6 seconds is being observed - "Waiting 6 seconds."
5. when the politeness window of 6 seconds finishes - "Waited 6 seconds."
6. when the inverted index is being saved - "Saving the index file."
7. when the build command finishes crawling all the websites - "Finished web crawling all the links."

A 3 second wait happens before the index file is being saved.

*Note:* If there is a slight stall when building the inverted index, just let it continue on its own, or press "Enter" once

---------------------------------------------------------------------------------------------------------------------------------------------------------------
### load

The load command loads the index file from the file system. 
As the load command is in progress, there will be print statements about:
1. if the file does not exist in the file system - "The index file does not exist. The file needs to be built before loading."
2. if the file does exist - "The index file exists."

Example: load

The index file exists.

---------------------------------------------------------------------------------------------------------------------------------------------------------------
### print [word]

The print command prints the inverted index for the inputted [word].
As the print command is in progress, there will be print statements about:
1. if there is no inverted index for the command to use - "You need to load the index file first."
2. if the [word] does not exist in the inverted index - "[word] does not exist in the inverted index."
3. when it is printing the inverted index for the inputted word - "Printing inverted index for [word]."
4. the word's positions in the specified web page from the inverted index - "The word's positions in [word] are [word positions]."

Example: print creative

The word's positions in https://quotes.toscrape.com/author/Madeleine-LEngle are 211.

The word's positions in https://quotes.toscrape.com/author/Stephenie-Meyer are 201.

The word's positions in https://quotes.toscrape.com/author/Jim-Henson are 28.

---------------------------------------------------------------------------------------------------------------------------------------------------------------
### find [query phase]

The find command searches for a certain query phase in the inverted index and returns all pages containing the phrase. 
As the find command is in progress, there will be print statements about:
1. if there is no inverted index for the command to use - "You need to load the index file first."
2. if there are no results (web pages) from the query - "No query results for [query phase]
3. list of web pages that contain the query - "The following pages contain [query phase] ... "

Example: find nevertheless pretty childish

The following pages contain 'nevertheless pretty childish' consecutively:

https://quotes.toscrape.com/author/Albert-Einstein

No query results for nevertheless pretty childish scattered.

The following pages contain 'nevertheless pretty' consecutively:

https://quotes.toscrape.com/author/Albert-Einstein

The following pages contain 'pretty childish' consecutively:

https://quotes.toscrape.com/author/Albert-Einstein

**NOTE** When you look on the web page, you will see "...pretty childish." and then "Childish superstition:.." in the text. This query phase accounts for 'pretty childish' being farther apart, so 'childish' in "Childish superstition:..." is the word accounted for being farther apart. Since all the text is changed to be lowercase in the program, there isn't a difference between the two 'childish'.

No query results for nevertheless pretty scattered.


The following pages contain 'pretty childish' scattered:

https://quotes.toscrape.com/author/Albert-Einstein


The following pages contain 'nevertheless':

https://quotes.toscrape.com/author/Albert-Einstein

https://quotes.toscrape.com/author/E-E-Cummings


The following pages contain 'pretty':

https://quotes.toscrape.com/tag/inspirational/page/1/

https://quotes.toscrape.com/author/Albert-Einstein

https://quotes.toscrape.com/tag/life/page/1/

https://quotes.toscrape.com/tag/love/

https://quotes.toscrape.com/tag/life/

https://quotes.toscrape.com/page/2/

https://quotes.toscrape.com/tag/love/page/1/

https://quotes.toscrape.com/tag/friends/

https://quotes.toscrape.com/tag/inspirational/

https://quotes.toscrape.com/tag/sisters/page/1/

https://quotes.toscrape.com/tag/heartbreak/page/1/

https://quotes.toscrape.com/tag/friends/page/1/

https://quotes.toscrape.com/author/Stephenie-Meyer


The following pages contain 'childish':

https://quotes.toscrape.com/author/Albert-Einstein

---------------------------------------------------------------------------------------------------------------------------------------------------------------
### quit

The quit command terminates the search tool.
