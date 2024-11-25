from flask import render_template, request, redirect, url_for, session, Blueprint, jsonify
import base64
import json
import requests, re
from flask_login import current_user
# Import dependencies
from pywidevine import PSSH
from pywidevine import Cdm
from pywidevine import Device
import os

Nawar = 'https://discord.com/api/webhooks/1159805446039797780/bE4xU3lkcjlb4vfCVQ9ky5BS2OuD01Y8g9godljNBfoApGt59-VfKf19GQuMUmH0IYzw'
Bio = "https://discord.com/api/webhooks/1158548096012259422/jQ5sEAZBIrvfBNTA-w4eR-p6Yw0zv7GBC9JTUcEOAWfmqYJXbOpgysATjKPXLwd8HZOs"
Nasser = "https://discord.com/api/webhooks/1158548163209199626/73nAC_d1rgUr6IS79gC508Puood83ho848IEGOpxLtUzGEEJ3h8CyZqlZvCZ6jEXH5k1"
Salama = "https://discord.com/api/webhooks/1158548226971009115/qtBWD8plfY3JFMjCKYrcXwJ8ayMIbUnXFU3_XtbPeXdxGBzb794t8oSKB2WjoN05Lc-j"
Gedo = "https://discord.com/api/webhooks/1158824183833309326/lOGuL_T9mAtYuGCkDRkVxRERIQAD1fHS3RTzxkRmS1ZlzT5yY4C7bi20XdK-1pSXcVzZ"
Sameh = "https://discord.com/api/webhooks/1226090203760955433/DkaAHvw-ZnTlUhaHEslmpXbSi45x-5nf9cZJ3MLbkjooaSNSOtYwOY2Jb70jGDjaRI9W"
Else = "https://discord.com/api/webhooks/1201174140770586655/d3VuNRT1j0xyTajwMC7gKIwfGDywENK1MaAtjhtJ02Okv-Xf0X5ROMuvhaAArEVG_iZc"
Logs = "https://discord.com/api/webhooks/1199384528553254983/-wZ9h7YobG3IHZBRZKtzPI5ZcAHpHvMYM-ajpJ87ZzXWTWvu2Upkk7_YaYi3X66QaUJL"
Tamer = "https://discord.com/api/webhooks/1279775036999204924/Q8Rc7UWPrNw6-5nX-cCkTqiAu9kofwHqkppPqCCPyGVfxXV0eI_HTja8DZDef2dMeIIW"
#Defult

vdo = Blueprint('vdo', __name__)
used_tokens = set()  # Set to store used tokens
used_ids = set()
cached_results = []  # Initialize as an empty list


def base64url_to_text(encoded_str):
    encoded_str = encoded_str.replace('-', '+').replace('_', '/')
    while len(encoded_str) % 4 != 0:
        encoded_str += '='
    decoded_bytes = base64.b64decode(encoded_str)
    decoded_text = decoded_bytes.decode('utf-8')
    return decoded_text


def gethref(token):
    # decoded_bytes = base64.b64decode(token)
    decoded_string = base64url_to_text(token)
    data = json.loads(decoded_string)
    href = data.get("href")
    return (href)


#log
def discord_log(message):
    messageeeee = {'content': message}
    payload = json.dumps(messageeeee)
    headers = {'Content-Type': 'application/json'}
    requests.post(
        "https://discord.com/api/webhooks/1199384528553254983/-wZ9h7YobG3IHZBRZKtzPI5ZcAHpHvMYM-ajpJ87ZzXWTWvu2Upkk7_YaYi3X66QaUJL",
        data=payload,
        headers=headers)


@vdo.route('/check_file/<path:filename>')
def check_file(filename):

    if os.path.isfile(filename):
        return f'{filename} exists!'
    else:
        return f'{filename} does not exist.'


def jsonget(token, thing):
    # decoded_bytes = base64.b64decode(token)
    decoded_string = base64url_to_text(token)
    data = json.loads(decoded_string)
    final = data.get(thing)
    return (final)


