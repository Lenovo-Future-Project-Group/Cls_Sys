from flask import Flask

from applications.view.quantify.v1 import v1


def register_quantify_views(app: Flask):
    app.register_blueprint(v1)
