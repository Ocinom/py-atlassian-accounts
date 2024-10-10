from api.spaces import Spaces
import logging
import logging.config
import json
import api.api_handler

if __name__ == "__main__":
    # logging.config.fileConfig('logging.conf')
    # logger = logging.getLogger(__name__)
    # space = Spaces("mySpace", "mySpaceKey", "my Space description")
    # space.add_permissions("user",
    #                       "712020:091d5911-8e36-4bf7-8836-58eeaa93d31a",
    #                       69,
    #                       [
    #                           ("administer", "space"),
    #                           ("read", "space"),
    #                           ("delete", "space"),
    #                           ("export", "space"),
    #                           ("create", "page"),
    #                           ("archive", "page"),
    #                           ("delete", "page")
    #                       ])
    #
    # logger.info("Creating space 'mySpace'...")
    # response = space.create_space()
    # if response.status_code == 200:
    #     logger.debug("Space 'mySpace' successfully created.\nJSON response: "
    #                  f"{json.dumps(response.json(), indent=4)}")
    # else:
    #     logger.error(f"Space 'mySpace' failed to be created.\nJSON response:"
    #                  f"{json.dumps(response.json(), indent=4)}")
    #
    # logger.info("Deleting space 'mySpaceKey'...")
    # response = Spaces.delete_space("mySpaceKey")
    # if response.status_code == 202:
    #     logger.debug(f"Space 'mySpace' successfully deleted.\nJSON response: "
    #                  f"{json.dumps(response.json(), indent=4)}")
    # else:
    #     logger.error(f"Space 'mySpace' failed to be deleted.\nJSON response: "
    #                  f"{json.dumps(response.json(), indent=4)}")
    #
    # logger.info("main.py finished executing.")
    ah = api.api_handler.ApiHandler(url="http://date.jsontest.com")
    ah.add_queries({
        "hello": "world"
    })
    ah.get("", "Going into JSONTest...")
