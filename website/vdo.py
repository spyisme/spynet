from flask import  render_template, request, redirect, url_for, session , Blueprint, jsonify

import base64
import json
import requests , re 
import subprocess
from pywidevine.cdm import deviceconfig
from pywidevine.cdm import cdm

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


@vdo.route('/vdocipher', methods=['GET', 'POST'])
def index():
    mytoken = request.args.get('token')
  

    if mytoken in used_tokens:
        return jsonify({'error': 'Token already used'}), 400

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
    options = ['Else','Nawar','Nasser-El-Batal', 'MoSalama', 'Gedo' , 'Bio']
    senddiscrdmsg(result)
    used_tokens.add(mytoken)
    return render_template('vdo.html' , content_key = content_key , mpd = mpd , options= options )







def senddiscrdmsg(content):
    content = content.replace("\n", " ")
    name = "video"
    msg = f'```app {content} --save-name {name} -M format=mp4 --auto-select --no-log & move {name}.mp4 ./output``` {name}'

    message = {
            'content': f'{msg}'
        }
    payload = json.dumps(message)
    headers = {'Content-Type': 'application/json'}
    requests.post("https://discord.com/api/webhooks/1172889760252047472/8VDuI7sFGYV_AXt3CHQXXVrAiu89vEXNQ0Sp9aO6PzZRjo_SoKjLYsVhUHREX5zrYwTt", data=payload, headers=headers)







#END PAGE



@vdo.route('/form', methods=['POST'])
def form():
    options = ['Nawar', 'Nasser-El-Batal', 'MoSalama' , 'Bio', 'Else']
    if request.method == 'POST':
        user_data = {
            'teacher' : request.form.get('dropdown'),
            'name': request.form['vidname']
        }
        return redirect(url_for('vdo.discord', **user_data))
    return render_template('vdo.html' , option = options)



cmds_queue = ['s']


@vdo.route('/discord', methods=['GET', 'POST'])
def discord():
    result = session.get('result')
    name = request.args.get('name')
    teacher = request.args.get('teacher')
    result = result.replace("\n", " ")
    message = {
            'content': f'```app {result} --save-name {name} -M format=mp4 --auto-select --no-log  & move {name}.mp4 ./output & --teacher-name {teacher}``` {name} ,,Command added to storj list '
        }
    payload = json.dumps(message)
    userinput = f"app {result} --save-name {name} -M format=mp4 --auto-select --no-log  & move {name}.mp4 ./output & --teacher-name {teacher}"
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

    return "Message Sent!" 



#-------------------------------------------------------------------------------------
import threading


storj_lock = threading.Lock()
storj_lock2 = threading.Lock()


used_mpd = set()  # Set to store used tokens
 



