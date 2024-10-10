from api.http import Http

from requests import Response
import json

http = Http.jira()


class Groups:
    """
    An object for manipulating Jira groups
    """

    @staticmethod
    def create_group(name: str) -> Response:
        """
        https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-groups/#api-rest-api-3-group-post
        """
        return http.set_payload({
                "name": name
            }
        ).post(
            "/rest/api/3/group",
            f"Creating a group with name {name} in Jira."
        )

    @staticmethod
    def delete_group(name: str) -> Response:
        """
        https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-groups/#api-rest-api-3-group-delete
        """
        return http.delete(
            "/rest/api/3/group",
            f"Creating a group with name {name} in Jira."
        )

    @staticmethod
    def add_user_to_group(groupID: str, accountID: str) -> Response:
        """
        https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-groups/#api-rest-api-3-group-user-post
        """
        return http.add_queries({
            "groupId": groupID
        }).set_payload(json.dumps({
            "accountId": accountID
        })).post(
            "/rest/api/3/group/user",
            f"Adding user with account ID {accountID} to group with ID {groupID} in Jira.",
        )

    @staticmethod
    def remove_user_from_group(groupID: str, accountID: str) -> Response:
        """
        https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-groups/#api-rest-api-3-group-user-delete
        """
        return http.add_queries({
            "groupId": groupID,
            "accountId": accountID
        }).delete(
            "/rest/api/3/group/user",
            f"Removing user with account ID {accountID} from group with ID {groupID} in Jira."
        )
