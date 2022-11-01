from ..shared import db


class UserPost(db.Model):
    __tablename__ = "user_post"
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey("post.id"), primary_key=True)
