import json
import os
import random
from datetime import date, time, datetime , timedelta
from sqlalchemy import not_
import shutil
import re
import requests
from flask import (
    Blueprint,
    jsonify,  
    redirect,
    render_template,
    render_template_string,
    request,
    send_file,
    session,
    url_for,
    abort,
    send_from_directory
)
from flask_login import current_user, login_user, logout_user
from flask_mail import Message
from google.auth.exceptions import GoogleAuthError
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

from . import mail
from .models import User, db

views = Blueprint('views', __name__)

SCOPES = ['https://www.googleapis.com/auth/youtube.readonly']

REDIRECT_URI = 'http://localhost:8080/oauth2callback'

TOKEN_STRING = {
    "token":
    "ya29.a0Ad52N38wmpNMPh55lHgtk8ou3TaUr9pO1rD8YQ4BIkNP6KdhmjsCLrOKPEGvPBHxnAAZpoM54Lxd2uXshy7YEutpFH1MjMHcPCtQVEmeKyp8nl7_29rE6zusVGHiUwKq8W6BASr1EYyAWUf_mLYNI2tselUPhUaMOsHNaCgYKAYASARASFQHGX2MiTRz94pflijZoACy4M5P5rQ0171",
    "refresh_token":
    "1//03ZAuoGB8P_PtCgYIARAAGAMSNwF-L9IrNJdAqry__XygiYCzsaV3pmjMiWGoGYRO76seff_ch2X9CyFxtYXPLhuEH5lddPA3uIM",
    "token_uri": "https://oauth2.googleapis.com/token",
    "client_id":
    "203680201166-nqeakc2q4vjsu20jmjmajcu68k3l5g43.apps.googleusercontent.com",
    "client_secret": "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",
    "scopes": ["https://www.googleapis.com/auth/youtube.readonly"],
    "universe_domain": "googleapis.com",
    "expiry": "2024-03-07T19:53:34.254535Z"
}


def get_authenticated_service():
    credentials = None

    try:
        # Parse the JSON string
        token_info = TOKEN_STRING
        credentials = Credentials.from_authorized_user_info(token_info)
    except GoogleAuthError as e:
        print(f"Couldn't log in: {e}")

    youtube = build('youtube', 'v3', credentials=credentials)
    return youtube


def convert_duration(duration):
    duration = duration[2:]
    hours, minutes, seconds = 0, 0, 0

    if 'H' in duration:
        hours = int(duration.split('H')[0])
        duration = duration.split('H')[1]

    if 'M' in duration:
        minutes = int(duration.split('M')[0])
        duration = duration.split('M')[1]

    if 'S' in duration:
        seconds = int(duration.split('S')[0])

    formatted_duration = '{:02d}:{:02d}:{:02d}'.format(hours, minutes, seconds)
    return formatted_duration


def get_playlist_videos(playlist_id):
    youtube = get_authenticated_service()

    # Fetch the playlist items
    playlist_items = []
    next_page_token = None

    while True:
        playlist_request = youtube.playlistItems().list(
            part='snippet',
            playlistId=playlist_id,
            maxResults=50,  # Adjust as needed
            pageToken=next_page_token)
        playlist_response = playlist_request.execute()

        playlist_items.extend(playlist_response['items'])
        next_page_token = playlist_response.get('nextPageToken')

        if not next_page_token:
            break

    videos = []

    for index, item in enumerate(playlist_items):
        video_id = item['snippet']['resourceId']['videoId']

        video_request = youtube.videos().list(part='contentDetails',
                                              id=video_id)
        video_response = video_request.execute()
        try:
            video_duration = video_response['items'][0]['contentDetails'][
                'duration']
        except IndexError:
            video_duration = "N/a"
        formatted_duration = convert_duration(video_duration)
        video_title = item['snippet']['title']

        videos.append({
            'id': video_id,
            'title': video_title,
            'duration': formatted_duration,
            'jsid': index
        })

    return videos


# Send a discord message (Log to #logs)
def discord_log_login(message):
    messageeeee = {'content': message}
    payload = json.dumps(messageeeee)
    headers = {'Content-Type': 'application/json'}
    requests.post(
        "https://discord.com/api/webhooks/1223513588527009802/V3innuq0yPRCsXlGWRkom4uXX5_f6AumLpgCd4N8glz84Py_GPp3F30UbWe9ZV_XEFzv",
        data=payload,
        headers=headers)


def discord_log_register(message):
    messageeeee = {'content': message}
    payload = json.dumps(messageeeee)
    headers = {'Content-Type': 'application/json'}
    requests.post(
        "https://discord.com/api/webhooks/1223552236727304313/GFdUeGUCKEQyH5YyR_4K7XG-2BlYKKnOZ_7jaeAVJhu8AQqyULsjPtOGsatMv9vnwAa7",
        data=payload,
        headers=headers)


def discord_log_backend(message):
    messageeeee = {'content': message}
    payload = json.dumps(messageeeee)
    headers = {'Content-Type': 'application/json'}
    requests.post(
        "https://discord.com/api/webhooks/1276724582866354327/-Xkth_SH8Yo9LFxuSxUyFiG5eU9Ga8aXT4gBtHoBy05ehTz5tYNloMXq4nd_6vcG8jfL",
        data=payload,
        headers=headers)
def discord_log_uptime(message):
    messageeeee = {'content': message}
    payload = json.dumps(messageeeee)
    headers = {'Content-Type': 'application/json'}
    requests.post(
        "https://discord.com/api/webhooks/1264918948730638336/nD1A8OVB0FmSgUVV7DCd2gumd7CBeTWAoq7AbqjCjwoRRkkgLRM7a8xuYRPOUos4AmwE",
        data=payload,
        headers=headers)

#Login , logout  (whitelist_ips is from EG)----------------------------------------------

blacklist_ips = set()
whitelist_ips = set()


