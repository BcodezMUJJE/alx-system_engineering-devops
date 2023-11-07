#!/usr/bin/python3
"""THE Recursive function that queries the Reddit API"""
import requests


def count_words(subreddit, word_list, after=None, counts=None):
    """this define a Reddit API word count"""
    if counts is None:
        counts = {}
    
    if not word_list:
        sorted_counts = sorted(counts.items(), key=lambda item: (-item[1], item[0]))
        for word, count in sorted_counts:
            print(f"{word.lower()}: {count}")
        return

    word = word_list[0]
    
    url = f"https://www.reddit.com/r/{subreddit}/hot.json?limit=100"
    
    headers = {
        'User-Agent': 'MyRedditBot/1.0'
    }

    params = {
        "after": after
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            data = response.json()
            if 'data' in data and 'children' in data['data']:
                posts = data['data']['children']
                for post in posts:
                    title = post['data']['title'].lower()
                    if f" {word.lower()} " in title or title.startswith(f"{word.lower()} ") or title.endswith(f" {word.lower()}") or title == word.lower():
                        counts[word.lower()] = counts.get(word.lower(), 0) + 1
                count_words(subreddit, word_list[1:], after=data['data']['after'], counts=counts)
            elif response.status_code == 302:
                print("Subreddit is not valid.")
            else:
                print("No posts found in this subreddit.")
        else:
            print(f"Error: Status code {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    subreddit_name = "learnpython"
    word_list = ["python", "java", "javascript"]
    count_words(subreddit_name, word_list)
