from api.http import Http

from requests import Response

http = Http.confluence()

STUDENT_PERMISSIONS = [
        # Issue permissions
        "BROWSE_PROJECTS",
        "ASSIGN_ISSUES",
        "CLOSE_ISSUES",
        "CREATE_ISSUES",
        "DELETE_ISSUES",
        "EDIT_ISSUES",
        "MOVE_ISSUES",
        "RESOLVE_ISSUES",
        "SCHEDULE_ISSUES",
        "TRANSITION_ISSUES",

        # Comments permissions
        "ADD_COMMENTS",
        "DELETE_OWN_COMMENTS",
        "EDIT_OWN_COMMENTS",

        # Attachments permissions
        "CREATE_ATTACHMENTS",
        "DELETE_OWN_ATTACHMENTS",

        # Time tracking permissions
        "DELETE_OWN_WORKLOGS",
        "EDIT_OWN_WORKLOGS",
        "WORK_ON_ISSUES",
]

TUTOR_PERMISSIONS = [
        # Issue permissions
        "BROWSE_PROJECTS",
        "ASSIGN_ISSUES",
        "CLOSE_ISSUES",
        "CREATE_ISSUES",
        "DELETE_ISSUES",
        "EDIT_ISSUES",
        "MOVE_ISSUES",
        "RESOLVE_ISSUES",
        "SCHEDULE_ISSUES",
        "TRANSITION_ISSUES",

        # Comments permissions
        "ADD_COMMENTS",
        "DELETE_OWN_COMMENTS",
        "DELETE_ALL_COMMENTS",
        "EDIT_OWN_COMMENTS",
        "EDIT_ALL_COMMENTS",

        # Attachments permissions
        "CREATE_ATTACHMENTS",
        "DELETE_OWN_ATTACHMENTS",
        "DELETE_ALL_ATTACHMENTS",

        # Time tracking permissions
        "DELETE_OWN_WORKLOGS",
        "DELETE_ALL_WORKLOGS",
        "EDIT_OWN_WORKLOGS",
        "EDIT_ALL_WORKLOGS",
        "WORK_ON_ISSUES",
]


class PermissionSchemes:
    """
    An object to create and edit permission schemes to be used in Jira projects
    self.permissions consist for the following data structure:
        A dictionary with the following tuple as a key:
            ("<subject_type>", "<subject_id>")
        and the following as the value to that key:
            [list of permission strings]
    The above lists (STUDENT_PERMISSIONS and TUTOR_PERMISSIONS) contain most,
    if not all of the permission strings required to be passed to the API calls

    e.g.
        permissions = {
            ("user", "a3t53259sdg80gw=a0guaas9etvhas"): STUDENT_PERMISSIONS,
            ("group", "myGroupId"): STUDENT_PERMISSIONS,
            ("group", "tutorGroupId"): TUTOR_PERMISSIONS,
        }
    """

    def __init__(self):
        """
        Refer to the below link to find all built-in Jira permissions:
        https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-permission-schemes/#api-rest-api-3-permissionscheme-get
        """
        self.permissions = {}

    def add_tutor_user_permissions(self, tutor_id: str):
        """
        Adds tutor permissions to be given to a given tutor ID
        """
        self.permissions.update({
            ("user", tutor_id): TUTOR_PERMISSIONS
        })
        return self

    def add_student_user_permissions(self, user_id: str):
        """
        Adds student permissions to be given to a given student ID
        """
        self.permissions.update({
            ("user", user_id): STUDENT_PERMISSIONS
        })
        return self

    def add_tutor_group_permissions(self, group_id: str):
        """
        Adds tutor permissions to be given to a given group ID
        """
        self.permissions.update({
            ("group", group_id): TUTOR_PERMISSIONS
        })
        return self

    def add_student_group_permissions(self, group_id: str):
        """
        Adds student permissions to be given to a given group ID
        """
        self.permissions.update({
            ("group", group_id): STUDENT_PERMISSIONS
        })
        return self

    def remove_permission(self, subject_type: str, subject_id: str):
        """
        Remove the permission set for a user or group
        """
        if (subject_type, subject_id) in self.permissions:
            del self.permissions[(subject_type, subject_id)]

    def create_permission_scheme(self, description: str, scheme_name: str) -> Response:
        """
        scheme_name must be unique from other scheme names in the Jira Cloud
        https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-permission-schemes/#api-rest-api-3-permissionscheme-post
        """
        payload = {
            "description": description,
            "name": scheme_name,
            "permissions": [
                {
                    "holder": {
                        "type": holder_type,
                        "value": value
                    },
                    "permission": permission
                }
                for holder, permissions in self.permissions
                for holder_type, value in holder
                for permission in permissions
            ]
        }
        return http.set_payload(payload).post(
            "/rest/api/3/permissionscheme",
            f"Creating permission scheme {scheme_name}..."
        )

    @staticmethod
    def remove_permission_scheme(scheme_id: str) -> Response:
        """
        https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-permission-schemes/#api-rest-api-3-permissionscheme-schemeid-delete
        """
        return http.delete(
            f"/rest/api/3/permissionscheme/{scheme_id}",
            f"Deleting permission scheme with id {scheme_id}"
        )