@views.route('/login', methods=['GET', 'POST'])
def login():
    client_ip = request.headers.get('X-Forwarded-For')

    bypass = request.args.get('bypass')


    if client_ip:
        client_ip = client_ip.split(',')[0].strip()
    else:
        client_ip = request.headers.get('CF-Connecting-IP',
                                        request.remote_addr)



    if bypass :
        try :
            blacklist_ips.remove(client_ip)
            whitelist_ips.add(client_ip)

        except :
            whitelist_ips.add(client_ip)

    user_agent = request.headers.get('User-Agent')

    if current_user.is_authenticated:
        return redirect(url_for('views.home'))

    if client_ip == "127.0.0.1":
        whitelist_ips.add(client_ip)

    if client_ip in blacklist_ips:
        return jsonify(message=f"Error 403 your ip is {client_ip}")

    if client_ip not in whitelist_ips:
        api_url = f'https://ipinfo.io/{client_ip}?token=8f8d5a48b50694'
        response = requests.get(api_url)
        data = response.json()

        if 'country' in data:
            country_code = data['country']
            if country_code != 'EG':
                blacklist_ips.add(client_ip)
                return jsonify(message="Please disable vpn/proxy.")
        else:
            blacklist_ips.add(client_ip)
            return jsonify(
                message="Unable to determine the country. Login failed.")

    whitelist_ips.add(client_ip)

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        username = username.replace(" ", "")  
        username = username.lower()
        user = User.query.filter_by(username=username).first()

        #To get the username using the Username/email
        if user:
            pass
        else:
            user = User.query.filter_by(email=username).first()

        if user:

            # if user.username not in ['spy'] and user.active_sessions >= 3:

                # discord_log_login(
                #     f"{username} tried to login from more than 3 devices <@709799648143081483>"  
                # )

                # return redirect(f"/login?maxdevices=yes&user={username}")

            if user.password == "password":
                return redirect(f"forgotpassword?user={username}")

            if password == user.password:
                login_user(user)
                user.active_sessions += 1
                db.session.commit()
                discord_log_login(
                    f"{client_ip} just logged in with {username} Device ```{user_agent}```  <@709799648143081483>"  
                )
                session.permanent = True
                return render_template('used_pages/landing.html')

            else:
                discord_log_login(
                    f"{client_ip} just failed to login with '{username}' Device ```{user_agent}``` <@709799648143081483>"  
                )
                return redirect(f"/login?password=false&user={username}")
        else:
            discord_log_login(
                f"{client_ip} just failed to login with '{username}' Device ```{user_agent}``` <@709799648143081483>"  
            )
            return redirect("/login?failed=true")
    return render_template('users_pages/login.html',
                           password=request.args.get("password"),
                           failed=request.args.get("failed"),
                           username=request.args.get("user"),
                           maxdevices=request.args.get("maxdevices"),
                           msg=request.args.get('msg'))


@views.route('/logout')
def logout():

    client_ip = request.headers.get('X-Forwarded-For')

    if client_ip:
        client_ip = client_ip.split(',')[0].strip()
    else:
        client_ip = request.headers.get('CF-Connecting-IP',
                                        request.remote_addr)
    current_user.active_sessions -= 1
    db.session.commit()
    discord_log_login(
        f"<@709799648143081483> {current_user.username} Logged out from {client_ip}")

    logout_user()
    return redirect(url_for('views.login'))


#Register , Forget Password--------------------------------------------------------------
def read_html_file(file_path, **kwargs):
    with open(file_path, 'r') as file:
        template = file.read()
    return render_template_string(template, **kwargs)


#Error handling?
@views.route('/forgotpassword', methods=['GET', 'POST'])
def forgotpassword():
    if current_user.is_authenticated:
        return redirect(url_for('views.home'))

    client_ip = request.headers.get('X-Forwarded-For')

    if client_ip:
        client_ip = client_ip.split(',')[0].strip()
    else:
        client_ip = request.headers.get('CF-Connecting-IP',
                                        request.remote_addr)

    user_agent = request.headers.get('User-Agent')
    username = request.args.get('user')
    msgg = request.args.get('msg')

    user = User.query.filter_by(username=username).first()
    if user:
        pass
    else:
        user = User.query.filter_by(email=username).first()
    if request.method == 'GET':  
        if user:  
            if user.otp == 'bypassotp':
                login_user(user)
                if user.username != 'spy':
                    user.active_sessions += 1
                db.session.commit()
                discord_log_login(
                    f"{client_ip} just logged in with {username} Device ```{user_agent}```  <@709799648143081483>"  
                )
                session.permanent = True
                return redirect(url_for('views.home'))
            elif user.otp == "Waiting approval":
                return 'Please wait to get approved'
            recipient = user.email
            if recipient:
                subject = "Account 2FA"

                random_number = random.randint(100000, 999999)

                user.otp = random_number
                db.session.commit()

                html_content = read_html_file(
                    'website/templates/users_pages/2fa.html', otp=user.otp)

                msg = Message(subject, recipients=[recipient])
                msg.html = html_content
                mail.send(msg)
                discord_log_login(f"Sent an otp to : {user.username}")

    if request.method == 'POST':
        otp = request.form.get('otp')
        if otp == user.otp:  
            # if user.username not in [
            #         'spy',
            #         'biba'  
            # ] and user.active_sessions >= 3:  

            #     discord_log_login(
            #         f"{username} tried to login from more than 3 devices <@709799648143081483>"
            #     )
            #     return redirect(f"/login?maxdevices=true&user={username}")

            login_user(user)

            user.active_sessions += 1  

            user.otp = "null"  
            user.password = "Chnageme"  

            db.session.commit()

            discord_log_login(
                f"{client_ip} just logged in with {username} Device ```{user_agent}```  <@709799648143081483>"
            )

            session.permanent = True

            return  render_template('used_pages/landing.html')
        else:
            return redirect(
                f'/forgotpassword?msg=failedtologin&user={username}')

    return render_template(
        'users_pages/verify.html',
        email=user.email,  
        msg=msgg)


