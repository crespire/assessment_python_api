import os
from flask import Flask

from db.shared import db
from db.models.user_post import UserPost
from db.models.post import Post
from db.models.user import User

SEED_PASSWORD = "123456"


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
        "DB_PATH", "sqlite:///database.db"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    return app


def reset(db):
    try:
        UserPost.__table__.drop(db.engine)
        User.__table__.drop(db.engine)
        Post.__table__.drop(db.engine)
    except:
        pass
    db.create_all()
    print("db is reset!")


def seed(db):
    thomas = User(username="thomas", password=SEED_PASSWORD)
    db.session.add(thomas)
    db.session.commit()

    santiago = User(username="santiago", password=SEED_PASSWORD)
    db.session.add(santiago)
    db.session.commit()

    ashanti = User(username="ashanti", password=SEED_PASSWORD)
    db.session.add(ashanti)
    db.session.commit()

    # post  1: multi author
    post1 = Post(
        text="Excepteur occaecat minim reprehenderit cupidatat dolore voluptate velit labore pariatur culpa esse mollit. Veniam ipsum amet eu dolor reprehenderit quis tempor pariatur labore. Tempor excepteur velit dolor commodo aute. Proident aute cillum dolor sint laborum tempor cillum voluptate minim. Amet qui eiusmod duis est labore cupidatat excepteur occaecat nulla.",
        likes=12,
        reads=5,
        tags=["food", "recipes", "baking"],
        popularity=0.19,
    )
    db.session.add(post1)
    db.session.commit()

    db.session.add(UserPost(user_id=santiago.id, post_id=post1.id))
    db.session.add(UserPost(user_id=thomas.id, post_id=post1.id))
    db.session.commit()

    # post 2: single-author
    post2 = Post(
        text="Ea cillum incididunt consequat ullamco nisi aute labore cupidatat exercitation et sunt nostrud. Occaecat elit tempor ex anim non nulla sit culpa ipsum aliquip. In amet in Lorem ut enim. Consectetur ea officia reprehenderit pariatur magna eiusmod voluptate. Nostrud labore id adipisicing culpa sunt veniam qui deserunt magna sint mollit. Cillum irure pariatur occaecat amet reprehenderit nisi qui proident aliqua.",
        likes=104,
        reads=200,
        tags=["travel", "hotels"],
        popularity=0.7,
    )
    db.session.add(post2)
    db.session.commit()

    db.session.add(UserPost(user_id=santiago.id, post_id=post2.id))
    db.session.commit()

    # post 3: multi-author
    post3 = Post(
        text="Voluptate consequat minim commodo nisi minim ut. Exercitation incididunt eiusmod qui duis enim sunt dolor sit nisi laboris qui enim mollit. Proident pariatur elit est elit consectetur. Velit anim eu culpa adipisicing esse consequat magna. Id do aliquip pariatur laboris consequat cupidatat voluptate incididunt sint ea.",
        likes=10,
        reads=32,
        tags=["travel", "airbnb", "vacation"],
        popularity=0.7,
    )
    db.session.add(post3)
    db.session.commit()

    db.session.add(UserPost(user_id=santiago.id, post_id=post3.id))
    db.session.add(UserPost(user_id=ashanti.id, post_id=post3.id))
    db.session.commit()

    # post 4: single-author
    post4 = Post(
        text="This is post 4",
        likes=50,
        reads=300,
        tags=["vacation", "spa"],
        popularity=0.4,
    )
    db.session.add(post4)
    db.session.commit()

    db.session.add(UserPost(user_id=ashanti.id, post_id=post4.id))
    db.session.commit()

    julia = User(username="julia", password=SEED_PASSWORD)
    db.session.add(julia)
    db.session.commit()

    cheng = User(username="cheng", password=SEED_PASSWORD)
    db.session.add(cheng)
    db.session.commit()

    print("seeded users and posts")


if __name__ == "__main__":
    with create_app().app_context():
        db.create_all()
        print("seeding...")
        reset(db)
        seed(db)
