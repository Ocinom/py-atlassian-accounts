from http.http import Http

from requests import Response

http = Http.jira()


class Projects:
    """
    An object for manipulating Jira projects
    """

    @staticmethod
    def create_scrum_project(name: str, key: str) -> Response:
        """
        :param str name: The name of the project
        :param str key: The project key - must be unique and max. 10 characters
        Creates a blank project based on the scrum classic template
        https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-projects/#api-rest-api-3-project-post
        """
        return http.set_payload({
            "name": name,
            "key": key,
            "projectTemplateKey": "com.pyxis.greenhopper.jira:gh-simplified-scrum-classic",
            "projectTypeKey": "software",
        }).post(
            "/rest/api/3/project",
            f"Creating scrum project {name}..."
        )

    @staticmethod
    def delete_project(project_id_or_key: str) -> Response:
        return http.delete(
            f"/rest/api/3/project/{project_id_or_key}",
            f"Deleting project with key {project_id_or_key}"
        )

    @staticmethod
    def assign_permission_scheme_to_project(project_key_or_id: str, scheme_id: int) -> Response:
        """
        https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-project-permission-schemes/#api-rest-api-3-project-projectkeyorid-permissionscheme-put
        """
        return http.put(
            f"/rest/api/3/project/{project_key_or_id}/permissionscheme",
            f"Assigning permission scheme with ID {scheme_id} to project with key/ID {project_key_or_id}"
        )

    @staticmethod
    def create_project_role(name: str, description: str) -> Response:
        """
        https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-project-roles/#api-rest-api-3-role-post
        """
        payload = {
            "name": name,
            "description": description,
        }

        return http.set_payload(payload).post(
            "/rest/api/3/role",
            f"Creating project role {name}"
        )

    @staticmethod
    def delete_project_role(role_id: str) -> Response:
        """
        https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-project-roles/#api-rest-api-3-role-id-delete
        """
        return http.delete(
            f"/rest/api/3/role/{role_id}",
            f"Deleting project role {role_id}"
        )

    @staticmethod
    def add_actors_to_project_role(project_id_or_key: str, role_id: str,
                                   group_ids: list[str], user_ids: list[str]):
        """
        https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-project-role-actors/#api-rest-api-3-project-projectidorkey-role-id-post
        """
        payload = {}
        if group_ids:
            payload["groupId"] = group_ids
        if user_ids:
            payload["user"] = user_ids

        return http.set_payload(payload).post(
            f"/rest/api/3/project/{project_id_or_key}/role/{role_id}",
            f"Assigning groups and/or users to roles with ID {role_id} to project with key/ID {project_id_or_key}"
        )

    @staticmethod
    def delete_user_from_project_role(project_id_or_key: str, role_id: str, user_id: str):
        """
        https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-project-role-actors/#api-rest-api-3-project-projectidorkey-role-id-delete
        """
        return http.add_queries({
            "user": user_id
        }).delete(
            f"/rest/api/3/project/{project_id_or_key}/role/{role_id}",
            f"Deleting user(s) from roles with ID {role_id} in project with key/ID {project_id_or_key}"
        )

    @staticmethod
    def delete_group_from_project_role(project_id_or_key: str, role_id: str, group_id: str):
        """
        https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-project-role-actors/#api-rest-api-3-project-projectidorkey-role-id-delete
        """
        return http.add_queries({
            "groupId": group_id
        }).delete(
            f"/rest/api/3/project/{project_id_or_key}/role/{role_id}",
            f"Deleting group(s) from roles with ID {role_id} in project with key/ID {project_id_or_key}"
        )