@views.route('/change_password', methods=['GET', 'POST'])
def change_password():
    if request.method == 'POST':
        password = request.form.get('Password')
        password2 = request.form.get('Password2')

        if password != password2:
            return redirect('/change_password?passwords=dontmatch')

        current_user.password = password

        db.session.commit()

        return render_template('used_pages/landing.html')

    return render_template('users_pages/password.html',
                           msg=request.args.get("passwords"))


#Add requiremts
@views.route('/register', methods=['GET', 'POST'])
def registeracc():
    if current_user.is_authenticated:
        return redirect(url_for('views.home'))
    

    client_ip = request.headers.get('X-Forwarded-For')
    user_agent = request.headers.get('User-Agent')

    if client_ip:
        client_ip = client_ip.split(',')[0].strip()
    else:
        client_ip = request.headers.get('CF-Connecting-IP',
                                        request.remote_addr)

    if client_ip in blacklist_ips:
        return jsonify(message=f"Please disable vpn/proxy. Current ip : {client_ip}"), 403

    if client_ip not in whitelist_ips:
        api_url = f'https://ipinfo.io/{client_ip}?token=8f8d5a48b50694'
        response = requests.get(api_url)

        if response.status_code == 200 :
            data = response.json()

            if 'country' in data:
                country_code = data['country']
                if country_code != 'EG':
                    blacklist_ips.add(client_ip)
                    return jsonify(message=f"Please disable vpn/proxy. Current ip : {client_ip}")
            else:
                blacklist_ips.add(client_ip)
                return jsonify(
                    message="Unable to determine the country. Login failed.")



    whitelist_ips.add(client_ip)


    if request.method == 'POST':
        username = request.form.get('username')
        user = User.query.filter_by(username=username).first()

        if user:
            return "Username is taken try another"
        email = request.form.get('email')
        number = request.form.get('number')
        stage = request.form.get('stage')


        #Need to have a web-interface

        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'

        if(re.fullmatch(regex, email)):
            pass
        else :
            return 'Invaild Email Address'
        
        if re.match(r'^01\d{8,}$', number):
            pass
        else :
            return "Invaild Phone Number"
        
        if re.match(r'^[a-zA-Z0-9]+$', username):
            pass
        else :
            return "Invaild Username"
        



        new_user = User(
            username=username,  
            password="password",  
            email=email,  
            otp="Waiting approval",
            type ="student_register",
            stage = stage ,
            phone_number =number,
            created_by= "registration")  

        db.session.add(new_user)
        db.session.commit()

        discord_log_register(
            f"New user  : {username} ====== {email} ====== {number} ====== {client_ip} ====== {user_agent} <@709799648143081483>"
        )

        login_user(new_user)
        session.permanent = True

        return redirect(f"/send_email?to={email}")
    return render_template('users_pages/register.html',
                           done=request.args.get("done") ,
                           data=[{
                               'name': 3
                           }, {
                               'name': 2
                           }, {
                               'name': 1
                           }])


#Dont edit------------------------------------------------------------------------------------------------
@views.route('/redirect/<path:link>')
def redirectlinks(link):
    link = link.replace('questionmark', '?')
    link = link.replace('andsympol', '&').replace(':', ':/')  #For iphone
    return redirect(f"{link}")


@views.route('/favicon.ico')
def favicon():
    return redirect("/static/favicon.ico")


@views.route('/Robots.txt')
def robots_txt1():
    return ""

@views.route('/robots.txt')
def robots_txt():
    return ""

@views.route('/monitor')  #Uptime robot
def monitor():
    return "Working"


@views.route('/check_username', methods=['POST'])
def check_username():
    data = request.get_json()
    stored_username = data.get('username')
    if current_user.type != 'admin': 
    # Compare the stored username with the current_user's username
        if current_user.is_authenticated and stored_username != current_user.username:
            # Log out the user if the usernames don't match
            logout_user()
            return jsonify(logout=True)
    
    return jsonify(logout=False)

#Home---------------------------------------------------------------------------------------------


def load_stage_data(stage):
    with open(f'website/Backend/stage{stage}_data.json', 'r') as file:
        return json.load(file)


@views.route("/subjects")
def subjectspage():
    end_date = current_user.subscription_date + timedelta(days=30)
    password = request.args.get("password")

    data = load_stage_data(current_user.stage)
    # with open('website/Backend/data.json') as f:
    #     data = json.load(f)

    lines = list(data.keys())
    return render_template('used_pages/all.html',
                           lines=lines,
                           teachername="All",
                           password=password , end_date = end_date)






@views.route("/")
def home():
    if current_user.is_authenticated:
        return redirect(url_for('views.subjectspage'))
    
    return render_template('users_pages/home.html')


#User pages---------------------------------------------------------------------------


#Subject
@views.route("/subjects/<subject>")
def subjects(subject):
    teachers = None
    data = load_stage_data(current_user.stage)

    # with open('website/Backend/data.json') as f:
    #     data = json.load(f)
    if subject in data:
        teachers = [{
            "name":
            teacher["name"],
            "badge":
        teacher.get("badge", ""),
            "link":
            teacher["link"],
            "description":
            teacher.get("description", "")
            or f"{len(teacher['courses'])} courses"
        } for teacher in data[subject]["teachers"]]
    else:
        abort(404)

    return render_template('used_pages/subjects.html',
                           teachername=subject,
                           teacher_links=teachers)


#Teacher
@views.route("/subjects/<subject>/<teacher_name>")
def teacher(subject, teacher_name):
    courses = None
    data = load_stage_data(current_user.stage)
    if subject in data:
        for teacher in data[subject]["teachers"]:
            if teacher["link"] == teacher_name:
                courses = teacher.get("courses")
                description = teacher.get("description")
                for item in courses:
                    item['link'] = item['name']
                break

    if courses == None:  
        abort(404)


    return render_template('used_pages/teacher.html',
                           teachername=subject,
                           teacher_links=courses,
                           teacher_name=teacher_name,
                           description=description)


