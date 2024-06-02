from flask import  render_template, request, redirect, url_for, session , Blueprint, jsonify
import base64
import json
import requests , re 
from flask_login import  current_user
# Import dependencies
from pywidevine import PSSH
from pywidevine import Cdm
from pywidevine import Device
import os


Nawar = 'https://discord.com/api/webhooks/1159805446039797780/bE4xU3lkcjlb4vfCVQ9ky5BS2OuD01Y8g9godljNBfoApGt59-VfKf19GQuMUmH0IYzw'
Bio= "https://discord.com/api/webhooks/1158548096012259422/jQ5sEAZBIrvfBNTA-w4eR-p6Yw0zv7GBC9JTUcEOAWfmqYJXbOpgysATjKPXLwd8HZOs"
Nasser = "https://discord.com/api/webhooks/1158548163209199626/73nAC_d1rgUr6IS79gC508Puood83ho848IEGOpxLtUzGEEJ3h8CyZqlZvCZ6jEXH5k1"
Salama = "https://discord.com/api/webhooks/1158548226971009115/qtBWD8plfY3JFMjCKYrcXwJ8ayMIbUnXFU3_XtbPeXdxGBzb794t8oSKB2WjoN05Lc-j"
Gedo = "https://discord.com/api/webhooks/1158824183833309326/lOGuL_T9mAtYuGCkDRkVxRERIQAD1fHS3RTzxkRmS1ZlzT5yY4C7bi20XdK-1pSXcVzZ"
Sameh = "https://discord.com/api/webhooks/1226090203760955433/DkaAHvw-ZnTlUhaHEslmpXbSi45x-5nf9cZJ3MLbkjooaSNSOtYwOY2Jb70jGDjaRI9W"
Else = "https://discord.com/api/webhooks/1201174140770586655/d3VuNRT1j0xyTajwMC7gKIwfGDywENK1MaAtjhtJ02Okv-Xf0X5ROMuvhaAArEVG_iZc"
Logs = "https://discord.com/api/webhooks/1199384528553254983/-wZ9h7YobG3IHZBRZKtzPI5ZcAHpHvMYM-ajpJ87ZzXWTWvu2Upkk7_YaYi3X66QaUJL"




#Defult

vdo = Blueprint('vdo', __name__)
used_tokens = set()  # Set to store used tokens
used_pssh = set()
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
    messageeeee = { 'content': message }
    payload = json.dumps(messageeeee)
    headers = {'Content-Type': 'application/json'}
    requests.post("https://discord.com/api/webhooks/1199384528553254983/-wZ9h7YobG3IHZBRZKtzPI5ZcAHpHvMYM-ajpJ87ZzXWTWvu2Upkk7_YaYi3X66QaUJL", data=payload, headers=headers)



@vdo.route('/check_file/<path:filename>')
def check_file(filename):

    if os.path.isfile(filename):
        return f'{filename} exists!'
    else:
        return f'{filename} does not exist.'



