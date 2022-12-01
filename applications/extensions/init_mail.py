from flask import Flask, current_app
from flask_mail import Mail

mail = Mail()


def init_mail(app: Flask):
    mail.init_app(app)