#Videos
@views.route("/subjects/<subject>/<teacher_name>/<course_name>")
def videos(subject, teacher_name, course_name):
    videos = None
    playlist_id = None
    folder = None

    if " " in course_name :
        course_name = course_name.replace(' ', '-')
        return redirect(f'/subjects/{subject}/{teacher_name}/{course_name}')

    if "-" in course_name:
        course_name = course_name.replace('-', ' ')

    data = load_stage_data(current_user.stage)

    # with open('website/Backend/data.json') as f:
    #     data = json.load(f)
    if subject in data:
        for teacher in data[subject]["teachers"]:
            if teacher.get("link") == teacher_name:
                for course in teacher.get("courses", []):
                    description = teacher.get("description")

                    if course.get("name") == course_name:
                        videos = course.get('videos', '')
                        playlist_id = course.get('playlist_id', '')
                        folder = course.get('folder', '')

    if videos == None:  
        abort(404)

    teachername = course_name

    return render_template('used_pages/videopage.html',
                           videos=videos,
                           playlist_id=playlist_id,
                           teachername=teachername,
                           folder=folder,
                           description=description)


#-----------------------------------------Ashraf el shenawy----------------


@views.route("/subjects/chemistry/ashrafelshenawy")
def ashrafelshemawy():

    return render_template('used_pages/ashraf.html')

#-----------------------------------------Basic Course mo adel----------------
@views.route("/subjects/physics/mohamedadel/Basic-Course")
def basiccoursemoadel():

    return redirect('https://www.youtube.com/watch?v=Mhcuu-A7RT8&list=PLM-GVlebsoPX_GMg2uu7IGI1bN0idBYOu')

#The leader---------------------------------------------------------------------

def getuploadedlec():
    headers = {
        "deviceid": "s",
    }
    proxy = {
    "http": "http://nprofi:6f0reuyu@139.171.104.74:29842",
    "https": "http://nprofi:6f0reuyu@139.171.104.74:29842"
}
    
    response = requests.get(
        "https://api.theleadersacademy.online/api/classroom/get/mrhossamonline25",
        headers=headers , proxies=proxy)

    data = response.json()



    allowed_types=['video', 'document', 'webcontent']

    lectures_with_units = []

    # Find the "Main Lectures" tab
    for tab in data['data']['tabs']:
        if tab['name'] == "Main Lectures":
            for section in tab['sections']:
                if section['name'] == "Online Lectures":
                    for course in section['courses']:
                        # Initialize the lecture info with name and id
                        lecture_info = {
                            "lecture_id": course['id'],
                            "lecture_name": course['name'],
                            "units": []
                        }
                        
                        # Extract units of allowed types
                        for unit in course['units']:
                            if unit['type']['name'].lower() in allowed_types:
                                lecture_info["units"].append([unit['id'], unit['name'], unit['type']['name']])
                        
                        lectures_with_units.append(lecture_info)

    lectures_with_units.insert(0, {"lecture_id": "", "lecture_name": "Choose a Lecture"})


    return  lectures_with_units


@views.route("/subjects/english/theleader")
def theleadersessions():
    lectures_with_units = getuploadedlec()

    return render_template('used_pages/theleader.html' , lectures = lectures_with_units ) 


def find_a_working_acc(url):
        with open('website/Backend/theleaderaccs.json', 'r') as file:
            accounts = json.load(file)

        for account in accounts:
            proxy = {
                "http": "http://nprofi:6f0reuyu@139.171.104.74:29842",
                "https": "http://nprofi:6f0reuyu@139.171.104.74:29842"
            }
            headers = {
                'Accept': '*/*',
                'Cache-Control': 'no-cache',
                'Connection': 'keep-alive',
                'Content-Type': 'application/json',
                'DeviceId': 's',
            }

            email = account['email']
            password = account['password']
            json_data = {
                'identifier': email,
                'password': password,
                'device': {
                    'browser': {
                        'name': 's',
                        'version': 's',
                        'major': 's',
                    },
                    'os': {
                        'name': 's',
                        'version': 's',
                    },
                    'device': {
                        'type': 's',
                        'id': 's',
                    },
                },
            }

            response = requests.post(
                'https://api.theleadersacademy.online/api/auth/login',
                headers=headers,
                json=json_data , proxies= proxy)

            token = response.json()['data']['token']
            headers = {"Authorization": f"Bearer {token}"}

            response = requests.get(url, headers=headers , proxies= proxy)
            if response.status_code == 200:
                return response 


def add_to_json(video_id, link, json_file_path='website/Backend/theleader.json', content_type='video'):
    if os.path.exists(json_file_path):
        with open(json_file_path, 'r') as json_file:
            data = json.load(json_file)
    else:
        data = {"video": {}, "webcontent": {}, "document": {}}

    # Add the link to the corresponding section based on content type
    if content_type == 'video':
        data["video"][video_id] = link
    elif content_type == 'webcontent':
        data["webcontent"][video_id] = link
    elif content_type == 'document':
        data["document"][video_id] = link

    # Save the updated JSON back to the file
    with open(json_file_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)


@views.route("/subjects/english/theleader/session/<type>/<id>")
def theleaderfinal(type , id):
    if type == 'video':
        json_file_path = 'website/Backend/theleader.json'
            
        if os.path.exists(json_file_path):
            with open(json_file_path, 'r') as json_file:
                data = json.load(json_file)
                if id in data["video"]:
                    link =  data["video"][id].strip() 
                else: 
                    video = find_a_working_acc(f"https://api.theleadersacademy.online/api/video/play/{id}")
                    

                    video = video.json()
                    video = video["data"]["details"]["iframe"]

                    match = re.search(r'src="([^"]+)"', video)
                    if match:
                        link = match.group(1)
                        add_to_json(id, link, content_type='video')

    elif type == 'webcontent':

        json_file_path = 'website/Backend/theleader.json'
            
        if os.path.exists(json_file_path):
            with open(json_file_path, 'r') as json_file:
                data = json.load(json_file)
                if id in data["webcontent"]:
                    link =  data["webcontent"][id].strip() 
                else: 
                    webcontent = find_a_working_acc(f"https://api.theleadersacademy.online/api/web-content/{id}")

                    webcontent = webcontent.json()
                    webcontent = webcontent["data"]["content"]
                    match = re.search(r'href="([^"]+)"', webcontent)
                    if match:
                        link = match.group(1)
                        add_to_json(id, link, content_type='webcontent')
                        # print(link)

    elif type == 'document':
        json_file_path = 'website/Backend/theleader.json'
            
        if os.path.exists(json_file_path):
            with open(json_file_path, 'r') as json_file:
                data = json.load(json_file)
                if id in data["document"]:
                    link =  data["document"][id].strip() 
                else: 
                    document = find_a_working_acc(f"https://api.theleadersacademy.online/api/document/{id}")

                    document = document.json()
                    link = document["data"]["uri"]
                    add_to_json(id, link, content_type='document')
  

    return redirect(link)