def getkeys(video_url):
    wvd = "cdm.wvd"  # Set your preferred value for wvd
    if wvd is None:
        exit(f"No CDM! To use local decryption, place a .wvd in {os.getcwd()}/WVDs")


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
            print("No OTP found in the decoded string.")

        if playback_info_index != -1:
            # Extract the playbackInfo substring
            playback_info_start_index = playback_info_index + len('"playbackInfo":"')
            playback_info_end_index = decoded_string.find('"', playback_info_start_index)
            playbackinfo_match = decoded_string[playback_info_start_index:playback_info_end_index]
            
        else:
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
    video_id = json.loads(base64.b64decode(playbackinfo_match).decode())["videoId"]

    # Send a get request to acquire the license URL
    license_get_request = requests.get(url=f'https://dev.vdocipher.com/api/meta/{video_id}')

    # Try to extract the license URL from the license get request
    try:
        license_url_match = license_get_request.json()["dash"]["licenseServers"]["com.widevine.alpha"].rsplit(":", 1)[0]
        mpd = license_get_request.json()["dash"]["manifest"]
        video_name = license_get_request.json()["title"]
    except KeyError:
        print("\nAn error occurred while getting mpd/license url")

    # Send a get request to acquire the MPD
    mpd_get_request = requests.get(url=mpd)

    # Regular expression search the mpd get request for PSSH
    input_pssh = re.search(r"<cenc:pssh>(.*)</cenc:pssh>", mpd_get_request.text).group(1)

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
        'vdo-sdk': 'Aegis/1.26.3-bp-zen-3',
        'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 13; SM-E625F Build/TP1A.220624.014)',
        'Host': 'license.vdocipher.com',
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip',
        #'Content-Length': '4320',
    }

    # Set service cert token
    service_cert_token = {
        "otp": otp_match,
        "playbackInfo": playbackinfo_match,
        "packageName": "com.vdocipher.zenplayer",
        "tech": "wv",
        "href":f"{url}",
        "licenseRequest": f"{base64.b64encode(cdm.service_certificate_challenge).decode()}",
        
    }
    token = base64.b64encode(json.dumps(service_cert_token).encode("utf-8")).decode()
    # Convert service cert token to JSON
    service_cert_json_data = {
        'token': f'{token}',
    }

    # Get service certificate
    service_cert = requests.post(
        'https://license.vdocipher.com/auth',
        headers=headers,
        json=service_cert_json_data
    )


    if service_cert.status_code != 200:
        print("Couldn't retrieve service cert")
    else:
        service_cert = service_cert.json()["license"]
        cdm.set_service_certificate(session_id, cdm.common_privacy_cert)

    # Generate license challenge
    if service_cert:
        challenge = cdm.get_license_challenge(session_id, pssh, privacy_mode=True)
    else:
        challenge = cdm.get_license_challenge(session_id, pssh)

    # Declare token dictionary for license challenge
    token = {
            "otp": otp_match,
            "playbackInfo": playbackinfo_match,
            "packageName": "com.vdocipher.zenplayer",
            "tech": "wv",
            "href":f"{url}",
            "licenseRequest": f"{base64.b64encode(challenge).decode()}",
            
        }

        # Convert token dictionary into JSON data
    json_data = {
            'token': f'{base64.b64encode(json.dumps(token).encode("utf-8")).decode()}',
        }

    headers = {
        'Content-Type': 'application/json',
        'vdo-sdk': 'Aegis/1.26.3-bp-zen-3',
        'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 13; SM-E625F Build/TP1A.220624.014)',
        'Host': 'license.vdocipher.com',
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip',
        #'Content-Length': '4320',
    }

        # send license challenge
    license = requests.post(
            'https://license.vdocipher.com/auth',
            headers=headers,
            json=json_data
        )

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
    return mpd , c_keys , video_name


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





