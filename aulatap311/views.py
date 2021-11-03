from flask import render_template

from .models import Usuario

def root():
    return render_template('index.html')