#Update videos-----------------------------------------------------------------

@views.route("/subjects/<subject>/<teacher_name>/<course_name>/update")  
def update(subject, teacher_name, course_name):
    videos = None
    if "-" in course_name:

        course_name = course_name.replace('-', ' ')

    #Needs a solution
    data = load_stage_data(current_user.stage)

    if subject in data:
        for teacher in data[subject]["teachers"]:
            if teacher.get("link") == teacher_name:
                # Find the specific course
                for course in teacher.get("courses", []):
                    if course.get("name") == course_name:
                        playlist_id = course.get('playlist_id', '')
                        videos = get_playlist_videos(playlist_id)
                        course['videos'] = videos
                        with open(
                                f'website/Backend/stage{current_user.stage}_data.json',
                                'w') as f:
                            json.dump(data, f, indent=4)
    if " " in course_name :
        course_name = course_name.replace(' ', '-')
    return redirect(f'/subjects/{subject}/{teacher_name}/{course_name}')
    # return videos


#Admin pages

#Manage users-----------------------------------------------------------------------


@views.route('/admin')
def admin():
    if current_user.type != 'admin':
        return "User is not an admin"
    
    users = User.query.all() 

    user_count = User.query.count()

    expired_users = 0


    # for user in users:
    #     if user.subscription_date:
    #         # Ensure both are datetime objects
    #         subscription_datetime = datetime.combine(user.subscription_date, datetime.min.time())
    #         if datetime.now() - subscription_datetime >= timedelta(days=30):
    #             user.expired = True
    #             expired_users = expired_users + 1
    #             # Optionally save the updated user state to the database
    #             # db.session.commit()
                
    return render_template('admin/admin.html', users=users , expired_users = expired_users  ,user_count = user_count)


@views.route('/admin-create', methods=['GET', 'POST'])
def create_user_route():
    if current_user.type != 'admin':
        return "User is not an admin"

    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        stage = request.form.get('stage')
        phone = request.form.get('phone')
        paid_status = request.form.get('paid')

        if not username:
            return jsonify({'error':
                            'Username and password are required'}), 400

        existing_user = User.query.filter_by(username=username).first()

        if existing_user:
            return jsonify({'error': 'Username already exists'}), 400
        
        if paid_status == 'Yes':
            subscription_method = request.form.get('sub_method')
            subscription_date = datetime.strptime(request.form.get('sub_date'), '%Y-%m-%d').date()

            new_user = User(
                username=username,
                password="password",
                email=email,
                stage=stage,
                otp="null"
                ,subscription_method= subscription_method,
                subscription_date = subscription_date,
                created_by = current_user.username
                )  
        else:
         
         new_user = User(
                username=username,
                password="password",
                email=email,
                stage=stage,
                otp="null",
                phone_number= phone,
                created_by = current_user.username
                )  
         
        db.session.add(new_user)
        db.session.commit()

        discord_log_backend("<@709799648143081483> " + current_user.username +
                            " created new account " + username)

        return redirect("/admin")

    return render_template('admin/user_create.html',
                           data=[{'name': "3"}, {'name': "2"}, {'name': "1"}],
                           sub_methods = [{'name': "Vodafone Cash" } , {'name' : "InstaPay"}])


@views.route('/user-manage/<user_id>', methods=['GET', 'POST'])
def manage_user(user_id):
    user = User.query.get(user_id)

    if user_id == -1:
        if current_user.id != -1:
            return "You cant edit"

    if not user:
        return "User not found", 404

    if request.method == 'POST':
        # Handle form submission to update user details
        username = request.form.get('username')

        existing_user = User.query.filter_by(username=username).first()

        if existing_user and existing_user.username != user.username:
            return jsonify({'error': 'Username already exists'}), 400

        user_before = {
            'username': user.username,
            'email': user.email,
            'stage': user.stage,
            'phone_number': user.phone_number,
            'password': user.password,
            'active_sessions': user.active_sessions,
            'subscription_method': user.subscription_method,
            'subscription_date': user.subscription_date,
        }
        user.username = request.form.get('username')
        user.email = request.form.get('email')
        user.stage = request.form.get('stage')
        user.phone_number =  request.form.get('phone')

        if current_user.username == 'spy' :
            user.password = request.form.get('password')

        user.active_sessions = request.form.get('devices')
        if user.type != 'admin' :
            user.subscription_method = request.form.get('sub_method')
            user.subscription_date = datetime.strptime(request.form.get('sub_date'), '%Y-%m-%d').date()
        changes = {}

        # Compare each field to identify changes
        for key, value in user_before.items():
            if getattr(user, key) != value:

                discord_log_backend(f'{key} for user {user.username} was {value} and now is {getattr(user, key)} by {current_user.username}')
                changes[key] = {
                    'before': value,
                    'after': getattr(user, key)
                }


        db.session.commit()
        return redirect(url_for('views.manage_user',user_id=user_id)) 

    # Render the manage user template
    return render_template('admin/manage.html',
                           user=user,
                           data=[{'name': "1"}, {'name': "2"}, {'name': "3"}],
                           sub_methods = [{'name': "Vodafone Cash" } , {'name' : "InstaPay"}])






