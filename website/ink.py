from flask import Flask, render_template, request, flash, redirect, url_for , session
import base64
import json
import requests
from pywidevine.cdm import deviceconfig
from pywidevine.cdm import cdm
import sys , re

app = Flask(__name__)
app.secret_key = 'dasdsdaasdsa232'

def getv(token):
    decoded_bytes = base64.b64decode(token)
    decoded_string = decoded_bytes.decode('utf-8')
    data = json.loads(decoded_string)
    v = data.get("v")
    return (v)


def generate_input1(mpd, content_key, vidname):
    input1 = f"app {mpd}\n--key " + "\n--key ".join(content_key) + f"\n--save-name {vidname} -M format=mp4 & move {vidname}.mp4 ./output"
    return input1

#pssh
def get_pssh(mpd: str):
    req = None
    req = requests.get(mpd)
    return re.search('<cenc:pssh>(.*)</cenc:pssh>', req.text).group(1)



webhook = "https://discord.com/api/webhooks/1158824183833309326/lOGuL_T9mAtYuGCkDRkVxRERIQAD1fHS3RTzxkRmS1ZlzT5yY4C7bi20XdK-1pSXcVzZ"

#mpd
def get_mpd(video_id , xotp):
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









@app.route('/', methods=['GET', 'POST'])
def index():
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
            mpd = get_mpd(newv , xotp)
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
    return render_template('index.html', content_key=content_key , mpd = mpd ,input1 = result)
    return render_template('ink.html')






#END PAGE



@app.route('/form', methods=['POST'])
def form():
    if request.method == 'POST':
        user_data = {
            'name': request.form['vidname']
        }
        return redirect(url_for('discord', **user_data))
    return render_template('index.html')


@app.route('/discord', methods=['GET', 'POST'])
def discord():
    result = session.get('result')
    name = request.args.get('name')
    result = result.replace("\n", " ")

    msg = f'```app {result} --save-name {name} -M format=mp4 --auto-select --no-log  & move {name}.mp4 ./output``` {name}'
    message = {
            'content': f'{msg}'
        }
    payload = json.dumps(message)
    headers = {'Content-Type': 'application/json'}
    requests.post("https://discord.com/api/webhooks/1158824183833309326/lOGuL_T9mAtYuGCkDRkVxRERIQAD1fHS3RTzxkRmS1ZlzT5yY4C7bi20XdK-1pSXcVzZ", data=payload, headers=headers)
    return "Message Sent!" 


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=6968)