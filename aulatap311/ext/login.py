from typing import NoReturn

from flask_login import LoginManager
from flask import Flask

loginmanager = LoginManager()

def init_app(app: Flask) -> NoReturn:
    loginmanager.init_app(app)
