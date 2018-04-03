# -*- coding: utf-8 -*-

import praw
from collections import Counter

class PopularWords(object):
    # A list of words scraped from post submissions and their respective comments
    words_list = []

    # A list of words / characters that will not be included in the words_list
    common_words_list = [
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
        'didnt', 'doesnt', 'yeah', 'only', 'many', 'things', 'around', 'here', 'want'
    ]

    time_filter_list = [
        'all', 'month', 'week', 'day'
    ]

    def __init__(self, reddit_client):
        self.reddit_client = reddit_client

    def scrape_titles(cls, subreddit_name, post_limit, top_time_filter):
        # Temporarily stores words for later content validation, 
        # e.g. needless characters like periods and commas, or words associated with the common_words_list
        temp_word_list = [] 

        if not isinstance(subreddit_name, str):
            raise ValueError('The subreddit name passed to PopularWords.scrape_titles is not a string.')

        if not isinstance(post_limit, int):
            raise ValueError('The post submission limit passed to PopularWords.scrape_titles is not an integer.')

        if top_time_filter not in cls.time_filter_list:
            raise ValueError('The time filter passed to PopularWords.scrape_titles is not acceptable. Please use `all`, `month`, `week`, or `day`')

        # Parse submissions and their respective comments. Add them to the temp_word_list for further validation
        for submission in reddit.subreddit(subreddit_name).top(time_filter=top_time_filter, limit=post_limit):
            # Split the titles of the posts into individual words
            temp_word_list.append(submission.title.split())
            # Grab top level and secondary comments
            submission.comments.replace_more(limit=0)
            for comment in submission.comments.list():
                # Split the comments into individual words
                temp_word_list.append(comment.body.split())

        for word_list in temp_word_list:
            for word in word_list:
                if "." in word:
                    word = word.replace(".", "")
                elif "'" in word:
                    word = word.replace("'", "")
                elif "," in word:
                    word = word.replace(",", "")

                # Check if the word is not a common word, and if it only has alpha characters
                if word.lower() not in cls.common_words_list:
                    if word.isalpha():
                        cls.words_list.append(word.lower())

    def count_words(cls, words_list, amt_typed):
        if not isinstance(words_list, list):
            raise ValueError('The words_list value passed to PopularWords.count_words is not a list.')

        if not isinstance(amt_typed, int):
            raise ValueError('The amt_typed value passed to PopularWords.count_words is not an integer.')

        word_count = Counter(words_list)
        for word in word_count:
            # If the words have been typed by users more than the amt_typed minimum, print it
            if word_count[word] > amt_typed:
                print (word + " | " + str(word_count[word])).encode('utf-8')
                
# Reddit client information
reddit = praw.Reddit(
    client_id = 'TVpfsnGcthb_Dw',
    client_secret = 'dCKQLTZgZIHDnCuze5__W0CtNdM',
    user_agent = 'popularwords:v0.0.1 (by /u/popularwords_bot)'
)

popularWords = PopularWords(reddit)

popularWords.scrape_titles('politics', 5, 'day')

popularWords.count_words(PopularWords.words_list, 90)