@views.route('/approve/<user_id>', methods=['GET', 'POST'])
def approve(user_id):
    if user_id == -1:
        return "You cant edit"
    user = User.query.filter_by(id=user_id).first()
    user.otp = "null"  
    db.session.commit()

    recipient = user.email  
    subject = "Account Approved"

    html_content = read_html_file(
        'website/templates/users_pages/account_created.html',
        username=user.username)  

    msg = Message(subject, recipients=[recipient])
    msg.html = html_content
    mail.send(msg)
    discord_log_backend(f"{current_user.username} approved {user.username}")
    return redirect(url_for('views.manage_user', user_id=user_id))


@views.route('/disable/<user_id>', methods=['GET', 'POST'])
def disable(user_id):
    if current_user.type != 'admin':
        return "User is not an admin"
    if user_id == -1:
        return "You cant edit"

    user = User.query.filter_by(id=user_id).first()
    user.otp = "Waiting approval"  
    db.session.commit()

    discord_log_backend(f"{current_user.username} disabled {user.username}")

    return redirect(url_for('views.manage_user', user_id=user_id))


def upload_file_to_discord(webhook_url, file_path):
    with open(file_path, 'rb') as file:
        files = {'file': file}
        requests.post(webhook_url, files=files)


import zipfile


@views.route('/uptime-backup')
def uptimebackup():

    zip_filename = 'website/stagesdata.zip'
    files_to_zip = [
        'website/Backend/stage1_data.json', 'website/Backend/stage2_data.json',
        'website/Backend/stage3_data.json'
    ]

    # Create a ZIP file
    os.remove('website/stagesdata.zip')

    with zipfile.ZipFile(zip_filename, 'w') as zipf:
        for file in files_to_zip:
            zipf.write(file)

    db_path = os.path.join(os.path.dirname(__file__), '..', 'instance',
                           'site.db')

    upload_file_to_discord(
        "https://discord.com/api/webhooks/1273289183993008241/bAsFwfve1lDTaFv4e4q8F4z--raNqKQbkLTW5lsHqyTwS5QkGS3uOSEN01NVhmmCuFmt",
        "website/stagesdata.zip")
    upload_file_to_discord(
        "https://discord.com/api/webhooks/1273288058808045679/-k8Tc5AWGZGroG3swyknC2y_EEWXfvQQUDyLiZnsHeqtWu4UQbLe-ZBJLABZH6hx2AtH",
        db_path)
    discord_log_uptime("UptimeRobot Backup")
    return "Done"


@views.route('/stages-data')
def stages_data():
    if current_user.type != 'admin':
        return "User is not an admin"

    zip_filename = 'website/stagesdata.zip'
    files_to_zip = [
        'website/Backend/stage1_data.json', 'website/Backend/stage2_data.json',
        'website/Backend/stage3_data.json'
    ]

    try:
        os.remove('website/stagesdata.zip')
    except:
        pass
    # Create a ZIP file
    with zipfile.ZipFile(zip_filename, 'w') as zipf:
        for file in files_to_zip:
            zipf.write(file)

    upload_file_to_discord(
        "https://discord.com/api/webhooks/1273289183993008241/bAsFwfve1lDTaFv4e4q8F4z--raNqKQbkLTW5lsHqyTwS5QkGS3uOSEN01NVhmmCuFmt",
        "website/stagesdata.zip")
    return send_file("stagesdata.zip")


@views.route('/database')
def database():
    if current_user.type != 'admin':
        return "User is not an admin"

    # Construct the absolute path to the database file
    db_path = os.path.join(os.path.dirname(__file__), '..', 'instance',
                           'site.db')
    if not os.path.exists(db_path):
        return "Database file not found."

    upload_file_to_discord(
        "https://discord.com/api/webhooks/1273288058808045679/-k8Tc5AWGZGroG3swyknC2y_EEWXfvQQUDyLiZnsHeqtWu4UQbLe-ZBJLABZH6hx2AtH",
        db_path)
    return send_file(db_path)


@views.route('/user-delete/<user_id>', methods=['GET', 'POST'])
def delete_user(user_id):
    if current_user.type != 'admin':
        return "User is not an admin"

    user_to_delete = User.query.get(user_id)

    if user_to_delete.username in ['spy', 'biba']:  
        return "Cant delete user"
    
    if user_to_delete.type == "admin":
        if current_user.username != 'spy':
            return "Cant delete user"

    if not user_to_delete:
        return jsonify({'error': 'User not found'}), 404

    discord_log_backend("<@709799648143081483> " + current_user.username +
                        " deleted " + user_to_delete.username)

    db.session.delete(user_to_delete)
    db.session.commit()

    return redirect("/admin")

@views.route('/send_email', methods=['GET', 'POST'])
def send_email():

    recipient = request.args.get('to')
    subject = "Account Registration Confirmation"

    email = User.query.filter_by(email=recipient).first()

    if email:

        html_content = read_html_file(
            'website/templates/users_pages/email.html')

        msg = Message(subject, recipients=[recipient])  
        msg.html = html_content

        try:
            mail.send(msg) 
            return render_template('used_pages/landing.html')
    
        except Exception as e:
            discord_log_backend(f"Error Sending the email to {recipient} : {e}")
            return render_template('used_pages/landing.html')
    else:
        return "Email doesnt exist"




@views.route('/edit_active_sessions/<user_id>', methods=['POST'])
def edit_active_sessions(user_id):
    if current_user.type != 'admin':
        return "User is not an admin"
    if request.method == 'POST':
        if current_user.username not in ['spy', 'skailler', 'behary']:
            return "..."
        new_active_sessions = request.form.get('value')

        if not new_active_sessions:
            return jsonify(
                {'error': 'New value for active_sessions is required'}), 400

        user = User.query.get(user_id)

        if user:
            user.active_sessions = new_active_sessions

            db.session.commit()
            if current_user.username != "spy":
                discord_log_backend("<@709799648143081483> " +
                                    current_user.username +
                                    " edited sessions for " + user.username)

            return redirect("/admin")
        else:
            return jsonify({'error': 'User not found'}), 404

    return jsonify({'error': 'Method not allowed'}), 405


