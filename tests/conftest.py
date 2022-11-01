import pytest

from db.shared import db
from app import create_app
import seed


@pytest.fixture
def client():
    app = create_app()
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["TESTING"] = True
    with app.test_client() as client:
        with app.app_context():
            db.init_app(app)
            seed.reset(db)
            seed.seed(db)
        yield client
