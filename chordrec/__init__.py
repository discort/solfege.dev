import logging
import sys

from flask import Flask
from flask_cors import CORS


def create_app(test_config=None):
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__)
    CORS(app)
    app.config['CORS_SUPPORTS_CREDENTIALS'] = True

    if test_config is not None:
        # load the test config if passed in
        app.config.update(test_config)

    # apply the blueprints to the app
    from chordrec import api

    app.register_blueprint(api.bp_api)
    app.register_blueprint(api.bpu)
    configure_logging(app)
    return app


def configure_logging(app):
    app.logger.setLevel(logging.INFO)

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.INFO)
    handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s ')
    )
    app.logger.addHandler(handler)