@views.route('/edit_email/<user_id>', methods=['POST'])
def edit_email(user_id):
    if current_user.type != 'admin':
        return "User is not an admin"

    if request.method == 'POST':
        new_email = request.form.get('value')

        user = User.query.get(user_id)

        if user:
            user.email = new_email

            db.session.commit()
            if current_user.username != "spy":
                discord_log_backend("<@709799648143081483> " +
                                    current_user.username +
                                    " edited email for " + user.username)

            return redirect("/admin")
        else:
            return jsonify({'error': 'User not found'}), 404

    return jsonify({'error': 'Method not allowed'}), 405


#Edit pages-----------------------------------------------------------------------


def load_data():
    with open('website/Backend/data.json', 'r') as file:
        return json.load(file)


def save_data(data, stage):
    timestamp = datetime.now().strftime("%m.%d-%H")
    backup_filename = f"website/Backend/dumps/Stage{stage}_{timestamp}.json"
    os.makedirs(os.path.dirname(backup_filename), exist_ok=True)

    # Backup the current data.json
    with open(f'website/Backend/stage{stage}_data.json', 'r') as file:
        current_data = file.read()
    with open(backup_filename, 'w') as backup_file:
        backup_file.write(current_data)

    with open(f'website/Backend/stage{stage}_data.json', 'w') as file:
        json.dump(data, file, indent=4)


#Add/remove a subject
@views.route('/subjects/edit', methods=['POST', 'GET'])
def manage_subjects():

    if current_user.type != 'admin':
        return "User is not an admin"

    data = load_stage_data(current_user.stage)
    if request.method == 'POST':
        if request.form['action'] == 'Add':

            subject = request.form['newSubject']

            file = request.files['file']

            if file:
                os.makedirs(os.path.dirname(
                    f'website/static/assets/Stage{current_user.stage}/homepage/'
                    + subject + '.jpg'),
                            exist_ok=True)

                file.save(
                    f'website/static/assets/Stage{current_user.stage}/homepage/{subject}.jpg'
                )

            else:
                return "Choose an imgae for the teacher"

            if subject == "":
                return "Subject is none "
            if subject not in data:
                data[subject] = {"teachers": []}
                save_data(data, current_user.stage)
                return redirect(url_for('views.manage_subjects'))

            else:
                return jsonify(
                    {"message": f"Subject '{subject}' already exists!"}), 400

        if request.form['action'] == 'Remove':
            subject = request.form['removeSubject']
            try:
                os.remove(
                    f'website/static/assets/Stage{current_user.stage}/homepage/{subject}.jpg'
                )
                shutil.rmtree(f"website/static/assets/Stage{current_user.stage}/{subject}/")

            except :
                pass

            if subject == "":
                return "Subject is none "
            if subject in data:
                del data[subject]
                save_data(data, current_user.stage)
                return redirect(url_for('views.manage_subjects'))
            else:
                return jsonify(
                    {"message": f"Subject '{subject}' does not exist!"}), 400

    return render_template('data/subjects.html', data=list(data.keys()))


#Add/remove a teacher
@views.route('/subjects/<subject>/edit', methods=['POST', 'GET'])
def manage_teachers(subject):
    if current_user.type != 'admin':
        return "User is not an admin"
    data = load_stage_data(current_user.stage)
    teachers = data[subject].get('teachers', [])
    teacher_list = [{
        'name': teacher['name'],
        'link': teacher['link']
    } for teacher in teachers]

    if request.method == 'POST':
        if request.form['action'] == 'Add':
            teacher_name = request.form['new']
            teacher_link = request.form['new2']

            file = request.files['file']
            if teacher_name == "":
                return "Teacher name is none "

            for entry in teacher_list:
                if teacher_link in entry['link']:
                    return "Link is taken already"
                
            if file:
                directory = f"website/static/assets/Stage{current_user.stage}/{subject}"
                if not os.path.exists(directory):
                    os.makedirs(directory)
                    
                file.save(f'{directory}/'+ teacher_link + '.jpg')

            else:
                return "Choose an imgae for the teacher"



            if subject in data:
                new_teacher = {
                    "name": teacher_name,
                    "link": teacher_link,
                    "courses": [],
                    "description": ""
                }
                data[subject]['teachers'].append(new_teacher)
                save_data(data, current_user.stage)
                return redirect(
                    url_for('views.manage_teachers', subject=subject))

            else:
                return jsonify(
                    {"message": f"Subject '{subject}' does not exist!"}), 400

        if request.form['action'] == 'Remove':
            teacher_name = request.form['remove']
            try:
                os.remove(
                    f'website/static/assets/Stage{current_user.stage}/{subject}/'
                    + teacher_name + '.jpg')
                shutil.rmtree(f"website/static/assets/Stage{current_user.stage}/{subject}/{teacher_name}")
                       
            except:
                pass
            if teacher_name == "":
                return "Teacher name is none "
            if subject in data:
                if 'teachers' in data[subject]:
                    teacher_exists = any(
                        teacher['link'] == teacher_name
                        for teacher in data[subject]['teachers'])
                    if teacher_exists:
                        data[subject]['teachers'] = [
                            teacher for teacher in data[subject]['teachers']
                            if teacher['link'] != teacher_name
                        ]
                        save_data(data, current_user.stage)
                        return redirect(
                            url_for('views.manage_teachers', subject=subject))
                    else:
                        return jsonify({
                            "message":
                            f"Teacher '{teacher_name}' does not exist in subject '{subject}'!"  
                        }), 400  

            else:
                return jsonify(
                    {"message": f"Subject '{subject}' does not exist!"}), 400

    return render_template('data/teachers.html',
                           data=teacher_list,
                           subject=subject)


