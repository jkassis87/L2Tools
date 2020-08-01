from flask import render_template, request
from app import app
import spur

@app.route('/')
@app.route('/index')
def index():
    pagesettings = {'title': 'Index Page'}
    return render_template('index.html')


# code for the r1soft checking tool
@app.route('/r1check_results')
@app.route('/r1check', methods=['GET', 'POST'])
def r1check():
    # triggered when the submit button is pressed
    if request.method == 'POST':
    
        # prepares ssh login
        sshhost = request.form.get('sshhost')
        sshuser = request.form['sshuser']
        sshpass = request.form['sshpass']
        sshport = request.form['sshport']
        shell = spur.SshShell(hostname=sshhost, 
                        username=sshuser, 
                        password=sshpass,
                        port = sshport,
                        missing_host_key=spur.ssh.MissingHostKey.accept)
                        
        # options in ssh command
        sshhosttype = request.form['hosttype']
        sshr1server = request.form['r1server']
        
        #### START END prepares ssh commands to run
        
        # pings r1soft server
        ssh_r1ping = f"ping {sshr1server}"
        
        # gets list of installed kernel modules
        ssh_kernelver = r"uname -r"
        
        # gets list of installed kernels and modules
        ssh_kernelmods = r"rpm -qa | grep kernel"
        
        #### END prepares ssh commands to run
        
        # logs in to host, runs commands, outputs results to new window
        #with shell:
            #result = shell.run(["uptime"])
            #return(result.output)
        return render_template('r1check_results.html', 
                ssh_r1ping=ssh_r1ping, 
                ssh_kernelver=ssh_kernelver, 
                ssh_kernelmods=ssh_kernelmods)
        
    return render_template('r1check.html', 
        title='R1soft Connection Checker')


# code for the large files and folders checking tool
@app.route('/diskcheck_results')
@app.route('/diskcheck', methods=['GET', 'POST'])
def diskcheck():
    # triggered when the submit button is pressed
    if request.method == 'POST':
    
        # prepares ssh login
        sshhost = request.form.get('sshhost')
        sshuser = request.form['sshuser']
        sshpass = request.form['sshpass']
        sshport = request.form['sshport']
        shell = spur.SshShell(hostname=sshhost, 
                        username=sshuser, 
                        password=sshpass,
                        port = sshport,
                        missing_host_key=spur.ssh.MissingHostKey.accept)
                        
        # options in ssh command
        ssh_minfilesize = request.form['minfilesize']
        
        #### START prepares ssh commands to run
        
        # lists all files larger than ssh_minfilesize
        ssh_bigfilesall = r"find / -type f -size +" + ssh_minfilesize + r"M -exec ls -lh {} \; 2>/dev/null | awk {'print $5, $9'} | sort -h"
        
        # lists all files in /home/ and /backup/ larger than ssh_minfilesize
        ssh_bigfiles = r"find /home/ /backup/ -type f -size +" + ssh_minfilesize + r"M -exec ls -lh {} \; 2>/dev/null | awk {'print $5, $9'} | sort -h"
        
        # lists largest 20 folders under /home/ 
        ssh_bigdirs = r"du -Sh / 2>/dev/null | sort -rh | head -20"
        
        #### END prepares ssh commands to run
        
        # logs in to host, runs commands, outputs results to new window
        #with shell:
            #result = shell.run(["uptime"])
            #return(result.output)
        return render_template('diskcheck_results.html', 
                ssh_bigdirs=ssh_bigdirs, 
                ssh_bigfiles=ssh_bigfiles, 
                ssh_bigfilesall=ssh_bigfilesall)
                
    return render_template('diskcheck.html',
        title='Disk Usage Check')


# code for the bot and WP attack checking tool
@app.route('/botwpcheck_results')
@app.route('/botwpcheck', methods=['GET', 'POST'])
def wpcheck():
    # triggered when the submit button is pressed
    if request.method == 'POST':
    
        # prepares ssh login
        sshhost = request.form.get('sshhost')
        sshuser = request.form['sshuser']
        sshpass = request.form['sshpass']
        sshport = request.form['sshport']
        shell = spur.SshShell(hostname=sshhost, 
                        username=sshuser, 
                        password=sshpass,
                        port = sshport,
                        missing_host_key=spur.ssh.MissingHostKey.accept)
                        
        #### START prepares ssh commands to run


        #### END prepares ssh commands to run
        
        # logs in to host, runs commands, outputs results to new window
        #with shell:
            #result = shell.run(["uptime"])
            #return(result.output)        
        return render_template('timecheck_results.html')
        
        
    return render_template('botwpcheck.html',
        title='Bot & WP Attack Check')


# code for the "what happened to the server around this time" checking tool
@app.route('/timecheck_results')        
@app.route('/timecheck', methods=['GET', 'POST'])
def timecheck():
    # triggered when the submit button is pressed
    if request.method == 'POST':
    
        # prepares ssh login
        sshhost = request.form.get('sshhost')
        sshuser = request.form['sshuser']
        sshpass = request.form['sshpass']
        sshport = request.form['sshport']
        shell = spur.SshShell(hostname=sshhost, 
                        username=sshuser, 
                        password=sshpass,
                        port = sshport,
                        missing_host_key=spur.ssh.MissingHostKey.accept)
                        
        #### START prepares ssh commands to run                        


        #### END prepares ssh commands to run
        
        # logs in to host, runs commands, outputs results to new window
        #with shell:
            #result = shell.run(["uptime"])
            #return(result.output)
        return render_template('timecheck_results.html')
        
    return render_template('timecheck.html',
        title='Find what happend around a certain time')


# code for the tool that runs custom commands
@app.route('/customcommand_results')        
@app.route('/customcommand', methods=['GET', 'POST'])
def customcommand():
    # triggered when the submit button is pressed
    if request.method == 'POST':
    
        # prepares ssh login
        sshhost = request.form.get('sshhost')
        sshuser = request.form['sshuser']
        sshpass = request.form['sshpass']
        sshport = request.form['sshport']
        shell = spur.SshShell(hostname=sshhost, 
                        username=sshuser, 
                        password=sshpass,
                        port = sshport,
                        missing_host_key=spur.ssh.MissingHostKey.accept)
                        
        #### START prepares ssh commands to run                        


        #### END prepares ssh commands to run

        # logs in to host, runs commands, outputs results to new window
        #with shell:
            #result = shell.run(["uptime"])
            #return(result.output)        
        return render_template('customcommand_results.html')
                        
    return render_template('customcommand.html',
        title='Custom Command')

