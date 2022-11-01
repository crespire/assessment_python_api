import json
from tests.utils import make_token


def test_get_posts(client):
    """should return all posts of author ID 2 in specific order."""

    token = make_token(2)
    query_params = {"authorIds": "2"}
    response = client.get(
        "/api/posts", headers={"x-access-token": token}, query_string=query_params
    )

    assert json.dumps(response.json, sort_keys=True) == json.dumps(
        posts_of_user_2, sort_keys=True
    )


def test_update_all_properties(client):
    """should update properties of a post."""

    token = make_token(1)
    post_id = 1
    data = {"tags": ["travel", "vacation"], "text": "my text", "authorIds": [1, 5]}

    response = client.patch(
        f"/api/posts/{post_id}",
        headers={
            "x-access-token": token,
            "Content-Type": "application/json",
        },
        data=json.dumps(data),
    )

    assert json.dumps(response.json, sort_keys=True) == json.dumps(
        updated_post_1, sort_keys=True
    )


def test_update_text_property(client):
    """should only update text when only text is provided."""

    token = make_token(2)
    post_id = 3
    data = {"text": "new text"}

    response = client.patch(
        f"/api/posts/{post_id}",
        headers={
            "x-access-token": token,
            "Content-Type": "application/json",
        },
        data=json.dumps(data),
    )

    assert json.dumps(response.json, sort_keys=True) == json.dumps(
        updated_post_2, sort_keys=True
    )


# mock data
posts_of_user_2 = {
    "posts": [
        {
            "tags": ["food", "recipes", "baking"],
            "id": 1,
            "text": "Excepteur occaecat minim reprehenderit cupidatat dolore voluptate velit labore pariatur culpa esse mollit. Veniam ipsum amet eu dolor reprehenderit quis tempor pariatur labore. Tempor excepteur velit dolor commodo aute. Proident aute cillum dolor sint laborum tempor cillum voluptate minim. Amet qui eiusmod duis est labore cupidatat excepteur occaecat nulla.",
            "likes": 12,
            "reads": 5,
            "popularity": 0.19,
        },
        {
            "tags": ["travel", "hotels"],
            "id": 2,
            "text": "Ea cillum incididunt consequat ullamco nisi aute labore cupidatat exercitation et sunt nostrud. Occaecat elit tempor ex anim non nulla sit culpa ipsum aliquip. In amet in Lorem ut enim. Consectetur ea officia reprehenderit pariatur magna eiusmod voluptate. Nostrud labore id adipisicing culpa sunt veniam qui deserunt magna sint mollit. Cillum irure pariatur occaecat amet reprehenderit nisi qui proident aliqua.",
            "likes": 104,
            "reads": 200,
            "popularity": 0.7,
        },
        {
            "tags": ["travel", "airbnb", "vacation"],
            "id": 3,
            "text": "Voluptate consequat minim commodo nisi minim ut. Exercitation incididunt eiusmod qui duis enim sunt dolor sit nisi laboris qui enim mollit. Proident pariatur elit est elit consectetur. Velit anim eu culpa adipisicing esse consequat magna. Id do aliquip pariatur laboris consequat cupidatat voluptate incididunt sint ea.",
            "likes": 10,
            "reads": 32,
            "popularity": 0.7,
        },
    ],
}

updated_post_1 = {
    "post": {
        "authorIds": [1, 5],
        "id": 1,
        "likes": 12,
        "popularity": 0.19,
        "reads": 5,
        "tags": ["travel", "vacation"],
        "text": "my text",
    },
}

updated_post_2 = {
    "post": {
        "authorIds": [2, 3],
        "id": 3,
        "likes": 10,
        "popularity": 0.7,
        "reads": 32,
        "tags": ["travel", "airbnb", "vacation"],
        "text": "new text",
    },
}
