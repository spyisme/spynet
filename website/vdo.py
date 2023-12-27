from flask import  render_template, request, redirect, url_for, session , Blueprint, jsonify

import base64
import json
import requests , re 
import subprocess
from pywidevine.cdm import deviceconfig
from pywidevine.cdm import cdm
from flask import copy_current_request_context
import threading

Nawar = 'https://discord.com/api/webhooks/1159805446039797780/bE4xU3lkcjlb4vfCVQ9ky5BS2OuD01Y8g9godljNBfoApGt59-VfKf19GQuMUmH0IYzw'
Bio= "https://discord.com/api/webhooks/1158548096012259422/jQ5sEAZBIrvfBNTA-w4eR-p6Yw0zv7GBC9JTUcEOAWfmqYJXbOpgysATjKPXLwd8HZOs"
Nasser = "https://discord.com/api/webhooks/1158548163209199626/73nAC_d1rgUr6IS79gC508Puood83ho848IEGOpxLtUzGEEJ3h8CyZqlZvCZ6jEXH5k1"
Salama = "https://discord.com/api/webhooks/1158548226971009115/qtBWD8plfY3JFMjCKYrcXwJ8ayMIbUnXFU3_XtbPeXdxGBzb794t8oSKB2WjoN05Lc-j"
Gedo = "https://discord.com/api/webhooks/1158824183833309326/lOGuL_T9mAtYuGCkDRkVxRERIQAD1fHS3RTzxkRmS1ZlzT5yY4C7bi20XdK-1pSXcVzZ"
Else = "https://discord.com/api/webhooks/1158548386392309831/V3d-iMhY0-cwU6TZ9bS8OZZEoKtqicbSzw6AjbB-pUaSiFvr-bEVZduwkwcYzPpIRGCk"





#The code on the html
def generate_input1(mpd, content_key, vidname):
    ffmpegcmd = f"move {vidname}.mp4 ./output"
    input1 = f"app {mpd}\n--key " + "\n--key ".join(content_key) + f"\n--save-name {vidname} -M format=mp4 & {ffmpegcmd}"
    return input1




#get otp from token2
def getotp(token):
    decoded_bytes = base64.b64decode(token)
    decoded_string = decoded_bytes.decode('utf-8')
    data = json.loads(decoded_string)
    otp_value = data.get("otp")
    return (otp_value)



def playback(token):
    decoded_bytes = base64.b64decode(token)
    decoded_string = decoded_bytes.decode('utf-8')
    data = json.loads(decoded_string)
    playbackInfo = data.get("playbackInfo")
    return (playbackInfo)

#Video ID for mpd and pssh
def get_video_id(token: str):
    playback_info = json.loads(base64.b64decode(token))['playbackInfo']
    return json.loads(base64.b64decode(playback_info))['videoId']
#pssh
def get_pssh(mpd: str):
    req = None
    req = requests.get(mpd)
    return re.search('<cenc:pssh>(.*)</cenc:pssh>', req.text).group(1)


#mpd
def get_mpd(video_id: str) -> str:
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
        'origin': 'https://dev.vdocipher.com/',
        'referer': 'https://dev.vdocipher.com/'
    }
    url = 'https://dev.vdocipher.com/api/meta/' + video_id
    req = None
    req = requests.get(url, headers=headers)
    resp = req.json()
    return resp['dash']['manifest']

#Defult

