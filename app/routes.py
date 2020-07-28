from flask import render_template
from app import app

@app.route('/')
@app.route('/index')
def index():
    pagesettings = {'title': 'Index Page'}
    return render_template('index.html')


@app.route('/r1check')
def r1check():
    
    return render_template('r1check.html', 
        title='R1soft Connection Checker')


@app.route('/diskcheck')
def diskcheck():
    return render_template('diskcheck.html',
        title='Disk Usage Check')


@app.route('/wpcheck')
def wpcheck():
    return render_template('wpcheck.html',
        title='WP Attack Check')
        
@app.route('/timecheck')
def timecheck():
    return render_template('timecheck.html',
        title='Find what happend around a certain time')

