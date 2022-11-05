from flask import jsonify, request, g, abort
from sqlalchemy import desc, asc

from api import api
from db.shared import db
from db.models.user_post import UserPost
from db.models.user import User
from db.models.post import Post

from db.utils import row_to_dict
from db.utils import rows_to_list
from middlewares import auth_required

VALID_PROPS = ['id', 'likes', 'reads', 'popularity']
VALID_SORTS = ['asc', 'desc']
DESC_STRING = 'desc'

@api.post("/posts")
@auth_required
def posts():
    # validation
    user = g.get("user")
    if user is None:
        return jsonify({"error": "Not authorized."}), 401

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
        return jsonify({"error": "Not authorized."}), 401

    data = request.get_json(force=True)
    authors = data.get("authorIds", None) or None

    if type(authors) is not str:
        return jsonify({"error": "Author IDs must be a string."})

    raw_list = authors.split(",")
    author_ids = []
    for id in raw_list:
        if id.__len__() > 0 and int(id) not in author_ids:
            author_ids.append(int(id))

    sort_prop = data.get("sortBy", None) or 'id'
    sort_input = data.get("direction", None) or 'asc'

    if authors is None:
        return jsonify({"error": "Must provide author IDs"}), 400
    
    if sort_prop not in VALID_PROPS:
        return jsonify({"error": "Sort property must one of: 'id', 'reads', 'likes' or 'popularity'. got '%s'" %(sort_prop)}), 400

    if sort_input not in VALID_SORTS:
        return jsonify({"error": "Sort direction not supported: '%s'" %(sort_input)}), 400

    sort_desc = True if sort_input == DESC_STRING else False
  
    if sort_prop == "likes":
        sort_obj = Post.likes
    elif sort_prop == "reads":
        sort_obj = Post.reads
    elif sort_prop == "popularity":
        sort_obj = Post.popularity
    else:
        sort_obj = Post.id

    posts = db.session.query(Post).join(UserPost).filter(UserPost.user_id.in_((author_ids))).order_by(sort_obj).all()

    unique_posts = []
    for post in posts:
        if post not in unique_posts:
            unique_posts.append(post)

    if sort_desc:
        unique_posts.reverse()

    response = {"posts": rows_to_list(unique_posts)}
    return response, 200

@api.route("/posts/<post_id>", methods=["PATCH"])
@auth_required
def update_post(post_id=None):
    user = g.get("user")
    if user is None:
        return jsonify({"error": "Not authorized."}), 401

    if post_id is None:
        return jsonify({"error": "No post ID provided."}), 400

    post = Post.query.get(post_id)
    if post is None:
        return jsonify({"error": f"Post with id {post_id} does not exist."}), 404

    if user not in post.users:
        return jsonify({"error": "That post is not yours."}), 403

    data = request.get_json(force=True)
    authors = data.get("authorIds", None) or None
    
    if authors is not None and type(authors) is not list:
        return jsonify({"error": "Author IDs must be a list"}), 400

    if authors is not None and not all(isinstance(id, int) for id in authors):
        return jsonify({"error": "Author IDs must be a list of integers"}), 400

    tags = data.get("tags", None) or None
    if tags is not None and type(tags) is not list:
        return jsonify({"error": "Tags must be a list of strings."}), 400

    if tags is not None and not all(isinstance(tag, str) for tag in tags):
        return jsonify({"error": "Tags must all be strings"}), 400

    text = data.get("text", None) or None
    if text is not None and type(text) is not str:
        return jsonify({"error": "Text needs to be a string."}), 400

    current_author_ids = [record.user_id for record in db.session.query(UserPost.user_id).filter_by(post_id=post_id)]

    if authors is not None and type(authors) is list:
        for id in authors:
            user = User.query.get(id)
            if user is None:
                return jsonify({"error": f"Could not find user with id {id}"}), 404
                        
        authors_to_add = []
        authors_to_delete = []
        
        for id in current_author_ids:
            if id not in authors:
                authors_to_delete.append(id)

        for id in authors:
            if id not in current_author_ids:
                authors_to_add.append(id)

        for id in authors_to_delete:
            instance = db.session.query(UserPost).filter_by(post_id=post_id, user_id=id).one()
            db.session.delete(instance)

        for id in authors_to_add:
            db.session.add(UserPost(user_id=id, post_id=post_id))
    
    if tags is not None and type(tags) is list:
        post.tags = tags
    
    if text is not None and type(text) is str:
        post.text = text

    db.session.commit()

    post = Post.query.get(post_id)
    id_list = [record.user_id for record in db.session.query(UserPost.user_id).filter_by(post_id=post_id)]
    print("Updated authors :", id_list)
    post_output = row_to_dict(post)
    post_output["authorIds"] = id_list
    
    return {"post": post_output}, 200