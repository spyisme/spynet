from flask import  render_template, request, redirect, url_for, session , Blueprint, jsonify
import base64
import json
import requests , re 
from pywidevine.cdm import deviceconfig
from pywidevine.cdm import cdm
from flask_login import  current_user
from flask import send_file
Nawar = 'https://discord.com/api/webhooks/1159805446039797780/bE4xU3lkcjlb4vfCVQ9ky5BS2OuD01Y8g9godljNBfoApGt59-VfKf19GQuMUmH0IYzw'
Bio= "https://discord.com/api/webhooks/1158548096012259422/jQ5sEAZBIrvfBNTA-w4eR-p6Yw0zv7GBC9JTUcEOAWfmqYJXbOpgysATjKPXLwd8HZOs"
Nasser = "https://discord.com/api/webhooks/1158548163209199626/73nAC_d1rgUr6IS79gC508Puood83ho848IEGOpxLtUzGEEJ3h8CyZqlZvCZ6jEXH5k1"
Salama = "https://discord.com/api/webhooks/1158548226971009115/qtBWD8plfY3JFMjCKYrcXwJ8ayMIbUnXFU3_XtbPeXdxGBzb794t8oSKB2WjoN05Lc-j"
Gedo = "https://discord.com/api/webhooks/1158824183833309326/lOGuL_T9mAtYuGCkDRkVxRERIQAD1fHS3RTzxkRmS1ZlzT5yY4C7bi20XdK-1pSXcVzZ"
Else = "https://discord.com/api/webhooks/1201174140770586655/d3VuNRT1j0xyTajwMC7gKIwfGDywENK1MaAtjhtJ02Okv-Xf0X5ROMuvhaAArEVG_iZc"
Logs = "https://discord.com/api/webhooks/1199384528553254983/-wZ9h7YobG3IHZBRZKtzPI5ZcAHpHvMYM-ajpJ87ZzXWTWvu2Upkk7_YaYi3X66QaUJL"




#Defult

vdo = Blueprint('vdo', __name__)
used_tokens = set()  # Set to store used tokens



#Base 64 tokens 
def base64url_to_text(encoded_str):
    encoded_str = encoded_str.replace('-', '+').replace('_', '/')
    while len(encoded_str) % 4 != 0:
        encoded_str += '='
    decoded_bytes = base64.b64decode(encoded_str)
    decoded_text = decoded_bytes.decode('utf-8')
    return decoded_text

#get otp from token2
def getotp(token):
    # decoded_bytes = base64.b64decode(token)
    decoded_string = base64url_to_text(token)
    data = json.loads(decoded_string)
    otp_value = data.get("otp")
    return (otp_value)


#ban our-matrix :
def gethref(token):
    # decoded_bytes = base64.b64decode(token)
    decoded_string = base64url_to_text(token)
    data = json.loads(decoded_string)
    href = data.get("href")
    return (href)



def playback(token):
    # decoded_bytes = base64.b64decode(token)
    decoded_string = base64url_to_text(token)
    data = json.loads(decoded_string)
    playbackInfo = data.get("playbackInfo")
    return (playbackInfo)

#Video ID for mpd and pssh
def get_video_id(token: str):
    playback_info = json.loads(base64url_to_text(token))['playbackInfo']
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


#log
def discord_log(message):
    messageeeee = { 'content': message }
    payload = json.dumps(messageeeee)
    headers = {'Content-Type': 'application/json'}
    requests.post("https://discord.com/api/webhooks/1199384528553254983/-wZ9h7YobG3IHZBRZKtzPI5ZcAHpHvMYM-ajpJ87ZzXWTWvu2Upkk7_YaYi3X66QaUJL", data=payload, headers=headers)



