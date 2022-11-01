from sqlalchemy.orm import validates
from ..shared import db
from db.models.user import User


class Post(db.Model):
    __tablename__ = "post"
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String, nullable=False)
    likes = db.Column(db.Integer, default=0, nullable=False)
    reads = db.Column(db.Integer, default=0, nullable=False)
    popularity = db.Column(db.Float, default=0.0, nullable=False)
    users = db.relationship("User", secondary="user_post", viewonly=True)

    # note: comma separated string since sqlite does not support arrays
    _tags = db.Column("tags", db.String, nullable=False)

    # getter and setter for tags column.
    # converts list to string when value is set and string to list when value is retrieved.
    @property
    def tags(self):
        return self._tags.split(",")

    @tags.setter
    def tags(self, tags):
        self._tags = ",".join(tags)

    @validates("popularity")
    def validate_popularity(self, key, popularity) -> str:
        if popularity > 1.0 or popularity < 0.0:
            raise ValueError("Popularity should be between 0 and 1")
        return popularity

    @staticmethod
    def get_posts_by_user_id(user_id):
        user = User.query.get(user_id)
        return Post.query.with_parent(user).all()