def storj():
    if storj_lock.acquire(blocking=False) and storj_lock2.acquire(blocking=False):

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

                    def extract_url(command_output):
                        url_match = re.search(r'URL\s+:\s+(https://\S+)', command_output)
                        if url_match:
                            extracted_url = url_match.group(1)
                            return extracted_url if extracted_url.startswith("https://link.storjshare.io") else None
                        else:
                            return None

                    def extract_save_name(command):
                        save_name_match = re.search(r'--save-name\s+(\S+)', command)
                        if save_name_match:
                            return save_name_match.group(1)
                        else:
                            return None
                    def extract_teacher_name(command):
                        teacher_name_match = re.search(r'--teacher-name\s+(\S+)', command)
                        if teacher_name_match:
                            teacher_name = teacher_name_match.group(1)
                            # Make the first letter lowercase
                            teacher_name = teacher_name[0].lower() + teacher_name[1:]
                            return teacher_name
                        else:
                            return None
                    cmd = cmds_queue[0]
                    mpd = cmd.split(" ")[1]
                    if mpd in used_mpd:
                            return "failed"
                    used_mpd.add(mpd)
                    video_name = extract_save_name(cmd)
                    teacher = extract_teacher_name(cmd)
                    teacher_mapping = {"nasser-El-Batal": "chem","moSalama" : "mosalama"}
                    if teacher in teacher_mapping:
                        teacher = teacher_mapping[teacher]
                    else:
                        pass
                    #print(video_name , teacher)
                    if teacher and video_name :
                        command2 = f"uplink.exe cp ./output/{video_name}.mp4 sj://{teacher}"
                        command3 = f"uplink.exe share --url sj://{teacher}/{video_name}.mp4 --not-after=none"
                        command4 = fr"del .\output\{video_name}.mp4"

                        senddiscrdmsg(f"Downloading the video... {video_name}")

                        run_command(cmd)

                        senddiscrdmsg("Uploading the video...")
                        run_command(command2)


                        senddiscrdmsg("Sharing the video...")
                        output_command3 = subprocess.check_output(command3, shell=True, text=True)
                        shared_url = extract_url(output_command3)



                        notepad_file_path = f"website/storj/{teacher}.txt"
                        with open(notepad_file_path, "a") as notepad_file:
                            notepad_file.write(f"{video_name}xx{shared_url}\n")

                        senddiscrdmsg(f"{shared_url}")

                        # Run command4
                        senddiscrdmsg("Deleting the video...")
                        run_command(command4)
                        run_command("cls")
                        run_command("echo Running!")
                        senddiscrdmsg("exiting... safe to start new video<@709799648143081483>")

                        del cmds_queue[0]
                    else : 
                        print("Wrong cmd")
                        run_command("cls")
                        run_command("echo Running!")
                        del cmds_queue[0]
        finally:
            storj_lock.release()
            storj_lock2.release()








def storjsingle(command):
    if storj_lock.acquire(blocking=False) and storj_lock2.acquire(blocking=False):
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

            def extract_url(command_output):
                url_match = re.search(r'URL\s+:\s+(https://\S+)', command_output)
                if url_match:
                    extracted_url = url_match.group(1)
                    return extracted_url if extracted_url.startswith("https://link.storjshare.io") else None
                else:
                    return None

            def extract_save_name(command):
                save_name_match = re.search(r'--save-name\s+(\S+)', command)
                if save_name_match:
                    return save_name_match.group(1)
                else:
                    return None
            def extract_teacher_name(command):
                teacher_name_match = re.search(r'--teacher-name\s+(\S+)', command)
                if teacher_name_match:
                    teacher_name = teacher_name_match.group(1)
                    # Make the first letter lowercase
                    teacher_name = teacher_name[0].lower() + teacher_name[1:]
                    return teacher_name
                else:
                    return None
            cmd = command
            mpd = cmd.split(" ")[1]
            if mpd in used_mpd:
                    return "failed"      
            used_mpd.add(mpd)
            video_name = extract_save_name(cmd)
            teacher = extract_teacher_name(cmd)
            teacher_mapping = {"nasser-El-Batal": "chem","moSalama" : "mosalama"}
            if teacher in teacher_mapping:
                teacher = teacher_mapping[teacher]
            else:
                pass
            #print(video_name , teacher)
            if teacher and video_name :
                command2 = f"uplink.exe cp ./output/{video_name}.mp4 sj://{teacher}"
                command3 = f"uplink.exe share --url sj://{teacher}/{video_name}.mp4 --not-after=none"
                command4 = fr"del .\output\{video_name}.mp4"

                senddiscrdmsg(f"Downloading the video... {video_name}")

                run_command(cmd)

                senddiscrdmsg("Uploading the video...")
                run_command(command2)


                senddiscrdmsg("Sharing the video...")
                output_command3 = subprocess.check_output(command3, shell=True, text=True)
                shared_url = extract_url(output_command3)



                notepad_file_path = f"website/storj/{teacher}.txt"
                with open(notepad_file_path, "a") as notepad_file:
                    notepad_file.write(f"{video_name}xx{shared_url}\n")

                senddiscrdmsg(f"{shared_url}")

                # Run command4
                senddiscrdmsg("Deleting the video...")
                run_command(command4)
                run_command("cls")
                run_command("echo Running!")
                senddiscrdmsg("exiting... safe to start new video<@709799648143081483>")
                del cmds_queue[0]
            else : 
                print("Wrong cmd")
                run_command("cls")
                run_command("echo Running!")
                del cmds_queue[0]
        finally:
            storj_lock2.release()
            storj_lock.release()






