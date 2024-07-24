from flask import Blueprint, render_template, request, redirect, url_for, render_template_string, send_file, current_app

from googleapiclient.discovery import build
import os
import ast
import json
import requests
from flask import session
from flask import jsonify  #type: ignore
from flask_login import login_user, current_user, logout_user
from .models import User, db
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build  #type: ignore
import random
from flask_mail import Message
from . import mail
from google.auth.exceptions import GoogleAuthError
from datetime import datetime

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
    discord_log_backend(
        f"Using youtube api to fetch : <https://www.youtube.com/playlist?list={playlist_id}> <@709799648143081483>"  #type: ignore
    )

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
        "https://discord.com/api/webhooks/1223859771401179146/Qaxf4CVfRhTn7oQ2lbz1MdJQZ441_-VruTkP8tir3JabeFbMkLR9aJpDANDwFSYcEDfJ",
        data=payload,
        headers=headers)


#Uptime robot
@views.route('/monitor')
def monitor():
    return "Working"


#Login route (whitelist_ips is from EG)

blacklist_ips = set()
whitelist_ips = set()


@views.route('/login', methods=['GET', 'POST'])
def login():
    client_ip = request.headers.get('X-Forwarded-For')

    if client_ip:
        client_ip = client_ip.split(',')[0].strip()
    else:
        client_ip = request.headers.get('CF-Connecting-IP',
                                        request.remote_addr)

    user_agent = request.headers.get('User-Agent')

    # if current_user.is_authenticated:
    #     return redirect(url_for('views.home'))
    # if client_ip in blacklist_ips:
    #     return jsonify(message=f"Error 403 your ip is {client_ip}"), 403

    # if client_ip not in whitelist_ips:
    #     api_url = f'https://ipinfo.io/{client_ip}?token=8f8d5a48b50694'
    #     response = requests.get(api_url)
    #     data = response.json()

    #     if 'country' in data:
    #         country_code = data['country']
    #         if country_code != 'EG':
    #             blacklist_ips.add(client_ip)
    #             return jsonify(message="Please disable vpn/proxy."), 403
    #     else:
    #         blacklist_ips.add(client_ip)
    #         return jsonify(
    #             message="Unable to determine the country. Login failed."), 403

    # whitelist_ips.add(client_ip)

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        username = username.replace(" ", "")
        username = username.lower()
        user = User.query.filter_by(username=username).first()

        if user:

            if user.username not in [
                    'spy'
            ] and user.active_sessions >= 3:  #If he logged on more than 3 or 3 devices excpet []
                discord_log_login(
                    f"{username} tried to login from more than 3 devices <@709799648143081483>"
                )
                return redirect(f"/login?maxdevices=yes&user={username}")

            if password == user.password:
                login_user(user)
                if user.username != 'spy':
                    user.active_sessions += 1
                db.session.commit()
                discord_log_login(
                    f"{client_ip} just logged in with {username} Device ```{user_agent}```  <@709799648143081483>"
                )
                session.permanent = True
                return redirect(url_for('views.home'))

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
    current_user.active_sessions -= 1
    db.session.commit()
    discord_log_login(
        f"<@709799648143081483> {current_user.username} Logged out ")

    logout_user()
    return redirect(url_for('views.login'))


#Re do it
@views.route('/verify', methods=['GET', 'POST'])
def verifyemail():
    if current_user.is_authenticated:
        return redirect(url_for('views.home'))

    client_ip = request.headers['X-Forwarded-For'].split(',')[0].strip()
    user_agent = request.headers.get('User-Agent')
    username = request.args.get('user')
    msgg = request.args.get('msg')

    user = User.query.filter_by(username=username).first()

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
            if user.username not in ['spy', 'biba'
                                     ] and user.active_sessions >= 3:
                discord_log_login(
                    f"{username} tried to login from more than 3 devices <@709799648143081483>"
                )
                return redirect(f"/login?maxdevices=true&user={username}")

            login_user(user)
            if user.username != 'spy':
                user.active_sessions += 1
            user.otp = "null"
            db.session.commit()
            discord_log_login(
                f"{client_ip} just logged in with {username} Device ```{user_agent}```  <@709799648143081483>"
            )
            session.permanent = True
            return redirect('/')
        else:
            return redirect(f'/verify?msg=failedtologin&user={username}')
    return render_template('users_pages/verify.html',
                           email=user.email,
                           msg=msgg)


