from flask import render_template, request
from app import app
import spur

@app.route('/')
@app.route('/index')
def index():
    pagesettings = {'title': 'Index Page'}
    return render_template('index.html')


@app.route('/r1check', methods=['GET', 'POST'])
def r1check():
    return render_template('r1check.html', 
        title='R1soft Connection Checker')


@app.route('/diskcheck', methods=['GET', 'POST'])
def diskcheck():
    if request.method == 'POST':
        sshhost = request.form.get('sshhost')
        sshuser = request.form['sshuser']
        sshpass = request.form['sshpass']
        sshport = request.form['sshport']
        shell = spur.SshShell(hostname=sshhost, 
                        username=sshuser, 
                        password=sshpass,
                        port = sshport,
                        missing_host_key=spur.ssh.MissingHostKey.accept)
        with shell:
            result = shell.run(["uptime"])
            return(result.output)
    return render_template('diskcheck.html',
        title='Disk Usage Check')


@app.route('/botwpcheck', methods=['GET', 'POST'])
def wpcheck():
    return render_template('botwpcheck.html',
        title='Bot & WP Attack Check')
        
@app.route('/timecheck', methods=['GET', 'POST'])
def timecheck():
    return render_template('timecheck.html',
        title='Find what happend around a certain time')
        
@app.route('/customcommand', methods=['GET', 'POST'])
def customcommand():
    return render_template('customcommand.html',
        title='Custom Command')