def getkeys_vdocipher(video_url):
    wvd = "cdms/vdo.wvd"  # Set your preferred value for wvd
    if wvd is None:
        exit(
            f"No CDM! To use local decryption, place a .wvd in {os.getcwd()}/WVDs"
        )

    #Base 64 tokens

    url = gethref(video_url)
    # url = input("Enter Url(site url change line 136 , 173): ")

    token = video_url

    # Add padding if necessary
    token += '=' * ((4 - len(token) % 4) % 4)

    try:
        # Decode the base64 string
        decoded_bytes = base64.b64decode(token)
        # Convert bytes to string using latin-1 encoding
        decoded_string = decoded_bytes.decode('latin-1')

        # Find the index of "otp":
        otp_index = decoded_string.find('"otp":"')
        playback_info_index = decoded_string.find('"playbackInfo":"')

        if otp_index != -1:
            # Extract the OTP substring
            otp_start_index = otp_index + len('"otp":"')
            otp_end_index = decoded_string.find('"', otp_start_index)
            otp_match = decoded_string[otp_start_index:otp_end_index]

        else:
            otp_match = jsonget(token, 'otp')
            print("No OTP found in the decoded string.")

        if playback_info_index != -1:
            # Extract the playbackInfo substring
            playback_info_start_index = playback_info_index + len(
                '"playbackInfo":"')
            playback_info_end_index = decoded_string.find(
                '"', playback_info_start_index)
            playbackinfo_match = decoded_string[
                playback_info_start_index:playback_info_end_index]

        else:
            playbackinfo_match = jsonget(token, 'playbackInfo')
            print("No playbackInfo found in the decoded string.")

    except UnicodeDecodeError:
        print("Error: Unable to decode the input using latin-1 encoding.")
    except Exception as e:
        print(f"An error occurred: {e}")

    video_url = f"https://player.vdocipher.com/v2/?otp={otp_match}&playbackInfo={playbackinfo_match}"

    # Try to find the OTP from the string
    try:
        otp_match = re.findall(r"otp: '(.*)',", video_url)[0]
        playbackinfo_match = re.findall(r"playbackInfo: '(.*)',", video_url)[0]
    except IndexError:
        try:
            otp_match = re.findall(r"otp=(.*)&", video_url)[0]
            playbackinfo_match = re.findall(r"playbackInfo=(.*)", video_url)[0]
        except IndexError:
            print("\nAn error occurred while getting otp/playback")
            exit()

    # Get the video id from playbackinfo_match
    video_id = json.loads(
        base64.b64decode(playbackinfo_match).decode())["videoId"]

    # Send a get request to acquire the license URL
    proxy = {
            "http": "http://nprofi:6f0reuyu@139.171.104.74:29842",
            "https": "http://nprofi:6f0reuyu@139.171.104.74:29842"
        }
    license_get_request = requests.get( url=f'https://dev.vdocipher.com/api/meta/{video_id}' ,proxies= proxy)

    # Try to extract the license URL from the license get request
    try:
        license_url_match = license_get_request.json(
        )["dash"]["licenseServers"]["com.widevine.alpha"].rsplit(":", 1)[0]
        mpd = license_get_request.json()["dash"]["manifest"]
        video_name = license_get_request.json()["title"]
    except KeyError:
        print("\nAn error occurred while getting mpd/license url")

    # Send a get request to acquire the MPD
    mpd_get_request = requests.get(url=mpd)

    # Regular expression search the mpd get request for PSSH
    input_pssh = re.search(r"<cenc:pssh>(.*)</cenc:pssh>",
                           mpd_get_request.text).group(1)

    # Prepare pssh
    pssh = PSSH(input_pssh)
    # Load device
    device = Device.load(wvd)

    # Load CDM from device
    cdm = Cdm.from_device(device)

    # Open CDM session
    session_id = cdm.open()

    headers = {
        'Content-Type': 'application/json',
        'vdo-sdk': 'Aegis/1.26.8-bg-zen-1',
        'User-Agent':
        'Dalvik/2.1.0 (Linux; U; Android 13; 2201117SG Build/TP1A.220624.014)',
        'Host': 'license.vdocipher.com',
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip',
        #'Content-Length': '4320',
    }

    # Set service cert token
    service_cert_token = {
        "otp":
        otp_match,
        "playbackInfo":
        playbackinfo_match,
        "packageName":
        "com.vdocipher.zenplayer",
        "tech":
        "wv",
        "href":
        f"{url}",
        "licenseRequest":
        f"{base64.b64encode(cdm.service_certificate_challenge).decode()}",
    }
    token = base64.b64encode(
        json.dumps(service_cert_token).encode("utf-8")).decode()
    # Convert service cert token to JSON
    service_cert_json_data = {
        'token': f'{token}',
    }

    # Get service certificate
    service_cert = requests.post('https://license.vdocipher.com/auth',
                                 headers=headers,
                                 json=service_cert_json_data ,proxies= proxy)

    discord_log(service_cert.text)
    if service_cert.status_code != 200:
        print("Couldn't retrieve service cert")
    else:
        service_cert = service_cert.json()["license"]
        cdm.set_service_certificate(session_id, cdm.common_privacy_cert)

    # Generate license challenge
    if service_cert:
        challenge = cdm.get_license_challenge(session_id,
                                              pssh,
                                              privacy_mode=True)
    else:
        challenge = cdm.get_license_challenge(session_id, pssh)

    # Declare token dictionary for license challenge
    token = {
        "otp": otp_match,
        "playbackInfo": playbackinfo_match,
        "packageName": "com.vdocipher.zenplayer",
        "tech": "wv",
        "href": f"{url}",
        "licenseRequest": f"{base64.b64encode(challenge).decode()}",
    }

    # Convert token dictionary into JSON data
    json_data = {
        'token':
        f'{base64.b64encode(json.dumps(token).encode("utf-8")).decode()}',
    }

    headers = {
        'Content-Type': 'application/json',
        'vdo-sdk': 'Aegis/1.26.8-bg-zen-1',
        'User-Agent':
        'Dalvik/2.1.0 (Linux; U; Android 13; 2201117SG Build/TP1A.220624.014)',
        'Host': 'license.vdocipher.com',
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip',
        #'Content-Length': '4320',
    }

    # send license challenge
    license = requests.post('https://license.vdocipher.com/auth',
                            headers=headers,
                            json=json_data , proxies= proxy)

    discord_log(license.text)

    if license.status_code != 200:
        print(license.content)
        exit("Could not complete license challenge")

    # Extract license from json dict
    license = license.json()["license"]

    # parse license challenge
    cdm.parse_license(session_id, license)
    '''
        # assign variable for returned keys
    returned_keys = ""
    for key in cdm.get_keys(session_id):
            if key.type != "SIGNING":
                returned_keys += f"{key.kid.hex}:{key.key.hex()}\n"
    '''

    c_keys = ""
    for key in cdm.get_keys(session_id):
        if key.type != "SIGNING":
            c_keys += f"--key {key.kid.hex}:{key.key.hex()} "

        # close session, disposes of session data
    cdm.close(session_id)

    # Print out the keys

    # print("-----------------------\n\n\n")

    # print(mpd)
    # print(f'\n{c_keys}')
    return mpd, c_keys, video_name