def read_html_file(file_path, **kwargs):
    with open(file_path, 'r') as file:
        template = file.read()
    return render_template_string(template, **kwargs)


#Re do it
@views.route('/register', methods=['GET', 'POST'])
def registeracc():
    client_ip = request.headers['X-Forwarded-For'].split(',')[0].strip()
    user_agent = request.headers.get('User-Agent')
    if current_user.is_authenticated:
        return redirect(url_for('views.home'))

    if request.method == 'POST':
        username = request.form.get('username')
        user = User.query.filter_by(username=username).first()
        if user:
            return "Username taken"
        email = request.form.get('email')
        phone = request.form.get('phone')
        if email is None:
            return 'Email is null'
        if phone is None:
            return 'Phone is null'
        if '@' not in email:
            return 'Invalid email'
        if '0' not in phone:
            return 'Invalid phone number'
        discord_log_register(
            f"New user  : {username} ====== {email} ====== {phone} ====== {client_ip} {user_agent} <@709799648143081483>"
        )
        return redirect(f"/send_email?to={email}")
    return render_template('users_pages/register.html',
                           done=request.args.get("done"))


#Dont edit
@views.route('/redirect/<path:link>')
def redirectlinks(link):
    link = link.replace('questionmark', '?')
    link = link.replace('andsympol', '&').replace(':', ':/')  #For iphone

    return redirect(f"{link}")


@views.route('/favicon.ico')
def favicon():
    return redirect("/static/favicon.ico")


@views.route('/robots.txt')
def robots_txt():

    return send_file('robots.txt', mimetype='otp/plain')


#Home
@views.route("/")
def home():
    with open('website/Backend/data.json') as f:
        data = json.load(f)
    lines = list(data.keys())
    return render_template('used_pages/all.html',
                           lines=lines,
                           teachername="All")


#Subjects
@views.route("/subjects/<subject>")
def subjects(subject):
    with open('website/Backend/data.json') as f:
        data = json.load(f)
    if subject in data:

        teachers = [{
            "name":
            teacher["name"],
            "link":
            teacher["link"],
            "description":
            teacher.get("description", "")
            or f"{len(teacher['courses'])} courses"
        } for teacher in data[subject]["teachers"]]

    else:
        return "404"

    return render_template('used_pages/subjects.html',
                           teachername=subject,
                           teacher_links=teachers)


#Teacher
@views.route("/subjects/<subject>/teacher/<teacher_name>")
def teacher(subject, teacher_name):

    with open('website/Backend/data.json') as f:
        data = json.load(f)
    if subject in data:
        for teacher in data[subject]["teachers"]:
            if teacher["link"] == teacher_name:
                courses = teacher.get("courses")
                for item in courses:
                    item['link'] = item['name']
                break
            else:
                return "404"
    else:
        return "404"
    return render_template('used_pages/teacher.html',
                           teachername=subject,
                           teacher_links=courses,
                           teacher_name=teacher_name)


#Videos
@views.route("/subjects/<subject>/teacher/<teacher_name>/course/<course_name>")
def videos(subject, teacher_name, course_name):

    with open('website/Backend/data.json') as f:
        data = json.load(f)
    if subject in data:
        for teacher in data[subject]["teachers"]:
            if teacher.get("link") == teacher_name:
                # Find the specific course
                for course in teacher.get("courses", []):
                    if course.get("name") == course_name:
                        # Return the course videos and playlist_id
                        videos = course.get('videos', '')
                        playlist_id = course.get('playlist_id', '')
                        folder = course.get('folder', '')
                    else:
                        return "404"    
            else:
                return "404"            

    else:
        return "404"

    teachername = course_name

    return render_template('used_pages/videopage.html',
                           videos=videos,
                           playlist_id=playlist_id,
                           teachername=teachername,
                           folder=folder)


