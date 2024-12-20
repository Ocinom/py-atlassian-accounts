from api.spaces import Spaces
import logging
import logging.config
import json
import api.api_handler

if __name__ == "__main__":
    ah = api.api_handler.ApiHandler(url="http://jsonplaceholder.typicode.com/posts/1")
    ah.add_queries({
        "hello": "world"
    })
    ah.get("", "Going into JSONPlaceholder...")