vdo = Blueprint('vdo', __name__)
used_tokens = set()  # Set to store used tokens
usernames = ['spy'] 
secrectoken = "omgspyissocool"
@vdo.route('/vdocipher', methods=['GET', 'POST'])
def index():
    mytoken = request.args.get('token')
    spy = request.args.get('spy')
    username = request.args.get('username')
    secrectokens = request.args.get('secrectokens')
    if mytoken in used_tokens:
        return jsonify({'error': 'Token already used'}), 400
    if username not in  usernames:
        return jsonify({'error': 'Provide a username'}), 400
    if secrectokens !=secrectoken :
        return jsonify({'error': 'Provide the token'}), 400
    class WvDecrypt:
        def __init__(self, pssh_b64, device):
            self.cdm = cdm.Cdm()
            self.session = self.cdm.open_session(pssh_b64, device)
    
        def create_challenge(self):
            challenge = self.cdm.get_license_request(self.session)
            return challenge
    
        def decrypt_license(self, license_b64):
            if self.cdm.provide_license(self.session, license_b64) == 1:
                raise ValueError
    
        def set_server_certificate(self, certificate_b64):
            if self.cdm.set_service_certificate(self.session, certificate_b64) == 1:
                raise ValueError
    
        def get_content_key(self):
            content_keys = []
            for key in self.cdm.get_keys(self.session):
                if key.type == 'CONTENT':
                    kid = key.kid.hex()
                    key = key.key.hex()
    
                    content_keys.append('{}:{}'.format(kid, key))
    
            return content_keys
    
        def get_signing_key(self):
            for key in self.cdm.get_keys(self.session):
                if key.type == 'SIGNING':
                    kid = key.kid.hex()
                    key = key.key.hex()
    
                    signing_key = '{}:{}'.format(kid, key)
                    return signing_key
    
    def headers():

        return {
        'Content-Type': "application/json",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "en-US,en;q=0.9",
        "connection": "keep-alive",
        "host": "player.vdocipher.com",
    #   "referer": "https://dashboard.elhusseinyusmleprep.com/",
        "sec-ch-ua-mobile": "?1",
        "sec-ch-ua-platform": "Android",
        "sec-fetch-dest": "iframe",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "cross-site",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": '1',
        "user-agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36"
    }
    
    
    class Pyd:
        def __init__(self) -> None:
            pass

        def post_license_request(self, link, challenge, data):
            if challenge == "":
                enoded = base64.b64encode(challenge.encode()).decode()
            else:
                enoded = base64.b64encode(challenge).decode()
            myotp = getotp(mytoken)
            data['otp'] = f"{myotp}"
            data["licenseRequest"] = enoded
            
            payload_new = {
                'token': base64.b64encode(json.dumps(data).encode("utf-8")).decode('utf-8')
            }
            r = requests.post(link, json=payload_new, headers=headers())
            return r.json()['license']
    
        def start(self):
            license_url = "https://license.vdocipher.com/auth"
            video_id = get_video_id(mytoken)
            mpd = get_mpd(video_id)
            pssh = get_pssh(mpd)
            pssh_b64 = f"{pssh}"
            data = {"token":f"{mytoken}"}
            data = eval(base64.b64decode(data['token']).decode())
            wvdecrypt = WvDecrypt(pssh_b64, deviceconfig.DeviceConfig(deviceconfig.device_android_generic))
            wvdecrypt.set_server_certificate(self.post_license_request(license_url, '', data))
            challenge = wvdecrypt.create_challenge()
            license = self.post_license_request(license_url, challenge, data)
            wvdecrypt.decrypt_license(license)
            content_key = wvdecrypt.get_content_key()
            return content_key 
        
    video_id = get_video_id(mytoken)
    mpd = get_mpd(video_id)
    content_key = Pyd().start()

    #code = generate_input1(mpd, content_key, "vidname")
    content_key_lines = '\n'.join([f'--key {key}' for key in content_key])
    result = mpd + '\n' + content_key_lines 
    # print(result)
    session['result'] = result
    options = []
    if spy :
        options = ['Else','Nawar','Nasser-El-Batal', 'MoSalama', 'Gedo' , 'Bio']
    used_tokens.add(mytoken)
    session['result'] = result
    session['spy'] = spy
    return render_template('backend_pages/vdo.html' , content_key = content_key , mpd = mpd ,options = options ,spy = spy)




