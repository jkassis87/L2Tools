from flask import render_template, request, make_response, jsonify
from app import app
import spur, sys, re, geoip2.database, json

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
                
        with shell:
        
            #### START prepares ssh commands to run
            
            # pings the r1soft server 4 times
            com_r1ping = shell.run(["sh", "-c", f"ping -c 4 {sshr1server}"])
            str_r1ping = f"ping -c 4 {sshr1server}"

            # gets the kernel version
            com_kernelver = shell.run(["sh", "-c", "uname -r"])
            str_kernelver = "uname -r"

            # lists installed kernel modules
            com_kernelmods = shell.run(["sh", "-c", r"rpm -qa | grep kernel"])
            str_kernelmods = r"rpm -qa | grep kernel"

            #### END prepares ssh commands to run
            
            # outputs to r1check_results.html and renders the ssh command results
            return render_template('r1check_results.html',
                                com_r1ping=com_r1ping, str_r1ping=str_r1ping,
                                com_kernelver=com_kernelver, str_kernelver=str_kernelver,
                                com_kernelmods=com_kernelmods, str_kernelmods=str_kernelmods)
        
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
                
        with shell:
        
            #### START prepares ssh commands to run
            
            # lists all files larger than ssh_minfilesize under /home/ and /backup/
            com_largefiles = shell.run(["sh", "-c", r"find /home/ /backup/ -type f -size +" + ssh_minfilesize + " -exec ls -lh {} \; | awk {'print $5, $9'}  | sort -h"])
            str_largefiles = r"find /home/ /backup/ -type f -size +" + ssh_minfilesize + " -exec ls -lh {} \; | awk {'print $5, $9'}  | sort -h"
            
            # lists 20 largest folders under /home/ and /backup/
            com_largedirs = shell.run(["sh", "-c", r"du -Sh /home/ /backup/ | sort -rh | head -20"])
            str_largedirs = r"du -Sh /home/ /backup/ | sort -rh | head -20"
            
            #### END prepares ssh commands to run
            
            # outputs to diskcheck_results.html and renders the ssh command results
            return render_template('diskcheck_results.html', 
                                    com_largefiles=com_largefiles, str_largefiles=str_largefiles,
                                    com_largedirs=com_largedirs, str_largedirs=str_largedirs)
                
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
                        
        with shell:
        
            #### START prepares ssh commands to run
            
            # lists all files larger than ssh_minfilesize under /home/ and /backup/
            com_atkcheck = shell.run(["sh", "-c", r"less /home/*/access-logs/* | grep -i 'xmlrpc\|wp-login\|bot' |  awk '{print $1}' | sort | uniq -c | sort -n"])
            str_atkcheck = r"less /home/*/access-logs/* | grep -i 'xmlrpc\|wp-login\|bot' |  awk '{print $1}' | sort | uniq -c | sort -n"
            
            #### END prepares ssh commands to run
            
            ### START converts the com_atkcheck results to a usable dict
            
            # changes com_atkcheck type from binary to multiline str
            a_str = com_atkcheck.output.decode()
            a_str = a_str.splitlines()
            
            # converts atkcheck_str from multiline str to list
            a_str = [re.sub('     ', '', i) for i in a_str]
            
            # turns list into dict
            a_dict = {k:v for k,v in (x.split(' ') for x in a_str) } 
            
            # swaps the key and value
            a_dict = {v:k for (k, v) in a_dict.items()}
            
            # converts value from str into list
            a_dict = {k:[v] for (k, v) in a_dict.items()}
            
            ### END converts the com_atkcheck results to a usable dict
            
            ### START add geoip data to dict
            
            with geoip2.database.Reader('GeoLite2-City.mmdb') as reader:
                for k, v in a_dict.items():
                    print(type(v))
                    response = reader.city(k)
                    i = response.country.name
                    v.append(i)
                
            with geoip2.database.Reader('GeoLite2-ASN.mmdb') as reader:
                for k, v in a_dict.items():
                    print(type(v))
                    response = reader.asn(k)
                    i = response.autonomous_system_organization
                    v.append(i)
            
            ### END add geoip data to dict
            
            # converts the dict to json
            check_results = json.dumps(a_dict, separators=(',', ':')).replace("],", "],\n")
            check_results = check_results.translate(str.maketrans({'{': '', '}': '', '"': '', '[': '', ']': ''}))
            
            # outputs to diskcheck_results.html and renders the ssh command results
            #return jsonify(json.dumps(a_dict))
            return render_template('botwpcheck_results.html',  check_results=check_results)
        
        
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

