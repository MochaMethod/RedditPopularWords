# -*- coding: utf-8 -*-

import praw
import time
import json
import sys
import time
from collections import Counter

#: str: Popular words current version.
version = 'v0.0.8'

class PopularWords(object):
    '''
    The PopularWords class scrapes submissions and comments from reddit, splits them into individual words,
    validates said words to weed out unwanted ones, counts how many times a given word was typed,
    and returns a JSON file with each word relating to the submissions and comments they were used in.
    '''
    def __init__(self):
        '''
        The __init__ method stores reddit client information, lists and dictionaries to store words,
        submissions and comments, timers to count how long processing takes, reddit filters and sort methods,
        and a list of common words to validate scraped words against.
        '''

        #: obj: Reddit user client information.
        self.reddit = praw.Reddit(
            client_id = 'TVpfsnGcthb_Dw',
            client_secret = 'dCKQLTZgZIHDnCuze5__W0CtNdM',
            user_agent = 'popularwords:'+version+'(by /u/popularwords_bot)'
        )

        #: Dictionary of str: Contains words, and the associated sentences they're used in.
        self.word_sentence_dictionary = {}
        
        #: List of str: A list of words scraped from post submissions and their respective comments.
        self.validated_words_list = []

        # List of str: Temporarily holds words for later validation.
        self.temp_words_list = []
        
        #: bool: Indicates whether or not submissions, comments, and individual words have scraped and validated.
        self.finished_scraping_words = False

        #: List of str: Stores scraped submission titles.
        self.submission_titles_list = []

        #: List of str: Stores scraped comment bodies.
        self.comment_bodies_list = []

        #: int: Tracks the start time of a scrape and validation.
        self.start_time = 0

        #: int: Tracks the time needed to scrape and validate.
        self.time_needed = 0

        #: List of str: Reddit time filters.
        self.time_filter_list = [
            'all', 'month', 'week', 'day'
        ]

        #: List of str: Reddit sort methods.
        self.sort_methods_list = [
            'hot', 'top', 'controversial', 'new'
        ]

        # List of str: A list of words / characters that will not be included in the validated_words_list.
        self.common_words_list = [
        'the', 'be', 'to', 'of', 'an', 'a', 'in', 'that', 'have',
        'i', 'is', 'it', 'for', 'not', 'on', 'with', 'as',
        'you', 'do', 'at', 'this', 'but', 'his', 'from', 'they',
        'we', 'say', 'or', 'will', 'all', 'would', 'there',
        'what', 'so', 'up', 'out', 'if', 'get', 'go', 'when', 'can', 
        'like', 'could', 'should', 'would', 'how', 'me', 'my', 'was', 'has',
        'who', 'are', 'too', 'got', 'had', 'and', '-', '&', 'our', 'your', 'their', 
        'about', 'than', 'by', 'more', '[removed]', '[deleted]', ':(', ':)',
        'did', 'id', '=', 'its', 'which', 'why', '>', 'into', 'just', '*', 'inst',
        'any', 'im', 'well', 'keep', 'very', 'were', 'werent', 'one', 'two', 'three', 'us',
        'cant', 'theyre', 'thing', 'need', 'then', 'them', 'through', 'threw', 'own',
        'didnt', 'doesnt', 'yeah', 'only', 'many', 'things', 'around', 'here', 'want', 'am', 'never', 
        'much', 'extra', 'use', 'last', 'no', 'yes', 'some', 'sure', 'last', 'bit', 'end',
        'good', 'big', 'thats', 'now', 'he', 'she', 'her', 'him', 'enough', 'first', 'said',
        'youre', 'dont', 'been', 'isnt', 'because', 'every', 'been', 'other', 'dont', 'same',
        'those', 'same', 'enough', 'same', 'long', 'off', 'wont', 'down', 'now', 'still', 
        'make', 'after', 'way', 'hes', 'really', 'way', 'make', 'see', 'these', 'new', 'even'
        'all' 'be'
    ]


    def scrape_reddit(self, subreddit_name, sort_method, post_limit, sort_method_filter):
        '''
        The scrape_reddit method scrapes submissions and comments from reddit.

        When scraping, one can choose what sort method to use, and the length of time to sort by, e.g. one month, one year, all time, etc.

        Args:
            subreddit_name (str): The name of a specific subreddit.
            sort_method (str): What to sort method to use for a specific subreddit.
            post_limit (int): The amount of posts to scrape.
            sort_method_filter (str): The timeframe of posts to scrape from.
        '''
        if self.finished_scraping_words is False:
            if (sort_method == 'top'):
                for submission in self.reddit.subreddit(subreddit_name).top(time_filter=sort_method_filter, limit=post_limit):
                    self.submission_titles_list.append(submission.title.encode('utf-8'))
                    # Split the titles of the posts into individual words.
                    self.temp_words_list.append(submission.title.split())
                    # Grab top level and secondary comments.
                    submission.comments.replace_more(limit=0)
                    for comment in submission.comments.list():
                        self.comment_bodies_list.append(comment.body.encode('utf-8'))
                        # Split the comments into individual words.
                        self.temp_words_list.append(comment.body.split())

            elif (sort_method == 'hot'):
                for submission in self.reddit.subreddit(subreddit_name).hot(limit=post_limit):
                    self.submission_titles_list.append(submission.title.encode('utf-8'))
                    self.temp_words_list.append(submission.title.split())
                    submission.comments.replace_more(limit=0)
                    sys.stdout.flush() 
                    for comment in submission.comments.list():
                        self.comment_bodies_list.append(comment.body.encode('utf-8'))
                        self.temp_words_list.append(comment.body.split())

            elif (sort_method == 'controversial'):
                for submission in self.reddit.subreddit(subreddit_name).controversial(time_filter=sort_method_filter, limit=post_limit):
                    self.submission_titles_list.append(submission.title.encode('utf-8'))
                    self.temp_words_list.append(submission.title.split())
                    submission.comments.replace_more(limit=0)
                    for comment in submission.comments.list():
                        self.comment_bodies_list.append(comment.body.encode('utf-8'))
                        self.temp_words_list.append(comment.body.split())
            
            elif (sort_method == 'new'):
                for submission in self.reddit.subreddit(subreddit_name).new(limit=post_limit):
                    self.submission_titles_list.append(submission.title.encode('utf-8'))
                    self.temp_words_list.append(submission.title.split())
                    submission.comments.replace_more(limit=0)
                    for comment in submission.comments.list():
                        self.comment_bodies_list.append(comment.body.encode('utf-8'))
                        self.temp_words_list.append(comment.body.split())

            self.word_validation(self.temp_words_list)

    def word_validation(self, temp_words_list):
        '''
        The word_validation method validates whether or not the words contain certain characters, or are apart of the common words list.

        Args:
            temp_words_list (list of str): A list of words being temporarily stored for validation.
        '''
        print 'Temp word list completed. Passing words for validation...'
        # Start time counter to track how long the scrape / validation will last.
        time.clock()
        self.start_time = time.time()
        for word_list in self.temp_words_list:
            # Remove common punctuation from words.
            for word in word_list:
                if "." in word:
                    word = word.replace(".", "")
                elif "'" in word:
                    word = word.replace("'", "")
                elif "," in word:
                    word = word.replace(",", "")

                # Check if the word is not a common word, and if it only has alpha characters.
                if word.lower() not in self.common_words_list:
                    if word.isalpha():
                        # Adds words from submission titles and comment bodies to a list that contains validated words.
                        self.validated_words_list.append(word.lower().encode('utf-8'))
                        for submission_title in self.submission_titles_list:
                            if word.lower().encode('utf-8') in submission_title:
                                if word.lower().encode('utf-8') not in self.word_sentence_dictionary:
                                    self.word_sentence_dictionary[word.lower().encode('utf-8')] = []
                                    self.word_sentence_dictionary[word.lower().encode('utf-8')].append(submission_title)
                                else:
                                    self.word_sentence_dictionary[word.lower().encode('utf-8')].append(submission_title)

                        for comment_body in self.comment_bodies_list:
                            if word.lower().encode('utf-8') in comment_body:
                                if word.lower().encode('utf-8') not in self.word_sentence_dictionary:
                                    self.word_sentence_dictionary[word.lower().encode('utf-8')] = []
                                    self.word_sentence_dictionary[word.lower().encode('utf-8')].append(comment_body)
                                else:
                                    self.word_sentence_dictionary[word.lower().encode('utf-8')].append(comment_body)

                    self.calculate_process_time()
                    
        self.finished_scraping_words = True
        self.create_json_data(self.word_sentence_dictionary)
    
    def calculate_process_time(self):
        '''
        The calculate_process_time variable calculates the time it took to perform the scrape and validation.
        '''
        self.time_needed = time.time() - self.start_time
        sys.stdout.write("\r" + "- " + str(len(self.validated_words_list)) + " words validated in " + str(self.time_needed) + " seconds.")
        sys.stdout.flush()

    def count_words(self, validated_words_list, amt_typed):
        '''
        The count_words method uses the Counter library to count the amount of times a certain word is used.

        Args:
            validated_words_list (list of str): A list containing words that have been validated through the word_validation method.
            amt_typed (int): A filter to display words mentioned 'n' amount of times.
        '''
        # Check if the validated_words_list parameter is a list.
        if not isinstance(validated_words_list, list):
            raise ValueError('The validated_words_list value passed to PopularWords.count_words is not a list.')

        # Check if the amt_typed parameter is an int.
        if not isinstance(amt_typed, int):
            raise ValueError('The amt_typed value passed to PopularWords.count_words is not an integer.')

        print 'Results: '
        word_count = Counter(validated_words_list)
        for word in word_count:
            # If the words have been typed by users more than the amt_typed minimum, print it.
            if word_count[word] > amt_typed:
                print (word + " | " + str(word_count[word])).encode('utf-8')

    def create_json_data(self, data):
        '''
        The create_json_data method takes in a list and exports it to a text file.

        Args:
            data (any type): A data set to be exported.
        '''
        # Open a text file and export data to it.
        with open('word_data.txt', 'w') as outfile:
            json.dump(data, outfile)

    def setup(self):
        '''
        The setup method gathers information via console to pass to the start_scrape method.
        '''
        print '### PopularWords '+version+' ###'

        # Gather a subreddit name, sorting method and its filter, and the amount of posts to scrape all through console input.
        subreddit_name = raw_input('Please enter a subreddit name: ').lower()
        if self.reddit.subreddits.search_by_name(subreddit_name, exact=True) == False:
            raise ValueError('The subreddit entered does not exist')
        if not isinstance(subreddit_name, str):
            raise ValueError('The subreddit name being passed to PopularWords.scrape_titles is not a string.')

        sort_method = raw_input('Please enter a sort method, e.g. `hot` or `top`: ').lower()
        if sort_method not in self.sort_methods_list:
            raise ValueError('The sort method being passed to PopularWords.scrape_titles is not acceptable. Please use `hot`, `new`, `top`, or `controversial`')

        if sort_method == 'top' or sort_method == 'controversial':
            sort_method_filter = raw_input('Please enter the sort method filter you would like to use, e.g. `all`, `month`, etc.: ' ).lower()
            if sort_method_filter not in self.time_filter_list:
                raise ValueError('The sort method filter being passed to PopularWords.scrape_titles is not acceptable. Please use `all`, `month`, `week`, or `day`')
        else:
            sort_method_filter = ''

        post_limit = input('Please enter the amount of submissions to scrape: ')
        if not isinstance(post_limit, int):
            raise ValueError('The post submission limit being passed to PopularWords.scrape_titles is not an integer.')
        if post_limit <= 0:
            raise ValueError('The minimum threshold for the post limit must be at least 1.')

        popularWords.start_scrape(subreddit_name, sort_method, post_limit, sort_method_filter)

    def start_scrape(self, subreddit_name, sort_method, post_limit, sort_method_filter):
        '''
        The start_scrape method takes in information from the setup method to decide which posts to scrape.

        Args:
            subreddit_name (str): The name of a specific subreddit.
            sort_method (str): What to sort method to use for a specific subreddit.
            post_limit (int): The amount of posts to scrape.
            sort_method_filter (str): The timeframe of posts to scrape from.
        '''
        print 'Scraping posts...'
        popularWords.scrape_reddit(subreddit_name, sort_method, post_limit, sort_method_filter)
        print "\n"
        print 'Total words scraped: ' + str(len(popularWords.validated_words_list))

        amt_typed = input('Enter the minimum threshold for the number of times a word has been posted, this value must be at least 1: ')
        # Check if the amt_typed paramter is an int.
        if not isinstance(amt_typed, int):
            raise ValueError('The minimum threshold being passed to PopularWords.count_words is not an integer.')
        # Check if the amt_typed paramater is zero or less.
        if amt_typed <= 0:
            raise ValueError('The minimum threshold must be at least 1.')
        print 'Checking how many times each word has been said...'
        print

        popularWords.count_words(popularWords.validated_words_list, amt_typed)

print 'Initializing...'
popularWords = PopularWords()
popularWords.setup()
                