cmds_queue = []

#Discord webhook , The webpage



@vdo.route('/form', methods=['POST'])
def form():
    options = ['Nawar', 'Nasser-El-Batal', 'MoSalama' , 'Bio', 'Else']
    spy = session.get('spy')
    route = "vdo.discord"
    if spy :
        route = "vdo.discord2"
    if request.method == 'POST':
        user_data = {
            'teacher' : request.form.get('dropdown'),
            'name': request.form['vidname']
        }
        return redirect(url_for(f'{route}', **user_data))
    return render_template('backend_pages/vdo.html', option = options)


@vdo.route('/discord2', methods=['GET', 'POST'])
def discord2():
    result = session.get('result')
    name = request.args.get('name')
    result = result.replace("\n", " ")
    teacher = request.args.get('teacher')
    message = {
            'content': f'```app {result} --save-name {name} -M format=mp4 --auto-select --no-log  & move {name}.mp4 ./output``` {name} '
        }
    payload = json.dumps(message)
    userinput = f"app {result} --save-name {name} -M format=mp4 --auto-select --no-log  & move {name}.mp4 ./output"
    cmds_queue.append(userinput)
    headers = {'Content-Type': 'application/json'}
    teacher_webhooks = {
        "Nawar": Nawar,
        "Nasser-El-Batal": Nasser,
        "MoSalama": Salama,
        "Bio": Bio,
        "Gedo": Gedo,
    }
    webhook_url = teacher_webhooks.get(teacher, Else)
    requests.post(webhook_url, data=payload, headers=headers)
    session.pop('spy', None)

    return 'Message Sent! <a href="https://discord.gg/vKBnMy5yUe">Discord server</a>'



@vdo.route('/discord', methods=['GET', 'POST'])
def discord():
    result = session.get('result')
    name = request.args.get('name')
    result = result.replace("\n", " ")
    message = {
            'content': f'```app {result} --save-name {name} -M format=mp4 --auto-select --no-log  & move {name}.mp4 ./output``` {name} '
        }
    payload = json.dumps(message)
    userinput = f"app {result} --save-name {name} -M format=mp4 --auto-select --no-log  & move {name}.mp4 ./output"
    cmds_queue.append(userinput)
    headers = {'Content-Type': 'application/json'}
    requests.post("https://discord.com/api/webhooks/1180085907668357161/loJp3PkaHiS_HCfyWy42QisFFiOGj__XXuApZyecvdTzTwWF_C121gZws0z9EiaBgO6i", data=payload, headers=headers)

    return redirect(url_for('vdo.commandslist'))



#-------------------------------------------------------------------------------------
import threading


storj_lock = threading.Lock()


used_mpd = set()  # Set to store used tokens
 

def storjsingle(command):
    if storj_lock.acquire(blocking=False):
        try :
            def senddiscrdmsg(content):
                message = {
                        'content': f'{content}'
                    }
                payload = json.dumps(message)
                headers = {'Content-Type': 'application/json'}
                requests.post("https://discord.com/api/webhooks/1177648648172093562/8PN6BS5c4l4tST5H_jtunzO46iiigz1zyEI34nPbWN_Q7IKJjQKIEYLdb6OXYpwVofwp", data=payload, headers=headers)

            def run_command(command):
                subprocess.run(command, shell=True)

            def extract_save_name(command):
                save_name_match = re.search(r'--save-name\s+(\S+)', command)
                if save_name_match:
                    return save_name_match.group(1)
                else:
                    return None
            cmd = command
            mpd = cmd.split(" ")[1]
            if mpd in used_mpd:
                    return "failed"      
            used_mpd.add(mpd)
            video_name = extract_save_name(cmd)

            if video_name :
                command2 = f"uplink.exe cp ./output/{video_name}.mp4 sj://spynet/Private/"
                command4 = fr"del .\output\{video_name}.mp4"

                # Download to local pc
                senddiscrdmsg(f"Downloading the video... {video_name}")
                run_command(cmd)

                # Upload to stoj
                run_command(f"move {video_name}.mp4 ./output")
                senddiscrdmsg("Uploading the video...")
                run_command(command2)

                # Cleanup
                # senddiscrdmsg("Deleting the video...")
                run_command(command4)
                run_command("cls")
                run_command("echo Running!")
                senddiscrdmsg("Done !")
                if command in cmds_queue:
                    cmds_queue.remove(command)
             #Incase no video name   
            else : 
                print("Wrong cmd")
                run_command("cls")
                run_command("echo Running!")
                if command in cmds_queue:
                    cmds_queue.remove(command)
        finally:
            storj_lock.release()

