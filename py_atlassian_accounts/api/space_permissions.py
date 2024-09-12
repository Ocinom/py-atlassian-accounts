class SpacePermissions:

    def __init__(self, subject_type: str, subject_id: str,
                 size: int, perms: list[tuple[str, str]] = []) -> None:
        """
        https://developer.atlassian.com/cloud/confluence/rest/v1/api-group-space/#api-wiki-rest-api-space-post
        subject_type: "user" or "group"
        subject_id: accountId of user or ID number of group
        size: Honestly, the Atlassian documentation was not clear about what
            this does, but it is a required field
        perms: A list consisting of (str, str) tuples, where the first string
            is the operation and the second string is the target type, as seen
            in their documentation
        """
        self.subject_type = subject_type
        self.subject_id = subject_id
        self.size = size
        self.perms = perms

    def id_name(self) -> str:
        """
        Group permissions have the following identifier within the resulting JSON:
            "id": "<group ID>"
        User permissions have the following identifier within the resulting JSON:
            "accountId": "<User's Atlassian account ID>"
        """
        match self.subject_type:
            case "group":
                return "id"
            case "user":
                return "accountId"
            case _:
                return ""

    def add_permission(self, perm: tuple[str, str]):
        self.perms += [perm]
        return self

    def add_permissions(self, perms: list[tuple[str, str]]):
        self.perms += perms
        return self

    def permissions_list(self) -> list:
        """
        Constructs permission dicts, adds them to a list, and returns that list
        Follows the payload structure in the below link:
        https://developer.atlassian.com/cloud/confluence/rest/v1/api-group-space/#api-wiki-rest-api-space-post
        """
        permissions = []
        for perm in self.perms:
            permissions.append(
                {
                    "subjects": {
                        self.subject_type: {
                            "results": [
                                {
                                    "type": self.subject_type,
                                    self.id_name(): self.subject_id,
                                }
                            ],
                            "size": self.size
                        }
                    },
                    "operation": {
                        "operation": perm[0],
                        "targetType": perm[1]
                    },
                    "anonymousAccess": False,
                    "unlicensedAccess": False,
                }
            )
        return permissions

    @staticmethod
    def user_permissions() -> list[tuple[str, str]]:
        """
        Space permissions for non-admin users (i.e. students and tutors)
        """
        return [
            # Allow students just to read the space
            ("read", "space"),

            # Allow students to create, archive, and delete pages
            ("create", "page"),
            ("archive", "page"),
            ("delete", "page"),

            # Allow students to create and delete blogposts
            ("create", "blogpost"),
            ("delete", "blogpost"),

            # Allow students to create and delete comments
            ("create", "comment"),
            ("delete", "comment"),

            # Allow students to create and delete attachments
            ("create", "attachment"),
            ("delete", "attachment"),
        ]

    @staticmethod
    def admin_permissions() -> list[tuple[str, str]]:
        """
        Space permissions for admin users
        """
        return [
            # Grant all space permissions
            ("administer", "space"),
            ("read", "space"),
            ("delete", "space"),
            ("export", "space"),

            # Grant all page permissions
            ("create", "page"),
            ("archive", "page"),
            ("delete", "page"),

            # Grant all blog permissions
            ("create", "blogpost"),
            ("delete", "blogpost"),

            # Grant all comment permissions
            ("create", "comment"),
            ("delete", "comment"),

            # Grant all attachment permissions
            ("create", "attachment"),
            ("delete", "attachment"),

            # Grant all restriction permissions
            ("create", "restrict_content"),
            ("delete", "attachment"),
        ]
