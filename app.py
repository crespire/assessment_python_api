from flask import Flask, request
import os
import sys
import click
from werkzeug.exceptions import HTTPException
import traceback


from dotenv import load_dotenv

load_dotenv()


def create_app():
    sys.path.append(".")  # to allow sub modules to access the parent module easily

    from db.shared import db
    from api import api as api_blueprint

    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
        "DB_PATH", "sqlite:///database.db"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)

    app.register_blueprint(api_blueprint, url_prefix="/api")

    @app.errorhandler(404)
    def handle_bad_request(e):
        return {"error": "The route is not defined"}, 404

    @app.errorhandler(Exception)
    def handle_exception(e):
        # pass through HTTP errors. You wouldn't want to handle these generically.
        if isinstance(e, HTTPException):
            return e

        # now you're handling non-HTTP exceptions only
        return {"message": repr(e), "stack": traceback.format_exc()}, 500

    @app.cli.command()
    @click.argument("test_names", nargs=-1)
    def test(test_names):
        """Run the unit tests."""

        import pytest

        if test_names:
            sys.exit(pytest.main(["-vv", *test_names]))
        else:
            sys.exit(pytest.main(["-vv", "tests/"]))

    return app


app = create_app()