def senddiscrdmsg(content):
    message = {
            'content': f'{content}'
        }
    payload = json.dumps(message)
    headers = {'Content-Type': 'application/json'}
    requests.post("https://discord.com/api/webhooks/1185957394526781491/-nQ6rLQ1Vlo8El7VB9of0waEU9A4mTKBJfrla8Po7F9UelL_HVfkhy9pIGN9pU8ZEMv4", data=payload, headers=headers)

def storj():
    if storj_lock.acquire(blocking=False):
        try :
            if cmds_queue :
                while len(cmds_queue) > 0:
                    def senddiscrdmsg(content):
                        message = {
                                'content': f'{content}'
                            }
                        payload = json.dumps(message)
                        headers = {'Content-Type': 'application/json'}
                        requests.post("https://discord.com/api/webhooks/1177648648172093562/8PN6BS5c4l4tST5H_jtunzO46iiigz1zyEI34nPbWN_Q7IKJjQKIEYLdb6OXYpwVofwp", data=payload, headers=headers)

                    def run_command(command):
                        subprocess.run(command, shell=True)

                    def extract_save_name(command):
                        save_name_match = re.search(r'--save-name\s+(\S+)', command)
                        if save_name_match:
                            return save_name_match.group(1)
                        else:
                            return None

                    cmd = cmds_queue[0]
                    mpd = cmd.split(" ")[1]
                    if mpd in used_mpd:
                            return "failed"
                    used_mpd.add(mpd)
                    video_name = extract_save_name(cmd)
                    if video_name :
                        command2 = f"uplink.exe cp ./output/{video_name}.mp4 sj://spynet/Private/"
                        command4 = fr"del .\output\{video_name}.mp4"

                        senddiscrdmsg(f"Downloading the video... {video_name}")
                        run_command(cmd)

                        senddiscrdmsg("Uploading the video...")
                        run_command(command2)

                        run_command(command4)
                        run_command("cls")
                        run_command("echo Running!")
                        senddiscrdmsg("Done !")

                        del cmds_queue[0]
                    else : 
                        print("Wrong cmd")
                        run_command("cls")
                        run_command("echo Running!")
                        del cmds_queue[0]
        finally:
            storj_lock.release()
        







@vdo.route("/list")
def commandslist():
    def extract_save_name(command):
        save_name_match = re.search(r'--save-name\s+(\S+)', command)
        if save_name_match:
            return save_name_match.group(1)
        else:
            return None
    return render_template("backend_pages/list.html", cmds_queue=cmds_queue, extract_save_name=extract_save_name)

from flask import render_template

@vdo.route('/downloadsingle', methods=['GET'])
def downloadsingle():
    command = request.args.get('command')
    
    # Check the status before proceeding
    storj_lock_acquired = storj_lock.acquire(blocking=False)
    storj_lock.release()

    if storj_lock_acquired:
        return render_template('backend_pages/loading.html', command=command , word = "Loading...")
    else:
        return render_template('backend_pages/loading.html' , word = "The resource is currently in use.")


@vdo.route('/start_background_task', methods=['POST'])
def start_background_task():
    command = request.args.get('command')
    storjsingle(command)
    return jsonify({'status': f'Video uploaded successfully'})