#get_playlist_videos(playlist id)
@views.route("/subjects/<subject>/teacher/<teacher_name>/course/<course_name>/update")
def update(subject, teacher_name, course_name):

    with open('website/Backend/data.json') as f:
        data = json.load(f)
    if subject in data:
        for teacher in data[subject]["teachers"]:
            if teacher.get("link") == teacher_name:
                # Find the specific course
                for course in teacher.get("courses", []):
                    if course.get("name") == course_name:
                        playlist_id = course.get('playlist_id', '')
                        videos = get_playlist_videos(playlist_id)
                        course['videos'] = videos
                        with open('website/Backend/data.json', 'w') as f:
                            json.dump(data, f, indent=4)
                    else:
                        return "404"        
            else:
               return "404"
    else:
        return "404"
    return videos




#Admin pages 
#Manage users laterrrrrrrrrrrr
#Add/remove subjects Done
#Add/remove teacher in each subject
#Add/remove couse in each teacher 
#Edit the course (Playlist_id , folder)

def load_data():
    with open('website/Backend/data.json', 'r') as file:
        return json.load(file)

def save_data(data):
    timestamp = datetime.now().strftime("%m.%d_%H.%M")
    backup_filename = f"website/Backend/dumps/{timestamp}.json"
    os.makedirs(os.path.dirname(backup_filename), exist_ok=True)
    
    # Backup the current data.json
    with open('website/Backend/data.json', 'r') as file:
        current_data = file.read()
    with open(backup_filename, 'w') as backup_file:
        backup_file.write(current_data)
    
    # Save the new data
    with open('website/Backend/data.json', 'w') as file:
        json.dump(data, file, indent=4)


@views.route('/edit_subjects' , methods=['POST' , 'GET'])
def manage_subjects():
    data = load_data()
    if request.method == 'POST':
        if request.form['action'] == 'Add':
            subject = request.form['newSubject']

            if subject not in data:
                data[subject] = {"teachers": []}
                save_data(data)
                return redirect(url_for('views.manage_subjects'))

            else:
                return jsonify({"message": f"Subject '{subject}' already exists!"}), 400

        if request.form['action'] == 'Remove':
            subject = request.form['removeSubject']
             
            if subject in data:
                del data[subject]
                save_data(data)
                return redirect(url_for('views.manage_subjects'))
            else:
                return jsonify({"message": f"Subject '{subject}' does not exist!"}), 400

    return render_template('data/subjects.html' , data = list(data.keys()))




@views.route('/<subject>/edit' , methods=['POST' , 'GET'])
def manage_teachers(subject):
    data = load_data()
    teachers= data[subject].get('teachers', [])
    teacher_names = [teacher['name'] for teacher in teachers]
    if request.method == 'POST':
        if request.form['action'] == 'Add':
            teacher_name = request.form['new']
            if subject in data:
                new_teacher = {
                    "name": teacher_name,
                    "link": teacher_name,
                    "courses": []
                }
                data[subject]['teachers'].append(new_teacher)
                save_data(data)
                return redirect(url_for('views.manage_teachers', subject=subject))

            else:
                return jsonify({"message": f"Subject '{subject}' does not exist!"}), 400
  

        if request.form['action'] == 'Remove':
            teacher_name = request.form['remove']
             
            if subject in data:
                if 'teachers' in data[subject]:
                    teacher_exists = any(teacher['name'] == teacher_name for teacher in data[subject]['teachers'])
                    if teacher_exists:
                        data[subject]['teachers'] = [teacher for teacher in data[subject]['teachers'] if teacher['name'] != teacher_name]
                        save_data(data)
                        return redirect(url_for('views.manage_teachers', subject=subject))
                    else:
                        return jsonify({"message": f"Teacher '{teacher_name}' does not exist in subject '{subject}'!"}), 400

            else:
                return jsonify({"message": f"Subject '{subject}' does not exist!"}), 400

    return render_template('data/teachers.html' , data = teacher_names , subject = subject)



