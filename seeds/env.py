#!../venv/bin/python
import os
import sys

project_dir = os.path.abspath('../')
sys.path.append(project_dir)

from app import create_app
from app import db

app_main = create_app('app.settings.DevConfig', env='dev')
import app.models as m
