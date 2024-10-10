USER_PERMISSIONS = [
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

ADMIN_PERMISSIONS = [
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


class SpacePermissions:
    """
    A set of permissions given to either a group of a user
    The permissions are stored in self.perms as a (str, str) tuple,
    where the first str is the operation and the second str is the
    target type. Refer to the documentation below for more details
    https://developer.atlassian.com/cloud/confluence/rest/v1/api-group-space/#api-wiki-rest-api-space-post
    """

    def __init__(self, subject_type: str, subject_id: str,
                 size: int, perms: list[tuple[str, str]] = []) -> None:
        """
        https://developer.atlassian.com/cloud/confluence/rest/v1/api-group-space/#api-wiki-rest-api-space-post
        subject_type: "user" or "group"
        subject_id: accountId of user or ID number of group
        size: Honestly, the Atlassian documentation was not clear about what
            this does, but it is a required field
        perms: A list consisting of (str, str) permission tuples
        """
        self.subject_type = subject_type
        self.subject_id = subject_id
        self.size = size
        self.perms = perms

    def id_name(self) -> str:
        """
        Returns the corresponding key string for the required subject type
        "id" for groups,
        "accountId" for users,
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
        Constructs permission dicts from self.perms, adds them to a list,
        and returns that list
        Follows the payload structure in the below link:
        https://developer.atlassian.com/cloud/confluence/rest/v1/api-group-space/#api-wiki-rest-api-space-post
        """
        return [
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
                    "operation": operation,
                    "targetType": target_type
                },
                "anonymousAccess": False,
                "unlicensedAccess": False,
            }
            for operation, target_type in self.perms
        ]
