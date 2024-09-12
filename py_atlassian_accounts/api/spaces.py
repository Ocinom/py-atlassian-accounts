from api.api_handler import ApiHandler
from api.space_permissions import SpacePermissions

from requests import Response


class Spaces:

    handler = ApiHandler.confluence()

    def __init__(self, name: str, key: str, description: str, permissions: list = []):
        """
        :param str name: The name of the space
        :param str key: The unique key for the space
        :param str description: A brief dsecription of the space
        :param list permissions: A list of permission dicts, which are handled by the
            SpacePermissions object
        """
        self.name = name
        self.key = key
        self.description = description
        self.permissions = permissions

    def add_permissions(self, subject_type: str, subject_id: str,
                        size: int, perms: list[tuple[str, str]]):
        """
        :param str subject_type: The type of subject to apply the permissions to
            ie. "user" or "group"
        :param str subject_id: The string that uniquely identifies the subject.
            for users, it would be their Atlassian account ID. For groups, it
            would be their group ID number
        :param int size: A required parameter within the permissions JSON. It is
            clearly explained within Atlassian's documentation as to what this
            signifies
        :param list[tuple[str, str]] perms: A list of permisson tuples. Each
            permission tuple has the following structure:
            ("<operation>", "<target Type>").
            Refer to the documentation link below to find the accepted values for
            both fields
        https://developer.atlassian.com/cloud/confluence/rest/v1/api-group-space/#api-wiki-rest-api-space-post
        """
        sp = SpacePermissions(subject_type, subject_id, size).add_permissions(perms)
        self.permissions += sp.permissions_list()

    def add_user_permissions(self, subject_type: str, subject_id: str, size: int):
        """
        Adds non-admin permissions for a group or user
        Note: size is a required field that is not clearly explained in Confluence Cloud's
            documentation.
        """
        sp = SpacePermissions(
            subject_type, subject_id, size
        ).add_permissions(
            SpacePermissions.user_permissions()
        )
        self.permissions += sp.permissions_list()
        return self

    def add_admin_permissions(self, subject_type: str, subject_id: str, size: int):
        """
        Adds admin permissions for a group or user
        """
        sp = SpacePermissions(
            subject_type, subject_id, size
        ).add_permissions(
            SpacePermissions.admin_permissions()
        )
        self.permissions += sp.permissions_list()
        return self

    def payload(self) -> dict:
        """
        https://developer.atlassian.com/cloud/confluence/rest/v1/api-group-space/#api-wiki-rest-api-space-post
        https://requests.readthedocs.io/en/latest/api/
        Creates a dictionary payload from instance variables to be passed to the api_handler's
        json parameter
        """
        payload = {
            "name": self.name,
            "key": self.key,
            "description": {
                "plain": {
                    "value": self.description
                }
            }
        }
        # If permissions is neither empty nor None, add it to payload
        # Note that a json request sent with no permissions parameters
        # results in default permissions automatically implemented
        # in the newly created space
        if (self.permissions):
            payload["permissions"] = self.permissions
        return payload

    def create_space(self) -> Response:
        """
        https://developer.atlassian.com/cloud/confluence/rest/v1/api-group-space/#api-wiki-rest-api-space-post
        """
        response = self.handler.set_payload(self.payload).post(
            "/rest/api/space",
            f"Creating space {self.name} in Confluence...",
        )
        return response

    @staticmethod
    def delete_space(key: str) -> Response:
        """
        https://developer.atlassian.com/cloud/confluence/rest/v1/api-group-space/#api-wiki-rest-api-space-spacekey-delete
        """
        response = Spaces.handler.delete(
            "/rest/api/space/" + key,
            f"Deleting space with key {key} in Confluence...",
        )
        return response
