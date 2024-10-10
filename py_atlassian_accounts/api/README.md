# API module
The API module is responsible for sending messages to the Atlassian API and collecting json responses. It serves as a simple Http client that sends and receives json data.

## Http
The Http class in `http.py` is the backbone of this module. It is configured as a http client wrapped by a custom decorator used for logging purposes. Each execution step will be logged at INFO level and payload and json response data will be logged at DEBUG level

Additional payload data like request parameters or a json body is added on a per-instance basis i.e. each instance of the Http object will have its own distinct set of json payloads and request parameters. Http headers are defaulted to accept json responses. However, initialising the object with a custom headers dict is also possible.

Calling http methods (i.e. get, post, put, etc.) requires two parameters:
- endpoint: The url endpoint suffix to be appended to the base url
- desc: The description outlining the API execution step to be used by logging
These arguments are positional so order matters - endpoint first followed by desc.

e.g.
```python
# The create_group function in groups.py
from api.http import Http

http = Http.jira()

# -- snip --

@staticmethod
def create_group(name: str) -> Response:
    return http.set_payload({
        "name": name
    }).post (
        "/rest/api/3/group", # endpoint
        f"Creating a group with name {name} in Jira." # desc
    )
```

For creating additional http api call methods, the function signature must return a Response object to be wrapped by the `@log_api_call` decorator to be logged.

For convenience, the Http object has static methods `confluence()` and `jira()` to initialise these clients with their respective base urls taken from constants

## Permission Schemes
Permission schemes detail a set of permissions to be assigned to a group or to a user. The permissions are structured in a dict that contains the following:
- Key: A str tuple ("<subject_type>", "<subject_id>") that takes the subject type ("user" or "group") and the id for that subject
- Value: A list of strings that contain the permissions to be assigned to the subject. Within the permission_schemes.py file, there are constants STUDENT_PERMISSIONS and TUTOR_PERMISSIONS that have been pre-configured for those types of users/subjects

## Projects
Projects contains a set of static methods that can be called to create and manipulate projects. This includes assigning permission schemes that can be created from our permission scheme object. The scheme id must be known to assign the permission scheme.

## Space Permissions
The SpacePermissions object is used to create a set for permissions for a particular subject in a confluence space. Each permission consists of a str tuple ("<permission>", "<scope>"). Refer to the pre-configured USER_PERMISSIONS and ADMIN_PERMISSIONS to get a better idea of what a permission would entail.

A list of these permissions will be stored in an instance of the SpacePermissions object and a resultant list of dicts that are structured in the way that [Confluence's documentation](https://developer.atlassian.com/cloud/confluence/rest/v1/api-group-space/#api-wiki-rest-api-space-post) shows will be returned by the `permissions_list()` method. This list will subsequently be used by the Spaces object.

## Spaces
Spaces contains a set of methods to create and delete Confluence spaces. Note that permissions must be added to the object instance prior to creating the space.

## Groups
Groups contains a list of static methods to create and manipulate Jira groups.