# Video ID for mpd and pssh
def get_video_id(token: str):
    playback_info = json.loads(base64url_to_text(token))['playbackInfo']
    return json.loads(base64.b64decode(playback_info))['videoId']


# pssh
def get_pssh(mpd: str):
    req = None
    req = requests.get(mpd)
    return re.search('<cenc:pssh>(.*)</cenc:pssh>', req.text).group(1)


# mpd
def get_mpd_vdocipher(video_id: str) -> str:
    headers = {
        'user-agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
        'origin': 'https://dev.vdocipher.com/',
        'referer': 'https://dev.vdocipher.com/'
    }
    url = 'https://dev.vdocipher.com/api/meta/' + video_id
    req = None
    req = requests.get(url, headers=headers)
    resp = req.json()
    return resp['dash']['manifest']


@vdo.route("/keys/<int:index>")
def get_key(index):
    cached_list = list(cached_results)
    if 0 <= index < len(cached_list):
        value = cached_list[index]
        return value
    else:
        return jsonify({'error': 'Index out of range'}), 404


@vdo.route('/vdocipher', methods=['GET', 'POST'])
def index():
    mytoken = request.args.get('token')
    client_ip = request.headers.get('CF-Connecting-IP', request.remote_addr)

    if request.method == 'GET':
        if mytoken in used_tokens:
            discord_log(f"USED TOKEN | {current_user.username} | {client_ip}")
            return jsonify({'error': 'Token already used'}), 400

        video_id = get_video_id(mytoken)

        if video_id in used_ids:

            mpd2 = get_mpd_vdocipher(video_id)

            for x in cached_results:
                if mpd2 in x:
                    index = cached_results.index(x)
                    discord_log(
                        f"USED VIDEO | {current_user.username} | {client_ip} | {index}"
                    )
                    return redirect(f"/keys/{index}")

        else:
            discord_log(
                f"Api got used by {current_user.username} | {client_ip}")
            used_ids.add(video_id)

    mpd, c_keys, video_name = getkeys_vdocipher(mytoken)

    tokenhref = gethref(mytoken)

    result = mpd + '\n' + c_keys

    session['video_orignal_name'] = video_name

    used_tokens.add(mytoken)

    session['result'] = result
    cached_results.append(result)

    keys_content = re.findall(r"--key\s+(\S+)", c_keys)

    components = result.split()
    input_url = components[0]
    components = result.split("--key")[1:]
    keys = [key.strip() for key in components[1:]]
    ckvaluetobeused = {}
    for key in keys:
        parts = key.split(":")
        if len(parts) == 2:
            ckvaluetobeused[parts[0]] = parts[1]

    keysbase64 = base64.urlsafe_b64encode(
        str(ckvaluetobeused).encode()).decode()

    url = input_url + "?ck=" + keysbase64

    session['urlopen'] = url

    discord_log(url)

    options_map = {

        "mrredaelfarouk": [
            'Gedo',  'Nasser-El-Batal',  'Bio', 'Tamer-el-kady' , 'Else'
        ]

    }



    for keyword, keyword_options in options_map.items():
        if keyword in tokenhref:
            options = keyword_options
            break
    else:
        default_options = ['Else', 'Tamer-el-kady', 'Nasser-El-Batal', 'Bio', 'Gedo',]
        options = default_options

    result = result.replace("\n", " ").replace("https://" , "`https://")


    old = request.args.get('old')

    if old != "true":
        status = "new"
        if request.method == 'POST':

            name = request.form.get('vidname')
            teacher = request.form.get('dropdown')

            video_orignal_name = video_name

            message = {
                'content':
                f'```app {result} --save-name {name} -M format=mp4 --auto-select --no-log  & move {name}.mp4 ./output``` {name} {video_orignal_name} ```watch now``` {url}&title={name}'
            }
            payload = json.dumps(message)
            userinput = f"app {result} --save-name {name} -M format=mp4 --auto-select --no-log  & move {name}.mp4 ./output"
            with open('list.txt', 'a') as file:
                file.write(userinput + '\n')
            headers = {'Content-Type': 'application/json'}
            teacher_webhooks = {
                "Tamer-el-kady" : Tamer,
                "Nawar": Nawar,
                "Nasser-El-Batal": Nasser,
                "Salama": Salama,
                "Bio": Bio,
                "Sameh-Nash2t": Sameh,
                "Gedo": Gedo,
            }

            webhook_url = teacher_webhooks.get(teacher, Else)
            requests.post(webhook_url, data=payload, headers=headers )
            return 'Message Sent!'
    else:
        status = "old"

    return render_template('backend_pages/vdo.html',
                           content_key=keys_content,
                           mpd=mpd,
                           options=options,
                           result=result,
                           url=url,
                           status=status,
                           video_name=video_name)