@vdo.route('/vdocipher', methods=['GET', 'POST'])
def index():
    mytoken = request.args.get('token')
    tokenhref = gethref(mytoken)
    if current_user != 'spy' :
        if "our-matrix.com" in tokenhref :
            return jsonify({'error': 'Salama no longer works'}), 400
        
    if request.method != 'POST':
        if mytoken in used_tokens:
            return jsonify({'error': 'Token already used'}), 400
        
    # if current_user.username not in ['spy', 'skailler' , 'feteera'] :
    #     client_ip = request.headers.get('CF-Connecting-IP', request.remote_addr)
    #     discord_log(f"{current_user.username} tried opening /vdocipher | Ip : {client_ip}")
    #     return redirect(url_for('views.home'))

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
            print(r)
            discord_log(r)
            return r.json()['license']
    
        def start(self):
            client_ip = request.headers.get('CF-Connecting-IP', request.remote_addr)
            discord_log(f"Api got used by {current_user.username} | IP : {client_ip}")
            license_url = "https://license.vdocipher.com/auth"
            video_id = get_video_id(mytoken)
            mpd = get_mpd(video_id)
            pssh = get_pssh(mpd)
            pssh_b64 = f"{pssh}"
            data = {"token":f"{mytoken}"}
            data = eval(base64url_to_text(data['token']))
            wvdecrypt = WvDecrypt(pssh_b64, deviceconfig.DeviceConfig(deviceconfig.device_android_generic))
            wvdecrypt.set_server_certificate(self.post_license_request(license_url, '', data))
            challenge = wvdecrypt.create_challenge()
            license = self.post_license_request(license_url, challenge, data)
            wvdecrypt.decrypt_license(license)
            content_key = wvdecrypt.get_content_key()
            return content_key 
    #Video id to get mpd and send it    
    video_id = get_video_id(mytoken)
    mpd = get_mpd(video_id)
    content_key = Pyd().start()

    content_key_lines = '\n'.join([f'--key {key}' for key in content_key])
    result = mpd + '\n' + content_key_lines 
    used_tokens.add(mytoken)
    session['result'] = result



    # Extracting keys and creating url to view online 

    components = result.split()
    input_url = components[0]
    components = result.split("--key")[1:]
    keys = [key.strip() for key in components[1:]]
    ckvaluetobeused = {}
    for key in keys:
        parts = key.split(":")
        if len(parts) == 2:
            ckvaluetobeused[parts[0]] = parts[1]

    keysbase64 = base64.urlsafe_b64encode(str(ckvaluetobeused).encode()).decode()

    url = input_url + "?ck=" + keysbase64

    session['urlopen'] = url

    discord_log(url)

    options = ['Else','Nawar','Nasser-El-Batal', 'Gedo' , 'Bio' , 'Sameh-Nash2t']

    if "samehnashaat" in tokenhref :
        options = ['Sameh-Nash2t','Bio','Nawar','Nasser-El-Batal', 'Gedo' , 'Else']

    if "ednuva" in tokenhref :
        options = ['Bio','Nawar','Nasser-El-Batal', 'Gedo' , 'Else' , 'Sameh-Nash2t']
            
    if "chemistry" in tokenhref :
        options = ['Nasser-El-Batal', 'Else','Nawar', 'Gedo' , 'Bio', 'Sameh-Nash2t']
        
    if "class" in tokenhref : #classwork of nasser
        options = ['Nasser-El-Batal', 'Else','Nawar', 'Gedo' , 'Bio' , 'Sameh-Nash2t']

    if "mrredaelfarouk" in tokenhref :
        options = ['Gedo','Nawar','Nasser-El-Batal', 'Else' , 'Bio' , 'Sameh-Nash2t']
    if "nawar" in tokenhref :
        options = ['Nawar','Else','Nasser-El-Batal', 'Gedo' , 'Bio', 'Sameh-Nash2t']






    old = request.args.get('old')

    if old != "true" :
        status  = "new"
        if request.method == 'POST':
            name =  request.form.get('vidname')
            teacher =  request.form.get('dropdown')

            result = result.replace("\n", " ")
            message = {
                    'content': f'```app {result} --save-name {name} -M format=mp4 --auto-select --no-log  & move {name}.mp4 ./output``` {name} ```watch now``` {url}'
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
            return 'Message Sent!'
    else :
         status  = "old"    
   
    return render_template('backend_pages/vdo.html' , content_key = content_key , mpd = mpd ,options = options, result= result , url = url , status = status )




cmds_queue = []

#Discord webhook , The webpage




@vdo.route('/form', methods=['POST'])
def form():
    options = ['Nawar', 'Nasser-El-Batal', 'MoSalama' , 'Bio', 'Else']
    if request.method == 'POST':
        user_data = {
            'teacher' : request.form.get('dropdown'),
            'name': request.form['vidname']
        }
        return redirect(url_for('vdo.discord', **user_data))
    return render_template('index.html' , option = options)


@vdo.route('/vdodiscord', methods=['GET', 'POST'])
def discord():
    result = session.get('result')
    urlopen = session.get('urlopen')
    name = request.args.get('name')
    result = result.replace("\n", " ")
    teacher = request.args.get('teacher')
    message = {
            'content': f'```app {result} --save-name {name} -M format=mp4 --auto-select --no-log  & move {name}.mp4 ./output``` {name} ```watch now``` {urlopen}'
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
        "Sameh-Nash2t" : "https://discord.com/api/webhooks/1226090203760955433/DkaAHvw-ZnTlUhaHEslmpXbSi45x-5nf9cZJ3MLbkjooaSNSOtYwOY2Jb70jGDjaRI9W",
    }
    webhook_url = teacher_webhooks.get(teacher, Else)
    requests.post(webhook_url, data=payload, headers=headers)

    return 'Message Sent!'



@vdo.route('/iframes', methods=['GET', 'POST'])
def iframevids():
    url = request.args.get('url')
    name = request.args.get('name')
    sname = request.args.get('sname')

    if name == "nawar":
      webhook_url ="https://discord.com/api/webhooks/1159805446039797780/bE4xU3lkcjlb4vfCVQ9ky5BS2OuD01Y8g9godljNBfoApGt59-VfKf19GQuMUmH0IYzw"
    elif name == "ahmadsalah":
      webhook_url = "https://discord.com/api/webhooks/1170733207835115630/MpyyTLirCjBUOSHxisTsb4l7lqF7XBw-l4KEsi7DAFLAoZdUzMtGFwth67Qj3ZJCE5Oo"
    elif name == "sherbo":
      webhook_url="https://discord.com/api/webhooks/1169342540575670292/crazeFe5z0qAozWBJOnlZfevMMQ219NVzZ-Cl6mWK9NrtBqBXc3kBzj1tJ8_KVu7UuKf" 
    url = url.replace("/play/", "/embed/")
    if request.method == 'POST':
        name =  request.form.get('name')
        if "youtube" in url.lower() or "youtu.be" in url.lower():
            url = url.split('/')[4]

            msg = f'```python youtube.py https://www.youtube.com/watch?v={url} {name}``` {name}'
            cmds_queue.append(f"python youtube.py https://www.youtube.com/watch?v={url} {name}")
        else: 
            url = url.split('?')[0]
            msg = f'```python iframe.py {url} {name}``` {name}'
            cmds_queue.append(f"python iframe.py {url} {name}")

        message = {
                'content': f'{msg}'
            }
        payload = json.dumps(message)
        headers = {'Content-Type': 'application/json'}
        requests.post(webhook_url, data=payload, headers=headers)
        return "Message Sent!" 
    return render_template('backend_pages/iframe.html' , url = url , sname= sname)






@vdo.route('/watchit', methods=['GET', 'POST'])
def watchit():
    url = request.args.get('url')
    webhook_url="https://discord.com/api/webhooks/1197986558368825444/Q7kjJ3twI6GkOAqRAppGBlEtGR2I5egr98lX-Gh7D2JByHk1ePNBTVYKnjCtiHhIZ8U3" 
    if request.method == 'POST':
        name =  request.form.get('name')
        msg = f'```app {url} --save-name {name} -M format=mp4 --auto-select --no-log  & move {name}.mp4 ./output``` {name}'
        cmds_queue.append(f'app {url}  --save-name {name} -M format=mp4 --auto-select --no-log  & move {name}.mp4 ./output')

        message = {
                'content': f'{msg}'
            }
        payload = json.dumps(message)
        headers = {'Content-Type': 'application/json'}
        requests.post(webhook_url, data=payload, headers=headers)
        return "Message Sent!" 
    return render_template('backend_pages/iframe.html')

@vdo.route('/iframem3u8', methods=['GET', 'POST'])
def hosssamsameh():
    url = request.args.get('url')
    url = "/".join(url.split("/")[:4]) + "/playlist.m3u8"
    



    webhook_url="https://discord.com/api/webhooks/1224528158741626901/mIG58hd-FLTe79XHUsgwE0BxyyKjL2JFs9RyHfLBRfyM1v85YbkJGEzcJyQQVOsfhpRc" 
    if request.method == 'POST':
        name =  request.form.get('name')
        msg = f'```app {url} --header "User-Agent: Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0" --header "Referer: https://iframe.mediadelivery.net/" --save-name {name} -M format=mp4 --auto-select --no-log  & move {name}.mp4 ./output``` {name}'
        cmds_queue.append(f'app {url} --header "User-Agent: Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0" --header "Referer: https://iframe.mediadelivery.net/" --save-name {name} -M format=mp4 --auto-select --no-log  & move {name}.mp4 ./output')

        message = {
                'content': f'{msg}'
            }
        payload = json.dumps(message)
        headers = {'Content-Type': 'application/json'}
        requests.post(webhook_url, data=payload, headers=headers)
        return "Message Sent!" 
    return render_template('backend_pages/iframe.html' , url = url)




import base64


@vdo.route('/shahid', methods=['GET', 'POST'])
def shahid():
    licurl = request.args.get('licurl')
    mpd = request.args.get('mpd')
    pssh = base64.b64decode(request.args.get('pssh'))
    pssh = pssh.decode('utf-8')
    api_url = "https://keysdb.net/api"
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (Ktesttemp, like Gecko) Chrome/90.0.4430.85 Safari/537.36",
        "Content-Type": "application/json",
        "X-API-Key": 'c13cf813a7a384b56f5b5249d6fc0d113e3d981b3af7ee3b1409ff33fe452b15',
    }
    payload = {
        "license_url": licurl,
        "pssh": pssh,
    }
    response = requests.post(api_url, headers=headers, json=payload)
    response_json = response.json()
    keys = response_json["keys"]
    for key in keys:
        key_value = key["key"]

    ckvaluetobeused = {}
    parts = key_value.split(":")
    if len(parts) == 2:
        ckvaluetobeused[parts[0]] = parts[1]
    keysbase64 = base64.urlsafe_b64encode(str(ckvaluetobeused).encode()).decode()   
    if request.method == 'POST':
        name =  request.form.get('name')
        msg = f'```app {mpd} --key {key_value} --save-name {name} -M format=mp4 --no-log  & move {name}.mp4 ./output``` {name} ```watch now``` {mpd}&ck={keysbase64}'
        cmds_queue.append(f"app {mpd}  --key {key_value}  --save-name {name} -M format=mp4 --no-log  & move {name}.mp4 ./output")

        message = {
                'content': f'{msg}'
            }
        payload = json.dumps(message)
        headers = {'Content-Type': 'application/json'}
        requests.post("https://discord.com/api/webhooks/1217535086002573332/UZWHTP2ZPVUdIuOTBG-PVVHyi1bxaa8p_xDNVfeXvTS7_p72a0iVWmJkEoeHaxVowrbr", data=payload, headers=headers)
        return "Message Sent!" 
    return render_template('backend_pages/shahid.html' , mpd = mpd , key =key_value , pssh = pssh  , url = f"{mpd}&ck={keysbase64}")






