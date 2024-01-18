import re
from functools import lru_cache as cache
from requests_cache import requests
from django.utils.text import Truncator
from . import get_headers


#@cache(maxsize=128)
def get_forum_results(query):
    url = "https://forum.manjaro.org/"
    endpoint = f"{url}/search.json"

    response = requests.get(
        endpoint,
        params={
            "q": query,
            "order":  "latest",
            "status": "public",
            "in":     "title"
        }, timeout=20, headers=get_headers()
    )

    if response.ok:
        search_results = []
        response = response.json()
        try:
            topics = response["topics"]
            posts = response["posts"]
            for topic in topics:
                excluded_categories = [120]
                if topic["visible"] and topic["category_id"] not in excluded_categories:
                    count = topic["posts_count"] + topic["reply_count"]
                    topic_result = {
                        "url": f"{url}t/{topic['slug']}",
                        "title": re.sub("[\[].*?[\]]", "", topic["title"]),
                        "description": "",
                        "is_doc": False,
                        "type": "forum",
                        "activity": count,
                        "message": "unsolved"
                    }
                    if topic["tags"]:
                        tags = []
                        for tag in topic["tags"]:
                            tags.append(tag)

                        topic_result["tags"] = tags

                    announcements = [11, 19, 12, 15, 13, 18, 79, 80, 81, 102, 101, 112]

                    if topic["category_id"] == 40:  # tutorials
                        topic_result["is_doc"] = True
                        topic_result["message"] = "Tutorial"

                    elif topic["category_id"] in announcements:
                        topic_result["message"] = None
                    elif topic["has_accepted_answer"]:
                        topic_result["message"] = "solved"

                    if topic_result["message"] is None:
                        topic_result["message"] = "unsolved"

                    for post in posts:
                        if post["topic_id"] == topic["id"]:
                            topic_result["description"] = Truncator(post["blurb"]).chars(160)

                    search_results.append(topic_result)

        except KeyError:
            pass
 
        return tuple(search_results)