#Add/remove a course
@views.route('/subjects/<subject>/<teachername>/edit', methods=['POST', 'GET'])
def manage_courses(subject, teachername):
    if current_user.type != 'admin':
        return "User is not an admin"
    data = load_stage_data(current_user.stage)

    teachers = data.get(subject, {}).get('teachers', [])

    teacher_courses = next(
        (teacher['courses']
         for teacher in teachers if teacher['link'] == teachername), None)

    course_names = [course['name']
                    for course in teacher_courses]  

    teacherinfo = None

    for teacher in teachers:
        if teacher['link'] == teachername:
            teacherinfo = teacher

    if request.method == 'POST':

        if request.form['action'] == 'Set':
            description = request.form['description']
            teacherinfo['description'] = description
            data[subject]['teachers'] = teachers
            save_data(data, current_user.stage)

            return redirect(
                url_for('views.manage_courses',
                        subject=subject,
                        teachername=teachername))

        if request.form['action'] == 'Add':
            course_name = request.form['new']
            file = request.files['file']

            if file:
                os.makedirs(os.path.dirname(
                    f'website/static/assets/Stage{current_user.stage}/{subject}/{teachername}/'
                    + course_name + '.jpg'),
                            exist_ok=True)

                file.save(
                    f'website/static/assets/Stage{current_user.stage}/{subject}/{teachername}/'
                    + course_name + '.jpg')

            else:
                return "Choose an imgae for the course"

            if course_name == "":
                return "Course name is none "
            new_course = {
                "name": course_name,
                "description": "",
                "videos": "",
                "playlist_id": "",
                "folder": ""
            }
            teacher_courses.append(new_course)  
            data[subject]['teachers'] = teachers
            save_data(data, current_user.stage)
            return redirect(
                url_for('views.manage_courses',
                        subject=subject,
                        teachername=teachername))

        if request.form['action'] == 'Remove':

            course_name = request.form['remove']
            file_path = f'website/static/assets/Stage{current_user.stage}/{subject}/{teachername}/' + course_name + '.jpg'  

            if os.path.exists(file_path):
                os.remove(file_path)

            teacher = next((t for t in teachers if t['link'] == teachername),
                           None)

            if course_name == "":
                return "Course name is none "
            teacher_courses = [
                course for course in teacher_courses  
                if course['name'] != course_name
            ]

            teacher['courses'] = teacher_courses  
            data[subject]['teachers'] = teachers

            save_data(data, current_user.stage)

            return redirect(
                url_for('views.manage_courses',
                        subject=subject,
                        teachername=teachername))

    return render_template('data/courses.html',
                           data=course_names,
                           teachername=teachername,
                           desc=teacherinfo['description'])


#Edit a course info
@views.route('/subjects/<subject>/<teachername>/<course_name>/edit',
             methods=['POST', 'GET'])
def edit_course(subject, teachername, course_name):
    if current_user.type != 'admin':
        return "User is not an admin"
    data = load_stage_data(current_user.stage)
    current_course = None
    if "-" in course_name:
        course_name = course_name.replace('-', ' ')
    if request.method == 'POST':
        for teacher in data.get(subject, {}).get('teachers', []):
            if teacher['link'] == teachername:
                for course in teacher['courses']:
                    if course['name'] == course_name:
                        if request.form['action'] == 'apply':
                            
                            course['playlist_id'] = request.form['playlist'].split('?list=')[1]
                            
                        elif request.form['action'] == 'Apply':
                            course['folder'] = request.form['folder']
                        elif request.form['action'] == 'set':
                            course['description'] = request.form['description']
                        elif request.form['action'] == 'Clear videos':
                            course['videos'] = ""
                        save_data(data, current_user.stage)
                        course_name = course_name.replace(' ', '-')
                        return redirect(
                            url_for('views.edit_course',
                                    subject=subject,
                                    teachername=teachername,
                                    course_name=course_name))

    # Find the current course to display its details
    for teacher in data.get(subject, {}).get('teachers', []):
        if teacher['link'] == teachername:
            for course in teacher['courses']:
                if course['name'] == course_name:
                    current_course = course
                    break

    return render_template('data/course.html',
                           course_name=course_name,
                           teachername=teachername,
                           current_course=current_course)

#Vdocipher Api access--------------------------------------------------------------------------
import hmac
import hashlib
SECRET_KEY = b'sssss'  # Should be securely generated and consistent



def discord_log_vdocipher(message):
    messageeeee = {'content': message}
    payload = json.dumps(messageeeee)
    headers = {'Content-Type': 'application/json'}
    requests.post(
        "https://discord.com/api/webhooks/1280568380209889361/2Cmrouxw53pijJ9VwPw4tp73ByeQMiQwIN7QrMlnyLvwphrWUl-WSJ2vKvxeFESK-caD",
        data=payload,
        headers=headers)



def generate_signature(message, secret_key):
    return hmac.new(secret_key, message.encode(), hashlib.sha256).hexdigest()



@views.route('/vdocipher-api', methods=['POST'])
def secure_endpoint():

    client_ip = request.headers.get('X-Forwarded-For')

    if client_ip:
        client_ip = client_ip.split(',')[0].strip()
    else:
        client_ip = request.headers.get('CF-Connecting-IP',
                                        request.remote_addr)
        
    data = request.json
    username = data.get('username')
    command = data.get('command')



    if command: 
        discord_log_vdocipher(f"{command}")


    if username not in ['stofalleno01' , 'spyy'] :

        return jsonify({"status": "Wrong api key"}), 400
    
    if not username:

        return jsonify({"status": "missing message"}), 400

    response_data = {"status": "true", "message": username}
    # Serialize the data consistently
    data_string = json.dumps(response_data, sort_keys=True)
    response_signature = generate_signature(data_string, SECRET_KEY)

    discord_log_vdocipher(f"Vdocipher Script opened by {username} -- {client_ip}")

    return jsonify({"data": response_data, "signature": response_signature}), 200