# from pywidevine.L3.cdm import cdm, deviceconfig
# from base64 import b64encode
# from pywidevine.L3.getPSSH import get_pssh
# from pywidevine.L3.decrypt.wvdecryptcustom import WvDecrypt


# @vdo.route('/spotify', methods=['GET', 'POST'])
# def spotify():
#     lic_url = "https://gew1-spclient.spotify.com/widevine-license/v1/audio/license"

#     pssh = base64.b64decode(request.args.get('pssh'))
#     pssh = pssh.decode('utf-8')
#     auth = base64.b64decode(request.args.get('auth'))
#     auth = auth.decode('utf-8')

#     headers = {'Authorization': f'{auth}'}

#     def WV_Function(pssh, lic_url ,cert_b64=None):
#         wvdecrypt = WvDecrypt(init_data_b64=pssh, cert_data_b64=cert_b64, device=deviceconfig.device_android_generic)                   
#         widevine_license = requests.post(url=lic_url, headers=headers, data=wvdecrypt.get_challenge())

#         print(widevine_license.text)


#         license_b64 = b64encode(widevine_license.content)

#         wvdecrypt.update_license(license_b64)

#         Correct, keyswvdecrypt = wvdecrypt.start_process()

#         if Correct:
#             return Correct, keyswvdecrypt   
#     keys = WV_Function(pssh, lic_url)

#     return keys





#-------------------------------------------------------------------------------------






@vdo.route("/list")
def commandslist():
    def extract_save_name(command):
        if command.startswith("python"):
            return command.split(' ')[3]
        else:
            save_name_match = re.search(r'--save-name\s+(\S+)', command)
            return save_name_match.group(1)
    
    return render_template("backend_pages/list.html",count = len(cmds_queue) ,cmds_queue=cmds_queue, extract_save_name=extract_save_name)

from flask import render_template





@vdo.route('/deletecmd', methods=['GET'])
def delete_command():
    command_to_delete = request.args.get('command')
    if command_to_delete in cmds_queue:
        cmds_queue.remove(command_to_delete)
    return redirect(url_for('vdo.commandslist'))



@vdo.route("/addcmd", methods=['GET', 'POST'])
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
        combined_cmds = " & ".join([f'start cmd.exe @cmd /k "{element} & exit"' for element in cmds_queue]) + "& exit"
        return combined_cmds

@vdo.route("/cleartokens")
def cleartokens():
        used_tokens.clear()
        return "done"




#----------------------------------------------------------------------------------------------------------------
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
