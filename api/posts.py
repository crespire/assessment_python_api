from flask import jsonify, request, g, abort

from api import api
from db.shared import db
from db.models.user_post import UserPost
from db.models.post import Post

from db.utils import row_to_dict
from middlewares import auth_required

import json


@api.post("/posts")
@auth_required
def posts():
    # validation
    user = g.get("user")
    if user is None:
        return abort(401)

    data = request.get_json(force=True)
    text = data.get("text", None)
    tags = data.get("tags", None)
    if text is None:
        return jsonify({"error": "Must provide text for the new post"}), 400

    # Create new post
    post_values = {"text": text}
    if tags:
        post_values["tags"] = tags

    post = Post(**post_values)
    db.session.add(post)
    db.session.commit()

    user_post = UserPost(user_id=user.id, post_id=post.id)
    db.session.add(user_post)
    db.session.commit()

    return row_to_dict(post), 200

@api.route("/posts")
@auth_required
def get_posts():
    # validation
    user = g.get("user")
    if user is None:
        return abort(401)

    data = request.get_json(force=True)
    authors = data.get("authorIds", None)
    sortProp = data.get("sortBy", None) or 'id'
    sortDir = data.get("direction", None) or 'asc'
    valid_props = ['id', 'likes', 'reads', 'popularity']
    valid_dir = ['asc', 'desc']
    if authors is None:
        return jsonify({"error": "Must provide author IDs"}), 400
    
    if sortProp not in valid_props:
        return jsonify({"error": "Sort property must one of: 'id', 'reads', 'likes' or 'popularity'. got '%s'" %(sortProp)}), 400

    if sortDir not in valid_dir:
        return jsonify({"error": "Sort direction not supported: '%s'" %(sortDir)}), 400

    author_ids = list(map(int, authors.split(",")))

    # Create payload
    posts = db.session.query(Post).join(UserPost).filter(UserPost.user_id.in_((author_ids))).all()
    sortBool = True if sortDir == 'desc' else False

    if sortProp == 'likes':            
        posts.sort(key=lambda x: x.likes, reverse=sortBool)
    elif sortProp == 'reads':
        posts.sort(key=lambda x: x.reads, reverse=sortBool)
    elif sortProp == 'popularity':
        posts.sort(key=lambda x: x.popularity, reverse=sortBool)

    json_posts = []
    for post in posts:
        json_posts.append(post.serialize())

    return jsonify({"posts": json_posts}), 200