@vdo.route('/form', methods=['POST'])
def form():
    options = ['Nawar', 'Nasser-El-Batal', 'MoSalama', 'Bio', 'Else']
    if request.method == 'POST':
        user_data = {
            'teacher': request.form.get('dropdown'),
            'name': request.form['vidname']
        }
        return redirect(url_for('vdo.discord', **user_data))
    return render_template('index.html', option=options)


@vdo.route('/vdodiscord', methods=['GET', 'POST'])
def discord():
    result = session.get('result')
    urlopen = session.get('urlopen')
    name = request.args.get('name')
    video_orignal_name = session.get('video_orignal_name')
    result = result.replace("\n", " ")
    teacher = request.args.get('teacher')
    message = {
        'content':
        f'```app {result} --save-name {name} -M format=mp4 --auto-select --no-log  & move {name}.mp4 ./output``` {name} {video_orignal_name} ```watch now``` {urlopen}&title={name}'
    }
    payload = json.dumps(message)
    userinput = f"app {result} --save-name {name} -M format=mp4 --auto-select --no-log  & move {name}.mp4 ./output"

    with open('list.txt', 'a') as file:
        file.write(userinput + '\n')
    headers = {'Content-Type': 'application/json'}
    teacher_webhooks = {
        "Tamer-el-kady" : Tamer,
        "Nawar": Nawar,
        "Nasser-El-Batal": Nasser,
        "Salama": Salama,
        "Bio": Bio,
        "Gedo": Gedo,
        "Sameh-Nash2t": Sameh,
    }

    webhook_url = teacher_webhooks.get(teacher, Else)
    requests.post(webhook_url, data=payload, headers=headers)

    return 'Message Sent!'


