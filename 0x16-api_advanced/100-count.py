#!/usr/bin/python3
"""This module queries the reddit API"""
import requests
from sys import argv


def recurse_count(subreddit, hot_list=[], after=None):
    """This function queries the reddit API recursively
    """
    url = "https://www.reddit.com/r/{}/hot.json".format(subreddit)
    payload = {"after": after, "limit": 100}
    headers = {"User-Agent": "Python/requests"}

    try:
        req = requests.get(url, headers=headers, params=payload,
                           allow_redirects=False)
        if req.status_code == 200:
            data = req.json()
            after = data.get("data")["after"]
            for post in data.get("data")["children"]:
                hot_list.append(post.get("data")["title"])
            if after:
                return recurse_count(subreddit, hot_list, after)
            else:
                return hot_list
        else:
            return None
    except requests.exceptions.JSONDecodeError:
        pass


def count_words(subreddit, word_list):
    """This function queries the reddit API and
    sorts a list of words by occurences
    """
    word_dict = {}

    all_titles = recurse_count(subreddit)
    word_list = [w.lower() for w in word_list]

    # Only parse responses that not None
    if all_titles:
        for word in word_list:
            count = 0
            for title in all_titles:

                # convert words to lowercase for comparison
                title = [w.lower() for w in title.split()]

                # Only count for present words in response
                if word in title:
                    for w in title:
                        if word == w:
                            count += 1
            # Only add words that are present to dictionary
            if count:

                """If a word is duplicated in the function parameter
                add all the occurrences
                """
                if word_dict.get(word):
                    count += word_dict[word]
                word_dict[word] = count
        sorted_dict = dict(sorted(word_dict.items(),
                           key=lambda item: item[1], reverse=True))
        for k, v in sorted_dict.items():
            print("{}: {:d}".format(k, v))#!/usr/bin/python3
"""Function to count words in all hot posts of a given Reddit subreddit."""
import requests


def count_words(subreddit, word_list, instances={}, after="", count=0):
    """Prints counts of given words found in hot posts of a given subreddit.

    Args:
        subreddit (str): The subreddit to search.
        word_list (list): The list of words to search for in post titles.
        instances (obj): Key/value pairs of words/counts.
        after (str): The parameter for the next page of the API results.
        count (int): The parameter of results matched thus far.
    """
    url = "https://www.reddit.com/r/{}/hot/.json".format(subreddit)
    headers = {
        "User-Agent": "linux:0x16.api.advanced:v1.0.0 (by /u/bdov_)"
    }
    params = {
        "after": after,
        "count": count,
        "limit": 100
    }
    response = requests.get(url, headers=headers, params=params,
                            allow_redirects=False)
    try:
        results = response.json()
        if response.status_code == 404:
            raise Exception
    except Exception:
        print("")
        return

    results = results.get("data")
    after = results.get("after")
    count += results.get("dist")
    for c in results.get("children"):
        title = c.get("data").get("title").lower().split()
        for word in word_list:
            if word.lower() in title:
                times = len([t for t in title if t == word.lower()])
                if instances.get(word) is None:
                    instances[word] = times
                else:
                    instances[word] += times

    if after is None:
        if len(instances) == 0:
            print("")
            return
        instances = sorted(instances.items(), key=lambda kv: (-kv[1], kv[0]))
        [print("{}: {}".format(k, v)) for k, v in instances]
    else:
        count_words(subreddit, word_list, instances, after, count)
