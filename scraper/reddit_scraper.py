import praw
import numpy as np


# Define the subreddits we want to look at
data_dir = '../data/'
data_file = 'subreddits.txt'

# Access reddit with praw
reddit = praw.Reddit('ConspiracyCorpusScraper')


# Iterate over subreddits
https://wiki.haskell.org/Xmonad/Config_archive/John_Goerzen%27s_Configuration#Customizing_xmonad
with open(data_dir+data_file) as f:
    for subreddit_name in f:
        subreddit = reddit.subreddit(subreddit_name.strip()) 
        try:
            top_submissions = subreddit.top(limit=30)
        except:
            continue

        post_text = []
        for post in top_submissions:
            try:
               post_text.append(post.selftext) 
            except:
                continue
        print(post_text)