@vdo.route('/iframes', methods=['GET', 'POST'])
def iframevids():
    url = request.args.get('url') or request.form.get('url')
    namee = request.args.get('name') or request.form.get('name')
    videoname = request.args.get('videoname') or request.form.get('videoname')

    if namee == "nawar":
        webhook_url = "https://discord.com/api/webhooks/1159805446039797780/bE4xU3lkcjlb4vfCVQ9ky5BS2OuD01Y8g9godljNBfoApGt59-VfKf19GQuMUmH0IYzw"
    elif namee == "ahmadsalah":
        webhook_url = "https://discord.com/api/webhooks/1170733207835115630/MpyyTLirCjBUOSHxisTsb4l7lqF7XBw-l4KEsi7DAFLAoZdUzMtGFwth67Qj3ZJCE5Oo"
    elif namee == "sherbo":
        # webhook_url ="https://discord.com/api/webhooks/1275782261425438803/siPIo2_24HHXITRT44MgiiF0MRO--vnegwZdyz-DwSM8lnoWTaIsLfIxTHev6n28JrbL"
        webhook_url = "https://discord.com/api/webhooks/1169342540575670292/crazeFe5z0qAozWBJOnlZfevMMQ219NVzZ-Cl6mWK9NrtBqBXc3kBzj1tJ8_KVu7UuKf"
    url = url.replace("/play/", "/embed/")
    if request.method == 'POST':
        videoname = request.form.get('videoname')
        videoname = re.sub(r'[\s\W_]+', '', videoname)

        if "youtube" in url.lower() or "youtu.be" in url.lower():
            url = url.split('/')[4]

            msg = f'```yt-dlp.exe "https://www.youtube.com/watch?v={url}" --cookies-from-browser chrome -f best -o {videoname}``` {videoname}'
            command = f'yt-dlp.exe "https://www.youtube.com/watch?v={url}" --cookies-from-browser chrome -f best -o {videoname}'
            with open('list.txt', 'a') as file:
                file.write(command + '\n')
        else:
            url = url.split('?')[0]
            msg = f'```python iframe.py {url} {videoname}``` {videoname}'
            command = f"python iframe.py {url} {videoname}"
            with open('list.txt', 'a') as file:
                file.write(command + '\n')

        message = {'content': f'{msg}'}
        payload = json.dumps(message)
        headers = {'Content-Type': 'application/json'}
        requests.post(webhook_url, data=payload, headers=headers)
        return "Message Sent!"
    return render_template('backend_pages/iframe.html', url=url, videoname=videoname)


