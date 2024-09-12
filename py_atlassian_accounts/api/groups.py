from api.api_handler import ApiHandler

from requests import Response
import json


class Groups:

    @staticmethod
    def create_group(name: str) -> Response:
        """
        https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-groups/#api-rest-api-3-group-post
        """
        response = ApiHandler.jira().set_payload({
                "name": name
            }
        ).post(
            "/rest/api/3/group",
            f"Creating a group with name {name} in Jira."
        )
        return response

    @staticmethod
    def add_user_to_group(groupID: str, accountID: str) -> Response:
        """
        https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-groups/#api-rest-api-3-group-user-post
        """
        response = ApiHandler.jira().add_queries({
            "groupId": groupID
        }).set_payload(json.dumps({
            "accountId": accountID
        })).post(
            "/rest/api/3/group/user",
            f"Adding user with account ID {accountID} to group with ID {groupID} in Jira.",
        )
        return response

    @staticmethod
    def remove_user_from_group(groupID: str, accountID: str) -> Response:
        """
        https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-groups/#api-rest-api-3-group-user-delete
        """
        response = ApiHandler.jira().add_queries({
            "groupId": groupID,
            "accountId": accountID
        }).delete(
            "/rest/api/3/group/user",
            f"Removing user with account ID {accountID} from group with ID {groupID} in Jira."
        )
        return response