@vdo.route('/start_background_task_all', methods=['POST'])
def start_background_task_all():
    storj()
    return jsonify({'status': f'Videos uploaded successfully'})


@vdo.route('/downloadall', methods=['GET'])
def downloadall():
    storj_lock_acquired = storj_lock.acquire(blocking=False)
    storj_lock.release()

    if storj_lock_acquired:
        return render_template('backend_pages/loading_all.html', word = "Loading... (This will take long)")
    else:
        return render_template('backend_pages/loading_all.html' , word = "The resource is currently in use.")





@vdo.route('/deletecmd', methods=['GET'])
def delete_command():
    command_to_delete = request.args.get('command')
    if command_to_delete in cmds_queue:
        cmds_queue.remove(command_to_delete)
    return redirect(url_for('vdo.commandslist'))

@vdo.route("/status")
def lock_status():
    storj_lock_acquired = storj_lock.acquire(blocking=False)
    storj_lock.release()
    return f'{"Ready to use" if storj_lock_acquired else "Locked"}'



#Manual command add
@vdo.route("/storj2", methods=['GET', 'POST'])
def storjflask2():
    if request.method == 'POST':
        userinput = request.form['userinput']
        cmds_queue.append(userinput)
        return redirect(url_for('vdo.commandslist'))

    return render_template("backend_pages/storj.html")




@vdo.route("/clear")
def storjlist():
        cmds_queue.clear()
        return "done"


@vdo.route("/createcmd")
def cmdcommand():
        combined_cmds = " & ".join([f'start cmd.exe @cmd /k "{element} & exit"' for element in cmds_queue])
        return combined_cmds

@vdo.route("/cleartokens")
def cleartokens():
        used_tokens.clear()
        return "done"





from flask import send_file

@vdo.route("/vdo")
def vdofile():
    file_path = r'storj\vdo.txt'
    return send_file(file_path, as_attachment=True)











#--------------------------------------------------------------------------
def getv(token):
    decoded_bytes = base64.b64decode(token)
    decoded_string = decoded_bytes.decode('utf-8')
    data = json.loads(decoded_string)
    v = data.get("v")
    return (v)



#pssh
def get_pssh(mpd: str):
    req = None
    req = requests.get(mpd)
    return re.search('<cenc:pssh>(.*)</cenc:pssh>', req.text).group(1)



#mpd
def get_mpd2(video_id , xotp):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
        'origin': 'https://resource.inkryptvideos.com',
        'referer': 'https://resource.inkryptvideos.com/',
        'X-Otp' : f'{xotp}'
    }
    url = 'https://api.inkryptvideos.com/api/s1/v_info/' + video_id
    req = None
    req = requests.get(url, headers=headers)
    req.raise_for_status()  # Raise an exception if the request fails
    resp = req.json()
    storage_hostname = resp['data']['storage_hostname']
    dash_manifest = resp['data']['dash_manifest'].replace("\\", "")
    full_url = f"https://{storage_hostname}/{dash_manifest}"
    return full_url