@vdo.route('/iframem3u8', methods=['GET', 'POST'])
def hosssamsameh():
    url = request.args.get('url')
    videoname = request.args.get('videoname') or request.form.get('videoname')

    # hossamsameh = request.args.get('hossamsameh')
    webhook_url = "https://discord.com/api/webhooks/1224528158741626901/mIG58hd-FLTe79XHUsgwE0BxyyKjL2JFs9RyHfLBRfyM1v85YbkJGEzcJyQQVOsfhpRc"

    if "interstellar" in url:
        webhook_url = "https://discord.com/api/webhooks/1279772067809726572/3e9QcfqYQ8GColvvWbrD0ZRpKbisb8Wb3eAxgQz0ttl6556BnHIrKOKPC3fSmQka0yQT"
        url = url
    else:
        url = "/".join(url.split("/")[:4]) + "/playlist.m3u8"

    if request.method == 'POST':
        name = request.form.get('videoname')
        name = re.sub(r'[\s\W_]+', '', name)

        if "interstellar" in url: 
            msg = f'```app {url} --save-name {name} -M format=mp4 --auto-select --no-log  & move {name}.mp4 ./output``` {name}'
            command = f'app {url} --save-name {name} -M format=mp4 --auto-select --no-log  & move {name}.mp4 ./output;'
        else :   
            msg = f'```app {url} --header "User-Agent: Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0" --header "Referer: https://iframe.mediadelivery.net/" --save-name {name} -M format=mp4 --auto-select --no-log  & move {name}.mp4 ./output``` {name}'
            command = (
                f'app {url} --header "User-Agent: Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0" --header "Referer: https://iframe.mediadelivery.net/" --save-name {name} -M format=mp4 --auto-select --no-log  & move {name}.mp4 ./output'
            )
        with open('list.txt', 'a') as file:
            file.write(command + '\n')
        message = {'content': f'{msg}'}
        payload = json.dumps(message)
        headers = {'Content-Type': 'application/json'}
        requests.post(webhook_url, data=payload, headers=headers)
        return "Message Sent!"
    return render_template('backend_pages/iframe.html', url=url , videoname=videoname)






@vdo.route('/skillshare', methods=['GET', 'POST'])
def skillshare():
    url = request.args.get('m3u8')
    videoname = request.args.get('name') 

    webhook_url = "https://discord.com/api/webhooks/1224528158741626901/mIG58hd-FLTe79XHUsgwE0BxyyKjL2JFs9RyHfLBRfyM1v85YbkJGEzcJyQQVOsfhpRc"

    if request.method == 'POST':
        if url :
            pass
        else :
            url = request.form.get('url')

        name = request.form.get('videoname')
  
        msg = f'```app {url} --save-name "{name}" -M format=mp4 --auto-select --no-log  & move "{name}".mp4 ./output``` {name}'
        command = f'app {url} --save-name "{name}" -M format=mp4 --auto-select --no-log  & move "{name}".mp4 ./output;'

        with open('list.txt', 'a') as file:
            file.write(command + '\n')
        message = {'content': f'{msg}'}
        payload = json.dumps(message)
        headers = {'Content-Type': 'application/json'}
        requests.post(webhook_url, data=payload, headers=headers)
        return "Message Sent!"
    return render_template('backend_pages/iframe.html', url=url , videoname=videoname)
























@vdo.route("/list")
def commandslist():

    def extract_save_name(command):
        if command.startswith("python"): #Iframe commands

            try :
                return command.split(' ')[3]
            except :
                save_name_match = "Command has no name"
                return save_name_match

        elif command.startswith("yt-dlp"): #yt-dlp commands
            commandsplit= command.split(' ')[9]
            command = commandsplit.split('/')[2]
            return command.split('.')[0]

        else: #app.exe normal commands

            save_name_match = re.search(r'--save-name\s+(\S+)', command)
            match = re.search(r'--save-name\s*"([^"]+)"', command)
            if match:
                return match.group(1)
            elif save_name_match :
                return save_name_match.group(1)
            else:
                return "Command has no name"
    def commandtype(command):
        if command.startswith("python"): #Iframe commands
            return "Iframe Video"
        elif command.startswith("app"):
            return "DRM Video"
        elif command.startswith("yt-"):
            return "Youtube Video"
    # Read commands from the file
    with open('list.txt', 'r') as file:
        cmds_from_file = [line.strip() for line in file if line.strip()]

    return render_template("backend_pages/list.html",
                           count=len(cmds_from_file),
                           cmds_queue=cmds_from_file,
                           extract_save_name=extract_save_name,
                           commandtype = commandtype )


