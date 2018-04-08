# -*- coding: utf-8 -*-

import praw
import time
import json
import sys
import time
from collections import Counter

version = 'v0.0.7'

class PopularWords(object):
    # A list of words / characters that will not be included in the validated_words_list
    time_filter_list = [
        'all', 'month', 'week', 'day'
    ]

    sort_methods_list = [
        'hot', 'top', 'controversial', 'new'
    ]

    def __init__(self, reddit_client):
        self.reddit_client = reddit_client
        # Contains words, and the associated sentences they're used in.
        self.word_sentence_dictionary = {}
        # A list of words scraped from post submissions and their respective comments
        self.validated_words_list = []
        # Temporarily holds words for later validation.
        self.temp_words_list = []
        
        self.finished_scraping_words = False

        self.submission_titles_list = []
        self.comment_bodies_list = []

        self.start_time = 0
        self.time_needed = 0

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


    def scrape_submissions(self, subreddit_name, sort_method, post_limit, sort_method_filter):
        if self.finished_scraping_words is False:
            # Temporarily stores words for later content validation, 
            # e.g. needless characters like periods and commas, or words associated with the common_words_list
            
            # Parse submissions and their respective comments. Add them to the temp_words_list for further validation
            if (sort_method == 'top'):
                for submission in reddit.subreddit(subreddit_name).top(time_filter=sort_method_filter, limit=post_limit):
                    self.submission_titles_list.append(submission.title.encode('utf-8'))
                    # Split the titles of the posts into individual words
                    self.temp_words_list.append(submission.title.split())
                    # Grab top level and secondary comments
                    submission.comments.replace_more(limit=0)
                    for comment in submission.comments.list():
                        self.comment_bodies_list.append(comment.body.encode('utf-8'))
                        # Split the comments into individual words
                        self.temp_words_list.append(comment.body.split())

            elif (sort_method == 'hot'):
                for submission in reddit.subreddit(subreddit_name).hot(limit=post_limit):
                    self.submission_titles_list.append(submission.title.encode('utf-8'))
                    self.temp_words_list.append(submission.title.split())
                    submission.comments.replace_more(limit=0)
                    sys.stdout.flush() 
                    for comment in submission.comments.list():
                        self.comment_bodies_list.append(comment.body.encode('utf-8'))
                        self.temp_words_list.append(comment.body.split())

            elif (sort_method == 'controversial'):
                for submission in reddit.subreddit(subreddit_name).controversial(time_filter=sort_method_filter, limit=post_limit):
                    self.submission_titles_list.append(submission.title.encode('utf-8'))
                    self.temp_words_list.append(submission.title.split())
                    submission.comments.replace_more(limit=0)
                    for comment in submission.comments.list():
                        self.comment_bodies_list.append(comment.body.encode('utf-8'))
                        self.temp_words_list.append(comment.body.split())
            
            elif (sort_method == 'new'):
                for submission in reddit.subreddit(subreddit_name).new(limit=post_limit):
                    self.submission_titles_list.append(submission.title.encode('utf-8'))
                    self.temp_words_list.append(submission.title.split())
                    submission.comments.replace_more(limit=0)
                    for comment in submission.comments.list():
                        self.comment_bodies_list.append(comment.body.encode('utf-8'))
                        self.temp_words_list.append(comment.body.split())

            print 'Temp word list completed. Passing words for validation...'
            self.start_time = time.time()
            for word_list in self.temp_words_list:
                time.clock()
                for word in word_list:
                    if "." in word:
                        word = word.replace(".", "")
                    elif "'" in word:
                        word = word.replace("'", "")
                    elif "," in word:
                        word = word.replace(",", "")

                    # Check if the word is not a common word, and if it only has alpha characters
                    if word.lower() not in self.common_words_list:
                        if word.isalpha():
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

                            self.time_needed = time.time() - self.start_time
                            sys.stdout.write("\r" + "- " + str(len(self.validated_words_list)) + " words validated in " + str(self.time_needed) + " seconds.")
                            sys.stdout.flush()
                        
            self.finished_scraping_words = True
            self.create_json_data(self.word_sentence_dictionary)

    def count_words(self, validated_words_list, amt_typed):
    
        if not isinstance(validated_words_list, list):
            raise ValueError('The validated_words_list value passed to PopularWords.count_words is not a list.')

        if not isinstance(amt_typed, int):
            raise ValueError('The amt_typed value passed to PopularWords.count_words is not an integer.')

        print 'Results: '
        word_count = Counter(validated_words_list)
        largest = max(word_count)
        print str(largest)
        for word in word_count:
            # If the words have been typed by users more than the amt_typed minimum, print it
            if word_count[word] > amt_typed:
                print (word + " | " + str(word_count[word])).encode('utf-8')

    def create_json_data(self, data):
        with open('word_data.txt', 'w') as outfile:
            json.dump(data, outfile)

    def setup(cls):
        print '### PopularWords '+version+' ###'

        subreddit_name = raw_input('Please enter a subreddit name: ').lower()
        if reddit.subreddits.search_by_name(subreddit_name, exact=True) == False:
            raise ValueError('The subreddit entered does not exist')
        if not isinstance(subreddit_name, str):
            raise ValueError('The subreddit name being passed to PopularWords.scrape_titles is not a string.')

        sort_method = raw_input('Please enter a sort method, e.g. `hot` or `top`: ').lower()
        if sort_method not in cls.sort_methods_list:
            raise ValueError('The sort method being passed to PopularWords.scrape_titles is not acceptable. Please use `hot`, `new`, `top`, or `controversial`')

        if sort_method == 'top' or sort_method == 'controversial':
            sort_method_filter = raw_input('Please enter the sort method filter you would like to use, e.g. `all`, `month`, etc.: ' ).lower()
            if sort_method_filter not in cls.time_filter_list:
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
        print 'Scraping posts...'
        popularWords.scrape_submissions(subreddit_name, sort_method, post_limit, sort_method_filter)
        print "\n"
        print 'Total words scraped: ' + str(len(popularWords.validated_words_list))

        amt_typed = input('Enter the minimum threshold for the number of times a word has been posted, this value must be at least 1: ')
        if not isinstance(amt_typed, int):
            raise ValueError('The minimum threshold being passed to PopularWords.count_words is not an integer.')
        if amt_typed <= 0:
            raise ValueError('The minimum threshold must be at least 1.')
        print 'Checking how many times each word has been said...'
        print

        popularWords.count_words(popularWords.validated_words_list, amt_typed)

# Reddit client information
reddit = praw.Reddit(
    client_id = 'TVpfsnGcthb_Dw',
    client_secret = 'dCKQLTZgZIHDnCuze5__W0CtNdM',
    user_agent = 'popularwords:'+version+'(by /u/popularwords_bot)'
)

print 'Initializing class...'
popularWords = PopularWords(reddit)
popularWords.setup()
                




