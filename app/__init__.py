from flask import Flask, session
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
Bootstrap(app)

from app import routes
