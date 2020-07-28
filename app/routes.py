from flask import render_template
from app import app

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/r1check')
def r1check():
    return render_template('r1check.html')


@app.route('/diskcheck')
def diskcheck():
    return render_template('diskcheck.html', title='Disk Usage Check')


@app.route('/wpcheck')
def wpcheck():
    return render_template('wpcheck.html', title='WP Attack Check')

