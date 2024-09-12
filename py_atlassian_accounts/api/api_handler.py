from typing import Callable
from functools import wraps
import requests
from requests import Response
from requests.auth import HTTPBasicAuth
import constants

import json
import logging
import logging.config


def pretty_json(my_json):
    return json.dumps(my_json, indent=4)


def log_api_call(func: Callable[..., Response]):
    """
    A decorator function that wraps api call functions and performs the following logs:
    INFO: API Call execution progress
    DEBUG: Request metadata and payload and response json
    """

    @wraps(func)
    def wrapper(self, endpoint="", desc="") -> Response:

        # Initialise/get logger
        logging.config.fileConfig('logging.conf')
        logger = logging.getLogger(__name__)

        # Log progress to info, and JSON details to debug, where they are stored in a file
        logger.info(desc if desc else "Performing API call...")
        logger.debug(f"Sending {func.__name__.upper()} request to {self.url}"
                     f"\nwith queries {pretty_json(self.queries)}"
                     f"\nand payload {pretty_json(self.payload)}\n")

        # Carry out the API call and get the response
        response = func(self, endpoint, desc)
        response_json = json.dumps(response.json() if response.json()
                                   else {}, indent=4)
        response_status = response.status_code

        if response_status >= 400:
            # Log the JSON response in error if error status code is given
            logger.error(f"Results for {func.__name__.upper()} request to {self.url} :\n"
                         f"\nResponse Status: {response.status_code}"
                         f"\nResponse JSON:\n{response_json}\n")
        else:
            # Log the JSON response in debug
            logger.debug(f"Results for {func.__name__.upper()} request to {self.url} :\n"
                         f"\nResponse Status: {response.status_code}"
                         f"\nResponse JSON:\n{response_json}\n")
        return response
    return wrapper


class ApiHandler:

    auth = HTTPBasicAuth(constants.USER_NAME, constants.PASSWORD)

    def __init__(self, url: str, queries: dict = {}, payload={}, headers=None):
        self.url = url
        self.queries = queries
        self.payload = payload
        self.headers = headers or {
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

    @staticmethod
    def confluence():
        return ApiHandler(f"https://{constants.CONFLUENCE_INFOTECH_SCU_EDU_AU}")

    @staticmethod
    def jira():
        return ApiHandler(f"https://{constants.JIRA_INFOTECH_SCU_EDU_AU}")

    def set_payload(self, payload):
        self.payload = payload
        return self

    def add_queries(self, new_queries: dict[str, str]):
        self.queries = {**self.queries, **new_queries}
        return self

    @log_api_call
    def get(self, endpoint: str, desc: str = "") -> Response:
        return requests.get(
            url=self.url + f"/{endpoint}",
            params=self.queries,
            headers=self.headers,
            auth=self.auth,
        )

    @log_api_call
    def post(self, endpoint: str, desc: str = "") -> Response:
        return requests.post(
            url=self.url + f"{endpoint}",
            params=self.queries,
            headers=self.headers,
            auth=self.auth,
            data=self.payload
        )

    @log_api_call
    def put(self, endpoint: str, desc: str = "") -> Response:
        return requests.put(
            url=self.url + f"{endpoint}",
            params=self.queries,
            headers=self.headers,
            auth=self.auth,
            data=self.payload
        )

    @log_api_call
    def delete(self, endpoint: str, desc: str = "") -> Response:
        return requests.delete(
            url=self.url + f"{endpoint}",
            params=self.queries,
            headers=self.headers,
            auth=self.auth,
        )
