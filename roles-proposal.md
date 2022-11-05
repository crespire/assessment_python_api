# Adding roles to users for posts.

### Question 1: Database Changes

In terms of the schema, we have a few options.

I am unclear what the "viewer" role is for, so I'd probably ask for some additional context here: is the idea that a post can sit as "published" or "draft" and we only want published posts to be visible?

Or is the intent that only certain logged in users can view the post regardless of its status?

Depending on the answer, there may be an opportunity to update the Post schema to include this "published" boolean. Otherwise, the "viewer" role could be rolled into the general authorization system outlined below.

In terms of implementing authorization roles, I would probably update the UserPost table to include this "role" information. This way every user can have a role and we can filter as required. We would have to centralize and define what roles are capable of, so a new `Role` model here might be good. Then it would be simple to create additional roles in the future and use granular permissions, like `chmod` so we can create custom roles with custom authorization levels. We'd probably also need a `UserRole` model which references the resource and the user, so we can assign these roles to users and edit permissions on the fly.

I think this way, we can specify a somewhat complete authorization system that is outlined in the prompt (only owners can update author list, for example).

### Question 2: Changes to PATCH route
I would probably build a helper to retrieve all the UserPost records for a given post, then check the logged in user against these records to consider if they are authorized via querying the Roles model. If the user can perform what is requested in the PATCH request, then proceed, otherwise return a 403 error.

On the assumption that we implement the role system above, we would have to make sure we update the patch functionality.

First, we have to probably add a `roles` field to the request body so that we can update the roles in our patch as well. Inside the roles field, all sub-fields are optional, but we could make changes this way:

A sample updated request:
```json
{
  "roles": {
    "add": {
      "owner": [1],  # array of numbers
      "editor": [5],
      "viewer": [1, 5],
    },
    "delete": {
      "owner": [5],  # array of numbers
    },
  },
  "tags": ["tech", "health"],
  "text": "Some very short blog post text here."
}
```

Any changes requested within the `roles` field would be checked:
1. Can the current logged in user make this change?
  1. If so, validate change; otherwise return an error and do not make changes.
1. Does this change fit within our constraints? (how many owners are on this resource after this proposed change?)
  1. If so, make the change; otherwise return error and do not make changes.
1. Save changes to the resource, and then return success body.