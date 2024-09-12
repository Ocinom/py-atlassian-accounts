from api.api_handler import ApiHandler

from requests import Response


class PermissionSchemes:

    handler = ApiHandler.confluence()

    def __init__(self):
        """
        self.permissions is structured in the following manner:
        permissions = {
            ("<subject_type>", "<subject_id>"): [list of permission strings]
        }
        Refer to the below link to find all built-in Jira permissions:
        https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-permission-schemes/#api-rest-api-3-permissionscheme-get
        """
        self.permissions = {}

    def add_tutor_user_permissions(self, tutor_id: str):
        """
        Adds tutor permissions to be given to a given tutor ID
        """
        self.permissions.update({
            ("user", tutor_id): PermissionSchemes.tutor_permissions()
        })
        return self

    def add_student_user_permissions(self, user_id: str):
        """
        Adds student permissions to be given to a given student ID
        """
        self.permissions.update({
            ("user", user_id): PermissionSchemes.student_permissions()
        })
        return self

    def add_tutor_group_permissions(self, group_id: str):
        """
        Adds tutor permissions to be given to a given group ID
        """
        self.permissions.update({
            ("group", group_id): PermissionSchemes.tutor_permissions()
        })
        return self

    def add_student_group_permissions(self, group_id: str):
        """
        Adds student permissions to be given to a given group ID
        """
        self.permissions.update({
            ("group", group_id): PermissionSchemes.student_permissions()
        })
        return self

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

        response = PermissionSchemes.handler.set_payload(payload).post(
            "/rest/api/3/permissionscheme",
            f"Creating permission scheme {scheme_name}..."
        )

        return response

    @staticmethod
    def student_permissions() -> list[str]:
        """
        The currently configured set of permissions to assign to a student
        """
        return [
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

    @staticmethod
    def tutor_permissions() -> list[str]:
        """
        The currently configured set of permissions to assign to a tutor
            - slightly different, but lets them view and modify all projects
            instead of just one
        """
        return [
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