@vdo.route('/ink', methods=['GET', 'POST'])
def ink():
    token = request.args.get('token')
    xotp = request.args.get('otp')
    username = request.args.get('username')
    secrectokens = request.args.get('secrectokens')
    if username not in  usernames:
        return jsonify({'error': 'Provide a username'}), 400
    if secrectokens !=secrectoken :
        return jsonify({'error': 'Provide the token'}), 400 
    class WvDecrypt:
        def __init__(self, pssh_b64, device):
            self.cdm = cdm.Cdm()
            self.session = self.cdm.open_session(pssh_b64, device)

        def create_challenge(self):
            challenge = self.cdm.get_license_request(self.session)
            return challenge

        def decrypt_license(self, license_b64):
            if self.cdm.provide_license(self.session, license_b64) == 1:
                raise ValueError

        def set_server_certificate(self, certificate_b64):
            if self.cdm.set_service_certificate(self.session, certificate_b64) == 1:
                raise ValueError

        def get_content_key(self):
            content_keys = []
            for key in self.cdm.get_keys(self.session):
                if key.type == 'CONTENT':
                    kid = key.kid.hex()
                    key = key.key.hex()
                    content_keys.append('{}:{}'.format(kid, key))

            return content_keys

        def get_signing_key(self):
            for key in self.cdm.get_keys(self.session):
                if key.type == 'SIGNING':
                    kid = key.kid.hex()
                    key = key.key.hex()

                    signing_key = '{}:{}'.format(kid, key)
                    return signing_key

    def headers():
        
        return {
        'sec-ch-ua': '"Google Chrome";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
        'x-version': '2.1.63',
        'x-otp': f'{xotp}',
        'sec-ch-ua-mobile': '?0',
        #'ink-ref': 'https://mrredaelfarouk.com/lectures/progress/5',
        'content-type': 'application/json',
        'Referer': 'https://resource.inkryptvideos.com/',
        'sec-ch-ua-platform': '"Windows"',
    }


    class Pyd:
        def __init__(self) -> None:
            pass

        def post_license_request(self, link, challenge, data):
            if challenge == "":
                enoded = base64.b64encode(challenge.encode()).decode()
            else:
                enoded = base64.b64encode(challenge).decode()
            newv = getv(token)
            g = {"v" : f"{newv}",  
                    "c" : enoded}
            payload_new = {'token': base64.b64encode(json.dumps(g).encode()).decode()}
            r = requests.post(link, json=payload_new, headers=headers())
            return r.json()['l']

        def start(self):
            newv = getv(token)
            mpd = get_mpd2(newv , xotp)
            pssh = get_pssh(mpd)
            license_url = "https://license.inkryptvideos.com/api/v1/wj/license"
            pssh_b64 = f"{pssh}"
            data = {"token":f"{token}"}
            data = eval(base64.b64decode(data['token']).decode())
            wvdecrypt = WvDecrypt(pssh_b64, deviceconfig.DeviceConfig(deviceconfig.device_android_generic))
            wvdecrypt.set_server_certificate(self.post_license_request(license_url, '', data))
            challenge = wvdecrypt.create_challenge()
            license = self.post_license_request(license_url, challenge, data)
            wvdecrypt.decrypt_license(license)
            content_key = wvdecrypt.get_content_key()

            return content_key , mpd

    content_key , mpd = Pyd().start()

    content_key_lines = '\n'.join([f'--key {key}' for key in content_key])
    result = mpd + '\n' + content_key_lines
    session['result'] = result
    return render_template('backend_pages/ink.html', content_key=content_key , mpd = mpd ,input1 = result)







#END PAGE



@vdo.route('/inkform', methods=['POST'])
def inkform():
    if request.method == 'POST':
        user_data = {
            'name': request.form['vidname']
        }
        return redirect(url_for('vdo.discordink', **user_data))
    return render_template('backend_pages/ink.html')


@vdo.route('/inkdiscord', methods=['GET', 'POST'])
def discordink():
    result = session.get('result')
    name = request.args.get('name')
    result = result.replace("\n", " ")

    msg = f'app {result} --save-name {name} -M format=mp4 --auto-select --no-log  & move {name}.mp4 ./output'
    message = {
            'content': f'```{msg}```{name}'
        }
    payload = json.dumps(message)
    headers = {'Content-Type': 'application/json'}
    cmds_queue.append(msg)
    requests.post("https://discord.com/api/webhooks/1158824183833309326/lOGuL_T9mAtYuGCkDRkVxRERIQAD1fHS3RTzxkRmS1ZlzT5yY4C7bi20XdK-1pSXcVzZ", data=payload, headers=headers)
    return "Message Sent!" 