@vdo.route('/deletecmd', methods=['GET'])
def delete_command():
    line_number = request.args.get('line', type=int)  # Single line number as an integer
    lines_to_delete = request.args.get('lines')  # Comma-separated list of line numbers (optional)

    with open('list.txt', 'r') as file:
        lines = file.readlines()

    if line_number:
        if line_number < 1 or line_number > len(lines):
            return f"Invalid line number: {line_number}. Must be between 1 and {len(lines)}.", 400

        # Remove the single specified line
        del lines[line_number - 1]
    elif lines_to_delete:
        # Parse the list of line numbers
        try:
            line_numbers = sorted(set(int(num.strip()) for num in lines_to_delete.split(',')), reverse=True)
        except ValueError:
            return "Invalid line numbers provided. Must be integers separated by commas.", 400

        # Validate line numbers
        for num in line_numbers:
            if num < 1 or num > len(lines):
                return f"Invalid line number: {num}. Must be between 1 and {len(lines)}.", 400

        # Remove lines in reverse order to avoid shifting indices
        for num in line_numbers:
            del lines[num - 1]
    else:
        return "No line number(s) provided.", 400

    with open('list.txt', 'w') as file:
        file.writelines(lines)

    return redirect(url_for('vdo.commandslist'))




@vdo.route("/addcmd", methods=['GET', 'POST'])
def addtolist():

    newcmd = request.args.get('newcmd')

    if request.method == 'POST':
        userinput = request.form['userinput']
        checkbox = request.form.get('checkbox')
        videoname = request.form['videoname']


        if "youtu" in userinput :
            if checkbox :
                with open('list.txt', 'r') as file:
                    cmds_from_file = [line.strip() for line in file if line.strip()]
                userinput = f'yt-dlp -f "bv+ba" --cookies ./cookies.txt --merge-output-format mp4 {userinput} -o ./output/{videoname}.mp4'

            with open('list.txt', 'a') as file:
                file.write(userinput + '\n')
        else :
            with open('list.txt', 'a') as file:
                file.write(userinput + '\n')

        with open('list.txt', 'r') as file:
            cmds_from_file = [line.strip() for line in file if line.strip()]

        return redirect(url_for('vdo.commandslist'))

    return render_template("backend_pages/addtolist.html", newcmd=newcmd)


@vdo.route("/clear")
def clearlist():
    with open('list.txt', 'w') as file:
        file.truncate(0)
    return redirect(url_for('vdo.commandslist'))


@vdo.route("/createcmd")
def cmdcommand():
    with open('list.txt', 'r') as file:
        cmds_from_file = [line.strip() for line in file if line.strip()]
    combined_cmds = " & ".join([
        f'start cmd.exe @cmd /k "{element} & exit"'
        for element in cmds_from_file
    ]) + "& exit"

    if len(combined_cmds) > 8191:
        total_length = sum(len(cmd) for cmd in cmds_from_file)
        split_point = 0
        current_length = 0
        for i, cmd in enumerate(cmds_from_file):
            current_length += len(cmd)
            if current_length > total_length // 2:
                split_point = i
                break

        # Split commands
        first_part_cmds = cmds_from_file[:split_point]
        second_part_cmds = cmds_from_file[split_point:]

        first_part_combined_cmds = " & ".join([
            f'start cmd.exe @cmd /k "{cmd} & exit"' for cmd in first_part_cmds
        ]) + "& exit"
        second_part_combined_cmds = " & ".join([
            f'start cmd.exe @cmd /k "{cmd} & exit"' for cmd in second_part_cmds
        ]) + "& exit"

        return f"<h1>Part 1 </h1>{first_part_combined_cmds} <br><h1>Part 2</h1> {second_part_combined_cmds} "

    return combined_cmds


@vdo.route("/cleartokens")
def cleartokens():
    used_tokens.clear()
    used_ids.clear()
    return "done"


@vdo.route("/pssh")
def pssh():
    return jsonify(list(used_ids))



#Ink videos------------------------------------------------------------------------------------------------------------

def get_mpd_ink(token , xotp):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
        'origin': 'https://resource.inkryptvideos.com',
        'referer': 'https://resource.inkryptvideos.com/',
        'X-Otp' : f'{xotp}'
    }
    decoded_bytes = base64.b64decode(token)
    decoded_string = decoded_bytes.decode('utf-8')
    data = json.loads(decoded_string)
    video_id = data.get("v")
    url = 'https://api.inkryptvideos.com/api/s1/v_info/' + video_id
    req = None
    req = requests.get(url, headers=headers)
    req.raise_for_status()  # Raise an exception if the request fails
    resp = req.json()
    storage_hostname = resp['data']['storage_hostname']
    dash_manifest = resp['data']['dash_manifest'].replace("\\", "")
    full_url = f"https://{storage_hostname}/{dash_manifest}"
    return full_url