@vdo.route("/keys/<int:index>")
def get_key(index):
    cached_list = list(cached_results)
    if 0 <= index < len(cached_list):
        value = cached_list[index]
        return render_template('key_page.html', value=value)
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
        
        if current_user.username != 'spy':
            mpd = get_mpd(get_video_id(mytoken))

            pssh = get_pssh(mpd)

            if pssh in used_pssh :
                for result in cached_results:
                    if mpd in result:
                        index = cached_results.index(result)
                        discord_log(f"USED VIDEO | {current_user.username} | {client_ip}")

                return f"/keys/{index}"
            else:
                discord_log(f"Api got used by {current_user.username} | {client_ip}")

    
    mpd , c_keys , video_name = getkeys(mytoken)

       
    tokenhref = gethref(mytoken)


    result = mpd + '\n' + c_keys 
    used_tokens.add(mytoken)
    used_pssh.add(pssh)
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

    keysbase64 = base64.urlsafe_b64encode(str(ckvaluetobeused).encode()).decode()

    url = input_url + "?ck=" + keysbase64

    session['urlopen'] = url

    discord_log(url)

    options_map = {
        "samehnashaat": ['Sameh-Nash2t', 'Bio', 'Nawar', 'Nasser-El-Batal', 'Salama', 'Gedo', 'Else'],
        "ednuva": ['Bio', 'Nawar', 'Nasser-El-Batal', 'Gedo', 'Else', 'Salama', 'Sameh-Nash2t'],
        "chemistry": ['Nasser-El-Batal', 'Else', 'Nawar', 'Gedo', 'Bio', 'Salama', 'Sameh-Nash2t'],
        "class": ['Nasser-El-Batal', 'Else', 'Nawar', 'Gedo', 'Bio', 'Salama', 'Sameh-Nash2t'],
        "mrredaelfarouk": ['Gedo', 'Nawar', 'Nasser-El-Batal', 'Else', 'Bio', 'Salama', 'Sameh-Nash2t'],
        "nawar": ['Nawar', 'Else', 'Nasser-El-Batal', 'Gedo', 'Bio', 'Salama', 'Sameh-Nash2t'],
        "matrix": ['Salama', 'Else', 'Nasser-El-Batal', 'Gedo', 'Bio', 'Nawar', 'Sameh-Nash2t']
    }

    default_options = ['Else', 'Nawar', 'Salama', 'Nasser-El-Batal', 'Gedo', 'Bio', 'Sameh-Nash2t']

    for keyword, keyword_options in options_map.items():
        if keyword in tokenhref:
            options = keyword_options
            break
    else:
        options = default_options


    result = result.replace("\n", " ")

    old = request.args.get('old')

    if old != "true" :
        status  = "new"
        if request.method == 'POST':
            name =  request.form.get('vidname')
            teacher =  request.form.get('dropdown')
            message = {
                    'content': f'```app {result} --save-name {name} -M format=mp4 --auto-select --no-log  & move {name}.mp4 ./output``` {name} ```watch now``` {url}'
                }
            payload = json.dumps(message)
            userinput = f"app {result} --save-name {name} -M format=mp4 --auto-select --no-log  & move {name}.mp4 ./output"
            with open('list.txt', 'a') as file:
                file.write(userinput + '\n')
            headers = {'Content-Type': 'application/json'}
            teacher_webhooks = {
                "Nawar": Nawar,
                "Nasser-El-Batal": Nasser,
                "Salama": Salama,
                "Bio": Bio,
                "Sameh-Nash2t": Sameh,
                "Gedo": Gedo,
            }
            webhook_url = teacher_webhooks.get(teacher, Else)
            requests.post(webhook_url, data=payload, headers=headers)
            return 'Message Sent!'
    else :
         status  = "old"    
   
    return render_template('backend_pages/vdo.html' , content_key = keys_content , mpd = mpd ,options = options, result= result , url = url , status = status  , video_name = video_name)



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

    with open('list.txt', 'a') as file:
                file.write(userinput + '\n')
    headers = {'Content-Type': 'application/json'}
    teacher_webhooks = {
        "Nawar": Nawar,
        "Nasser-El-Batal": Nasser,
        "Salama": Salama,
        "Bio": Bio,
        "Gedo": Gedo,
        "Sameh-Nash2t" : Sameh,
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
            command = f"python youtube.py https://www.youtube.com/watch?v={url} {name}"
            with open('list.txt', 'a') as file:
                file.write(command + '\n')
        else: 
            url = url.split('?')[0]
            msg = f'```python iframe.py {url} {name}``` {name}'
            command = f"python iframe.py {url} {name}"
            with open('list.txt', 'a') as file:
                file.write(command + '\n')

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
        command = (f'app {url}  --save-name {name} -M format=mp4 --auto-select --no-log  & move {name}.mp4 ./output')
        with open('list.txt', 'a') as file:
            file.write(command + '\n')
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
    # hossamsameh = request.args.get('hossamsameh')
    if "interstellar" in url : 
        url = url
    else :
        url = "/".join(url.split("/")[:4]) + "/playlist.m3u8"

    webhook_url="https://discord.com/api/webhooks/1224528158741626901/mIG58hd-FLTe79XHUsgwE0BxyyKjL2JFs9RyHfLBRfyM1v85YbkJGEzcJyQQVOsfhpRc" 
    if request.method == 'POST':
        name =  request.form.get('name')
        msg = f'```app {url} --header "User-Agent: Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0" --header "Referer: https://iframe.mediadelivery.net/" --save-name {name} -M format=mp4 --auto-select --no-log  & move {name}.mp4 ./output``` {name}'
        command= (f'app {url} --header "User-Agent: Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0" --header "Referer: https://iframe.mediadelivery.net/" --save-name {name} -M format=mp4 --auto-select --no-log  & move {name}.mp4 ./output')
        with open('list.txt', 'a') as file:
            file.write(command + '\n')
        message = {
                'content': f'{msg}'
            }
        payload = json.dumps(message)
        headers = {'Content-Type': 'application/json'}
        requests.post(webhook_url, data=payload, headers=headers)
        return "Message Sent!" 
    return render_template('backend_pages/iframe.html' , url = url)




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
        command = (f"app {mpd}  --key {key_value}  --save-name {name} -M format=mp4 --no-log  & move {name}.mp4 ./output")
        with open('list.txt', 'a') as file:
            file.write(command + '\n')
        message = {
                'content': f'{msg}'
            }
        payload = json.dumps(message)
        headers = {'Content-Type': 'application/json'}
        requests.post("https://discord.com/api/webhooks/1217535086002573332/UZWHTP2ZPVUdIuOTBG-PVVHyi1bxaa8p_xDNVfeXvTS7_p72a0iVWmJkEoeHaxVowrbr", data=payload, headers=headers)
        return "Message Sent!" 
    return render_template('backend_pages/shahid.html' , mpd = mpd , key =key_value , pssh = pssh  , url = f"{mpd}&ck={keysbase64}")






@vdo.route("/list")
def commandslist():
    def extract_save_name(command):
        if command.startswith("python"):
            return command.split(' ')[3]
        else:
            save_name_match = re.search(r'--save-name\s+(\S+)', command)
            if save_name_match:
                return save_name_match.group(1)
            else:
                return "Command has no name"
    
    # Read commands from the file
    with open('list.txt', 'r') as file:
        cmds_from_file = [line.strip() for line in file if line.strip()]
    
    return render_template("backend_pages/list.html", count=len(cmds_from_file), cmds_queue=cmds_from_file, extract_save_name=extract_save_name)




@vdo.route('/deletecmd', methods=['GET'])
def delete_command():
    command_to_delete = request.args.get('command')
    
    with open('list.txt', 'r') as file:
        lines = file.readlines()
    
    with open('list.txt', 'w') as file:
        for line in lines:
            if line.strip() != command_to_delete:
                file.write(line)
    
    return redirect(url_for('vdo.commandslist'))

@vdo.route("/addcmd", methods=['GET', 'POST'])
def addtolist():

    newcmd = request.args.get('newcmd')

    if request.method == 'POST':
        userinput = request.form['userinput']
        with open('list.txt', 'a') as file:
            file.write(userinput + '\n')
        import random
        random_number = random.randint(0, 100)
        return redirect(f'/addcmd?newcmd={random_number}')

    return render_template("backend_pages/addtolist.html" , newcmd = newcmd)




@vdo.route("/clear")
def clearlist():
    with open('list.txt', 'w') as file:
        file.truncate(0) 
    return "done"


@vdo.route("/createcmd")
def cmdcommand():
    with open('list.txt', 'r') as file:
        cmds_from_file = [line.strip() for line in file if line.strip()]
    combined_cmds = " & ".join([f'start cmd.exe @cmd /k "{element} & exit"' for element in cmds_from_file]) + "& exit"
    return combined_cmds

@vdo.route("/cleartokens")
def cleartokens():
        used_tokens.clear()
        used_pssh.clear()
        return "done"



@vdo.route("/pssh")
def pssh():
    return jsonify(list(used_pssh))