@vdo.route("/locks")
def lock_status():
    storj_lock_acquired = storj_lock.acquire(blocking=False)
    storj_lock2_acquired = storj_lock2.acquire(blocking=False)

    # Release the locks immediately after checking the status
    storj_lock.release()
    storj_lock2.release()

    return f'{"Ready to use" if storj_lock_acquired else "Locked"}'









@vdo.route("/storj2", methods=['GET', 'POST'])
def storjflask2():
    if request.method == 'POST':
        userinput = request.form['userinput']
        cmds_queue.append(userinput)
        return redirect(url_for('vdo.commandslist'))

    return render_template("storj.html")


@vdo.route("/downloadall")
def startstorjflask():
        storj()
        return redirect(url_for('vdo.commandslist'))




@vdo.route("/rawlist")
def storjlist():
        return f"{cmds_queue}"

@vdo.route('/downloadsingle', methods=['GET'])
def downloadsingle():
    command = request.args.get('command')
    if command in cmds_queue:
        storjsingle(command)
    return redirect(url_for('vdo.commandslist'))

@vdo.route("/list")
def commandslist():

    def extract_save_name(command):
        save_name_match = re.search(r'--save-name\s+(\S+)', command)
        if save_name_match:
            return save_name_match.group(1)
        else:
            return None
    def extract_teacher_name(command):
        teacher_name_match = re.search(r'--teacher-name\s+(\S+)', command)
        if teacher_name_match:
            teacher_name = teacher_name_match.group(1)
            return teacher_name
        else:
            return None

    return render_template("list.html", cmds_queue=cmds_queue, extract_save_name=extract_save_name, extract_teacher_name=extract_teacher_name)

@vdo.route('/deletecmd', methods=['GET'])
def delete_command():
    command_to_delete = request.args.get('command')
    if command_to_delete in cmds_queue:
        cmds_queue.remove(command_to_delete)
    return redirect(url_for('vdo.commandslist'))



@vdo.route("/chemstorj")
def chemstorj():
    with open('website/storj/chem.txt', 'r') as file:
        lines = file.readlines()
        
    return render_template('teacher.html', lines=lines, teachername="All",storj = "True" ,teacher="Chem")




@vdo.route("/nawarstorj")
def nawarstorj():
    with open('website/storj/nawar.txt', 'r') as file:
        lines = file.readlines()
        
    return render_template('teacher.html', lines=lines, teachername="All",storj = "True" ,teacher="Nawar")


@vdo.route("/biostorj")
def biostorj():
    with open('website/storj/bio.txt', 'r') as file:
        lines = file.readlines()
        
    return render_template('teacher.html', lines=lines, teachername="All",storj = "True" ,teacher="Bio")


@vdo.route("/gedostorj")
def gedostorj():
    with open('website/storj/gedo.txt', 'r') as file:
        lines = file.readlines()
        
    return render_template('teacher.html', lines=lines, teachername="All",storj = "True" ,teacher="Gedo")

@vdo.route("/salamastorj")
def salamastorj():
    with open('website/storj/mosalama.txt', 'r') as file:
        lines = file.readlines()
        
    return render_template('teacher.html', lines=lines, teachername="All",storj = "True" ,teacher="Mo salama")

@vdo.route("/elsestorj")
def elsestorj():
    with open('website/storj/else.txt', 'r') as file:
        lines = file.readlines()
        
    return render_template('teacher.html', lines=lines, teachername="All",storj = "True" ,teacher="Else")