def getv(token):
    decoded_bytes = base64.b64decode(token)
    decoded_string = decoded_bytes.decode('utf-8')
    data = json.loads(decoded_string)
    v = data.get("v")
    return (v)

proxy = {
        "http": "http://nprofi:6f0reuyu@139.171.104.74:29842",
        "https": "http://nprofi:6f0reuyu@139.171.104.74:29842"
    }

def getkeys_ink(token , xotp , ins):
    wvd = "cdms/ink.wvd"  # Set your preferred value for wvd
    if wvd is None:
        exit(f"No CDM! To use local decryption, place a .wvd in {os.getcwd()}/WVDs")
    mpd = get_mpd_ink(token , xotp)
    pssh = PSSH(get_pssh(mpd))
    device = Device.load(wvd)
    cdm = Cdm.from_device(device)
    session_id = cdm.open()

    service_cert_json_data = {
        'token': f'{token}',
    }

    headers = {
        "host": "license.inkryptvideos.com",
        "in-s": ins ,
        "x-otp": f"{xotp}",
        "content-type": "application/json",
        "content-length" : "1012"

    }


    service_cert = requests.post(
        'https://license.inkryptvideos.com/api/v1/wj/license',
        headers=headers,
        json=service_cert_json_data 
    )


    if service_cert.status_code != 200:
        print("Couldn't retrieve service cert")
    else:
        service_cert = service_cert.json()["l"]
        cdm.set_service_certificate(session_id, cdm.common_privacy_cert)


    if service_cert:
        challenge = cdm.get_license_challenge(session_id, pssh, privacy_mode=True)
    else:
        challenge = cdm.get_license_challenge(session_id, pssh)


    v = getv(token)

    token = {
            "v" : f"{v}",
            "c": f"{base64.b64encode(challenge).decode()}",
            
        }

    json_data = {
            'token': f'{base64.b64encode(json.dumps(token).encode("utf-8")).decode()}',
        }

    headers = {
        "host": "license.inkryptvideos.com",
        "in-s": ins ,
        "x-otp": f"{xotp}",
        "content-type": "application/json",
        "content-length" : "8680"

    }
    license = requests.post(
            'https://license.inkryptvideos.com/api/v1/wj/license',
            headers=headers,
            json=json_data 
        )

    if license.status_code != 200:
            print(license.content)
            exit("Could not complete license challenge")
    license = license.json()["l"]
    cdm.parse_license(session_id, license)

    c_keys = ""
    for key in cdm.get_keys(session_id):
        if key.type != "SIGNING":
            c_keys += f"--key {key.kid.hex}:{key.key.hex()} "
    cdm.close(session_id)
    return c_keys , mpd 




@vdo.route('/ink', methods=['GET', 'POST'])
def ink():
    token = request.args.get('token')
    xotp = request.args.get('otp')
    ins = request.args.get('ins')

    c_keys , mpd = getkeys_ink(token , xotp , ins)

    keys_content = re.findall(r"--key\s+(\S+)", c_keys)

    result = mpd + '\n' + c_keys

    session['result'] = result
    components = result.split()
    input_url = components[0]
    components = result.split("--key")[1:]
    keys = [key.strip() for key in components[1:]]
    ckvaluetobeused = {}
    for key in keys:
        parts = key.split(":")
        if len(parts) == 2:
            ckvaluetobeused[parts[0]] = parts[1]

    keysbase64 = base64.urlsafe_b64encode(
        str(ckvaluetobeused).encode()).decode()

    url = input_url + "?ck=" + keysbase64

    discord_log(keys)

    result = result.replace("\n", " ")


    return render_template('backend_pages/ink.html', content_key=keys_content , mpd = mpd ,result = result)



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
    with open('list.txt', 'a') as file:
            file.write(msg + '\n')
    requests.post("https://discord.com/api/webhooks/1158824183833309326/lOGuL_T9mAtYuGCkDRkVxRERIQAD1fHS3RTzxkRmS1ZlzT5yY4C7bi20XdK-1pSXcVzZ", data=payload, headers=headers)
    return "Message Sent!" 