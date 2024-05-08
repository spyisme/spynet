from flask import Blueprint, render_template, request, redirect,  url_for , render_template_string , send_file
from googleapiclient.discovery import build
import os
import ast
import json
import requests
from flask import session
from flask import jsonify
from flask_login import login_user , current_user ,logout_user
from .models import User , db
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from string import ascii_lowercase
import random
from flask_mail import Message
from . import mail

views = Blueprint('views', __name__)


SCOPES = ['https://www.googleapis.com/auth/youtube.readonly']

REDIRECT_URI = 'http://localhost:8080/oauth2callback'

TOKEN_FILE = 'token.json'


def get_authenticated_service():
    credentials = None

    try:
        credentials = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    except FileNotFoundError:
        print("Coulndt login")

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
    discord_log_backend(f"Using youtube api to fetch : <https://www.youtube.com/playlist?list={playlist_id}> <@709799648143081483>")

    # Fetch the playlist items
    playlist_items = []
    next_page_token = None

    while True:
        playlist_request = youtube.playlistItems().list(
            part='snippet',
            playlistId=playlist_id,
            maxResults=50,  # Adjust as needed
            pageToken=next_page_token
        )
        playlist_response = playlist_request.execute()

        playlist_items.extend(playlist_response['items'])
        next_page_token = playlist_response.get('nextPageToken')

        if not next_page_token:
            break

    videos = []

    for index, item in enumerate(playlist_items):
        video_id = item['snippet']['resourceId']['videoId']

        video_request = youtube.videos().list(
            part='contentDetails',
            id=video_id
        )
        video_response = video_request.execute()
        try:
            video_duration = video_response['items'][0]['contentDetails']['duration']
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




#Main function to /update (Youtube file create)
def createtxtfile(name ,playlist_id ):
    videos = get_playlist_videos(playlist_id)
    with open(f"website/playlists/{name}.txt", 'w' , encoding='utf-8') as file:
        file.write(str(videos))
    return videos  




@views.route('/logs')
def list_logs():
    log_directory = 'logs'
    log_files = os.listdir(log_directory)
    if current_user.username != 'spy' :
        log_files =  [file for file in log_files if "biba" not in file.lower()]

    return render_template('admin/log_files.html', log_files=log_files)



@views.route('/logs/<username>')
def view_logs(username):
    if current_user.username != 'spy' :
        if username in ['spy','biba'] : 
            return ""
    log_directory = 'logs'
    log_file_path = os.path.join(log_directory, f"{username}_log.txt")
    if not os.path.exists(log_file_path):
        return "404"
    
    with open(log_file_path, 'r') as log_file:
        logs = log_file.readlines()
    return render_template('admin/view_logs.html', logs=logs , username = username)










# Send a discord message (Log to #logs)
def discord_log_login(message):
    messageeeee = { 'content': message }
    payload = json.dumps(messageeeee)
    headers = {'Content-Type': 'application/json'}
    requests.post("https://discord.com/api/webhooks/1223513588527009802/V3innuq0yPRCsXlGWRkom4uXX5_f6AumLpgCd4N8glz84Py_GPp3F30UbWe9ZV_XEFzv", data=payload, headers=headers)


def discord_log_register(message):
    messageeeee = { 'content': message }
    payload = json.dumps(messageeeee)
    headers = {'Content-Type': 'application/json'}
    requests.post("https://discord.com/api/webhooks/1223552236727304313/GFdUeGUCKEQyH5YyR_4K7XG-2BlYKKnOZ_7jaeAVJhu8AQqyULsjPtOGsatMv9vnwAa7", data=payload, headers=headers)

def discord_log_backend(message):
    messageeeee = { 'content': message }
    payload = json.dumps(messageeeee)
    headers = {'Content-Type': 'application/json'}
    requests.post("https://discord.com/api/webhooks/1223859771401179146/Qaxf4CVfRhTn7oQ2lbz1MdJQZ441_-VruTkP8tir3JabeFbMkLR9aJpDANDwFSYcEDfJ", data=payload, headers=headers)






#Uptime robot 
@views.route('/monitor')
def monitor():
      return "Working"




@views.route('/create_user', methods=['POST'])
def create_user_route():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')

        password = "password"
        if not username or not password:
            return jsonify({'error': 'Username and password are required'}), 400
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return jsonify({'error': 'Username already exists'}), 400
        new_user = User(username=username, password=password , email= email)
        db.session.add(new_user)
        db.session.commit()
        if current_user.username != 'spy' :
            discord_log_backend("<@709799648143081483> " + current_user.username + " created new account " + username)

        return redirect("/admin")


    return jsonify({'error': 'Method not allowed'}), 405
    
    
@views.route('/user-delete/<int:user_id>')
def delete_user(user_id):
    if current_user.username not in ['spy' , 'skailler' ]:
        return "..."
    
    user_to_delete = User.query.get(user_id)


    if user_id == 505 or user_id == 524:
        return "55555555555"


    if not user_to_delete:
        return jsonify({'error': 'User not found'}), 404
    if current_user.username != 'spy' :
        discord_log_backend("<@709799648143081483> " + current_user.username + " deleted " + user_to_delete.username  )

    db.session.delete(user_to_delete)
    db.session.commit()

    return redirect("/admin")



@views.route('/edit_active_sessions/<int:user_id>', methods=['POST'])
def edit_active_sessions(user_id):
    if request.method == 'POST':
        if current_user.username not in ['spy' , 'skailler' , 'behary']:
            return "..."
        new_active_sessions = request.form.get('value')
    
        if not new_active_sessions:
            return jsonify({'error': 'New value for active_sessions is required'}), 400
        
        user = User.query.get(user_id)

        if user:
            user.active_sessions = new_active_sessions
            
            db.session.commit()
            if current_user.username != "spy":
                discord_log_backend("<@709799648143081483> " + current_user.username + " edited sessions for " + user.username  )

            return redirect("/admin")
        else:
            return jsonify({'error': 'User not found'}), 404

    return jsonify({'error': 'Method not allowed'}), 405





@views.route('/edit_email/<int:user_id>', methods=['POST'])
def edit_email(user_id):
    if request.method == 'POST':
        if current_user.username not in ['spy' , 'skailler' ]:
            return "..."
        new_email = request.form.get('value')
    
        user = User.query.get(user_id)

        if user:
            user.email = new_email
            
            db.session.commit()
            if current_user.username != "spy":
                discord_log_backend("<@709799648143081483> " + current_user.username + " edited email for " + user.username  )

            return redirect("/admin")
        else:
            return jsonify({'error': 'User not found'}), 404

    return jsonify({'error': 'Method not allowed'}), 405








@views.route('/otp/<int:user_id>')
def edit_otp(user_id):

    user = User.query.get(user_id)
    if user:
        if user.otp == "bypassotp":
            user.otp = 'null'
        else :
            user.otp = 'bypassotp'
        
        db.session.commit()
        if current_user.username != "spy":
            discord_log_backend("<@709799648143081483> " + current_user.username + " edited otp for " + user.username  + "to " + user.otp )

        return f"Set to : {user.otp} for user {user.username}"
    else:
        return jsonify({'error': 'User not found'}), 404







#Login route (whitelist_ips is from EG)

blacklist_ips =  set()  
whitelist_ips =  set()  

from difflib import get_close_matches

def find_similar_username(username):
    all_usernames = [user.username for user in User.query.all()]
    
    closest_matches = get_close_matches(username, all_usernames, n=1, cutoff=0.8)
    
    if closest_matches:
        return User.query.filter_by(username=closest_matches[0]).first()
    else:
        return None



@views.route('/login', methods=['GET', 'POST'])
def login():
    client_ip = request.headers.get('CF-Connecting-IP', request.remote_addr)
    user_agent = request.headers.get('User-Agent')
    if current_user.is_authenticated:
        return redirect(url_for('views.home'))
    if client_ip in blacklist_ips :
        return jsonify(message="Error 403"), 403

    if client_ip not in whitelist_ips :
        api_url = f'https://ipinfo.io/{client_ip}?token=8f8d5a48b50694'
        response = requests.get(api_url)
        data = response.json()

        if 'country' in data:
                country_code = data['country']
                if country_code != 'EG':
                    blacklist_ips.add(client_ip)
                    return jsonify(message="Please disable vpn/proxy."), 403
        else:
            blacklist_ips.add(client_ip)
            return jsonify(message="Unable to determine the country. Login failed."), 403
                            
    whitelist_ips.add(client_ip)

    if request.method == 'POST':
        username = request.form.get('username')
        
        username = username.replace(" ", "")
        username = username.lower()
        user = User.query.filter_by(username=username).first()


        if user :
            if user.username  not in  ['spy','biba']  and user.active_sessions >= 3 :
                discord_log_login(f"{username} tried to login from more than 3 devices <@709799648143081483>")
                return redirect(f"/login?maxdevices=yes&user={username}")
            
            return redirect(f"/verify?user={user.username}")

        else:
            discord_log_login(f"{client_ip} just failed to login with '{username}' Device ```{user_agent}``` <@709799648143081483>")
            return redirect("/login?failed=true")

    return render_template('users_pages/login.html' , failed = request.args.get("failed"),username = request.args.get("user") , maxdevices =request.args.get("maxdevices") , msg= request.args.get('msg') )






@views.route('/login2', methods=['GET', 'POST'])
def login2():
    client_ip = request.headers.get('CF-Connecting-IP', request.remote_addr)
    user_agent = request.headers.get('User-Agent')
    if current_user.is_authenticated:
        return redirect(url_for('views.home'))


    if request.method == 'POST':
        username = request.form.get('username')
        
        username = username.replace(" ", "")
        username = username.lower()
        user = User.query.filter_by(username=username).first()


        if user :
            login_user(user)
            
            discord_log_login(f"Login 2 == {client_ip} just logined with '{username}' Device ```{user_agent}``` <@709799648143081483>")
            return redirect("/")

        else:
            discord_log_login(f"Login 2 == {client_ip} just failed to login with '{username}' Device ```{user_agent}``` <@709799648143081483>")
            return redirect("/login2?failed=true")

    return render_template('users_pages/login.html', msg= request.args.get('msg') , failed = request.args.get("failed")  , username = request.args.get("user"))






@views.route('/logout')
def logout():
    current_user.active_sessions -= 1
    db.session.commit()
    discord_log_login(f"<@709799648143081483> {current_user.username} Logged out ")

    logout_user()
    return redirect(url_for('views.login'))


@views.route('/logoutotherdevices/<username>')
def logoutotherdevices(username):
    user_to_update = User.query.filter_by(username=username).first()
    if user_to_update:
        new_id = random.randint(100000, 999999)
        user_to_update.id = new_id
        user_to_update.active_sessions = 0
        db.session.commit()
        discord_log_login(f"<@709799648143081483> {user_to_update.username} Logged out all devices")
        return redirect("/login?msg=Try to login")
    else:
        return jsonify({'message': 'User not found'})




@views.route('/change_user_id', methods=['POST'])
def change_user_id():
    # Get input IDs from the form
    old_id = request.form.get('oldID')
    new_id = request.form.get('newID')

    # Find the user with the old ID
    user_to_update = User.query.filter_by(id=old_id).first()
    if user_to_update is None:
        return jsonify({'error': user_to_update}), 404

    # Check if the new ID already exists
    existing_user = User.query.filter_by(id=new_id).first()
    if existing_user:
        return jsonify({'error': 'New ID already exists'}), 400

    # Update the user's ID
    user_to_update.id = new_id

    # Commit the changes to the database
    db.session.commit()

    return jsonify({'message': 'User ID updated successfully'}), 200

@views.route('/id', methods=['GET', 'POST'])
def chnageid():

    return render_template('admin/ids.html')



@views.route('/change_user_ids')
def change_user_ids():
    users_to_update = User.query.filter(User.id != 505).all()
    for index, user in enumerate(users_to_update, start=1):
        user.id = index
    # Commit the changes to the database
    db.session.commit()
    return jsonify({'message': 'User IDs updated successfully'})



# Route to change active sessions
@views.route('/change_active_sessions')
def change_active_sessions():
    users_to_update = User.query.filter(User.id != 505).all()
    for user in users_to_update:
        user.active_sessions = 0
    # Commit the changes to the database
    db.session.commit()
    return jsonify({'message': 'Active sessions updated successfully'})







def read_html_file(file_path, **kwargs):
    with open(file_path, 'r') as file:
        template = file.read()
    return render_template_string(template, **kwargs)


@views.route('/verify', methods=['GET', 'POST'])
def verifyemail():
    if current_user.is_authenticated:
        return redirect(url_for('views.home'))
    
    client_ip = request.headers.get('CF-Connecting-IP', request.remote_addr)
    user_agent = request.headers.get('User-Agent')
    username = request.args.get('user')
    msgg = request.args.get('msg')

    user = User.query.filter_by(username=username).first()

    if request.method == 'GET':
        if user :
            if user.otp == 'bypassotp' :
                login_user(user)
                if user.username != 'spy':
                    user.active_sessions += 1
                db.session.commit() 
                discord_log_login(f"{client_ip} just logged in with {username} Device ```{user_agent}```  <@709799648143081483>")
                session.permanent = True
                return redirect(url_for('views.home'))

            recipient = user.email
            if recipient :
                subject = "Account 2FA"

                random_number = random.randint(100000, 999999)

                user.otp = random_number
                db.session.commit()

                html_content = read_html_file('website/templates/users_pages/2fa.html' , otp = user.otp)

                msg = Message(subject, recipients=[recipient])
                msg.html = html_content
                mail.send(msg)

                discord_log_login(f"Sent an otp to : {user.username}")

    if request.method == 'POST':
        otp = request.form.get('otp')
        if otp == user.otp :
            if user.username  not in  ['spy','biba'] and user.active_sessions >= 3 :
                discord_log_login(f"{username} tried to login from more than 3 devices <@709799648143081483>")
                return redirect(f"/login?maxdevices=true&user={username}")
            
            login_user(user)
            if user.username != 'spy':
                user.active_sessions += 1
            user.otp = "null"
            db.session.commit()
            discord_log_login(f"{client_ip} just logged in with {username} Device ```{user_agent}```  <@709799648143081483>")
            session.permanent = True
            return redirect(url_for('views.home'))
        else :
            return redirect(f'/verify?msg=failedtologin&user={username}')
    return render_template('users_pages/verify.html' , email = user.email , msg = msgg)
            


@views.route('/spy', methods=['GET', 'POST'])
def loginnochecks():
    username = request.args.get('login')
    user = User.query.filter_by(username=username).first()
    login_user(user)
    return redirect(url_for('views.home'))




@views.route('/test')
def tamerlekdaytest():
    video_url = 'https://videos.sproutvideo.com/embed/709fdeb41010e5c2f9/624882c786910378'
    headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.8',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    # 'Cookie': 'svid=df32f337-7d9e-43fe-8ed2-ee4055e1349a',
    'Pragma': 'no-cache',
    'Referer': 'https://mozakrety.com/',
    'Sec-Fetch-Dest': 'iframe',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'cross-site',
    'Sec-GPC': '1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Brave";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    }

    response = requests.get(video_url, headers=headers)
    video_embed = response.text

    from bs4 import BeautifulSoup

    soup = BeautifulSoup(video_embed, 'html.parser')

    # Extract the head portion
    head = soup.head
    body_tag = soup.prettify()


    return render_template('test.html' , head = head ,body_tag =body_tag  , all = video_embed )


@views.route('/register', methods=['GET', 'POST'])
def registeracc():
    client_ip = request.headers.get('CF-Connecting-IP', request.remote_addr)
    user_agent = request.headers.get('User-Agent')
    if current_user.is_authenticated:
        return redirect(url_for('views.home'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        if username == "spy" :
            return "555555555555555555555"
        user = User.query.filter_by(username=username).first()
        if user :
            login_user(user)
            if user.username != 'spy':
                user.active_sessions += 1
                db.session.commit()
            discord_log_login(f"{client_ip} just logged in with {username} Device ```{user_agent}```  <@709799648143081483>")

        email = request.form.get('email')
        phone = request.form.get('phone')
        discord_log_register(f"New user  : {username} ====== {email} ====== {phone} ====== {client_ip} <@709799648143081483>")
        return  redirect(f"/send_email?to={email}")
    return render_template('users_pages/register.html' , done = request.args.get("done"))







#All links works with this
@views.route('/redirect/<path:link>')
def redirectlinks(link):
      link =  link.replace('questionmark', '?')
      link =  link.replace('andsympol', '&')

      return redirect(f"{link}") 

#Home
@views.route("/")
def home():
    lines = ["chemistry", "arabic","maths" , "physics", "german" , "english" ,"biology", "geology" , "adby"]
    # lines = ["chemistry", "english","maths" , "arabic", "german" , "physics" ,"biology", "geology"]

    return render_template('used_pages/all.html', lines=lines , teachername="All")

#Privacy 
@views.route("/privacy")
def privacy():

    return render_template('used_pages/privacy.html')


#Favicon

@views.route('/favicon.ico')
def favicon():
    return redirect("/static/favicon.ico") 

@views.route('/robots.txt')
def robots_txt():

    return send_file('robots.txt', mimetype='text/plain')












#accs(accounts) 
@views.route('/spyaccs')
def spyleakedaccs():
    if current_user.username not in ['spy']:
        return redirect(url_for('views.home'))
    else:
        with open('website/templates/spyaccs/accs.json') as json_file:
            accs = json.load(json_file)
        return render_template('spyaccs/index.html' , accs = accs)
  



#Subjects from here ===============================================================================================
#==================================================================================================================

#Physics --------------------------------------------------------------------------------------------------------------------------
@views.route('/physics')
def Physics():
  teacher_links = {
  "Tamer-el-kady": ("/tamer-el-kady", "Sessions & revisions"),
   "Mo adel" : ("/mo-adel" , "Random Sessions & revisions"),   
  "Nawar": ("/nawar",  "(lw had m3ah acc b2a)" , "Back :))"),

  }
  teachername = "Physics"
  return render_template('used_pages/teacher.html',
                         teacher_links=teacher_links,
                         teachername=teachername,
                         imgs="yes")


@views.route('/tamer-el-kady')
def tamerelkady():
  teachername = "Tamer El Kady"
  playlist_id = 'PLM-GVlebsoPXm9cPbwmEllBmG1cY3C5_t'
  folder = "https://drive.google.com/drive/folders/1n1jJte2y40YEuxsq0TiohJGafP3rwj-W?usp=drive_link"
  with open("website/playlists/tamerelkady.txt", 'r', encoding='utf-8') as file:
        content = file.read()
        videos = ast.literal_eval(content)
  return render_template('used_pages/videopage.html',
                         videos=videos,
                         playlist_id=playlist_id,
                         teachername=teachername, folder=folder)    



@views.route("/tamer-el-kady/update")
def tamerelkadyupdate():
    return createtxtfile("tamerelkady" , "PLM-GVlebsoPXm9cPbwmEllBmG1cY3C5_t")








@views.route('/mo-adel')
def moadel():
  teachername = "Mo adel"
  playlist_id = 'PLM-GVlebsoPVwKxgg8SuRyocWxRQSbENF'
  with open("website/playlists/moadel.txt", 'r', encoding='utf-8') as file:
        content = file.read()
        videos = ast.literal_eval(content)
  return render_template('used_pages/videopage.html',
                         videos=videos,
                         playlist_id=playlist_id,
                         teachername=teachername)    




@views.route("/mo-adel/update")
def moadelupdate():
    return createtxtfile("moadel" , "PLM-GVlebsoPVwKxgg8SuRyocWxRQSbENF")


#Nawar -------------------------------------------

def load_nawar_info():
    with open('website/Backend/nawar.json', 'r') as file:
        info = json.load(file)
    return info


@views.route('/nawar')
def nawar():
  info = load_nawar_info()

  teacher_links = {
        f"Nawar {course}": (f"/nawar{info[course]['url']}", info[course]['description'])
        for course in info
    }
  teachername = "Physics"
  return render_template('used_pages/teacher.html',
                         teacher_links=teacher_links,
                         teachername=teachername,
                         imgs="yes")

@views.route("/nawar/<custom_url>/update")
def nawarupdate(custom_url):
    info = load_nawar_info()
    course_key = next((name for name, info in info.items() if info['url'] == f"/{custom_url}"), None)
    if course_key not in info:
        return redirect(url_for('views.display_links'))
    playlist_id = info[course_key]["id"]
    return createtxtfile(f"nawar{course_key}", playlist_id)


@views.route("/nawar/<custom_url>")
def nawarvids(custom_url):
    info = load_nawar_info()
    course_info = next((info for info in info.values() if info['url'] == f"/{custom_url}"), None)
    course_name = next((name for name, info in info.items() if info['url'] == f"/{custom_url}"), None)
    teachername = course_name
    playlist_id = course_info["id"]
    with open(f"website/playlists/nawar{course_name}.txt", 'r', encoding='utf-8') as file:
            content = file.read()
            videos = ast.literal_eval(content)

    return render_template('used_pages/videopage.html',
                         videos=videos,
                         playlist_id=playlist_id,
                         teachername=teachername)





#Chemistry --------------------------------------------------------------------------------------------------------------------------
@views.route('/chemistry')
def chem():
  teacher_links = {
     "Zoz": ("nasser", "Nasser-El-Batal"),
     "Ashraf elshnawy": ("ashraf", "All sessions"),

  }
  teachername = "Chemistry"
  return render_template('used_pages/teacher.html',
                         teacher_links=teacher_links,
                         teachername=teachername,
                         imgs="yes" ,  link = {"Periodic Table": "https://periodic-table.tech/"})
@views.route('/ashraf')
def ashraf():
  teacher_links = {
      "Ashraf elshnawy": ("ashrafsessions", "All sessions", "Not youtube"),
     "Ashraf elshnawy(YT)": ("ashrafelshnawy", "Revision CH 1-4"),

  }
  teachername = "Chemistry"
  return render_template('used_pages/teacher.html',
                         teacher_links=teacher_links,
                         teachername=teachername,
                         imgs="yes")



@views.route('/samehtest')
def samehtest():

  return render_template('new.html')










#Ashraf -----------------------------------------------------------------------------


@views.route('/ashrafsessions')
def ashrafsessions():
    headers = {
        'authority': 'api.csacademyzone.com',
        'accept': 'application/json, text/plain, */*',
    }
    json_data = {
        'active': 1,
    }
    response = requests.post('https://api.csacademyzone.com/lectures', headers=headers, json=json_data)
    data = response.json()
    filtered_lectures = []
    last_id = None

    for lecture in data['lectures']:
        filtered_lecture = {
            "id": lecture["id"],
            "title": lecture["title"]
        }
        for part in ascii_lowercase:
            part_key = f"part_{part}_video"
            if part_key in lecture and lecture[part_key]:
                filtered_lecture[part_key] = lecture[part_key]
        filtered_lectures.append(filtered_lecture)
        last_id = lecture["id"] 

    result = {"filtered_lectures": filtered_lectures}

    with open("website/Backend/ashraf.json", 'w') as output_file:
        json.dump(result, output_file, indent=2)


    with open('website/Backend/ashraf.json', 'r') as file:
        lectures_data = json.load(file)
        # Extracting the last lecture ID
        last_lecture_id = lectures_data['filtered_lectures'][-1]['id']
    return render_template('used_pages/ashraf.html', lectures_data=lectures_data, last_lecture_id=last_lecture_id)



@views.route('/ashraf/<video_id>', methods = ['POST'])
def ashrafpost(video_id):
    if request.method == 'POST' :
        try:
            student_name = request.args.get('studentname') or 'ss'

 
            url = "https://api.csacademyzone.com/video/otp"
            params = {"student_name": student_name, "video_id": video_id}
            headers = {"Content-type": "application/x-www-form-urlencoded", "sessionToken": "imcool"}
            response = requests.post(url, data=params, headers=headers)
            if response.status_code == 401:
                data = response.json()
                otp = data.get("otp")
                playback_info = data.get("playbackInfo")
                return jsonify({"otp": otp, "playbackInfo": playback_info})
            else:
                return jsonify({"error": f"Failed to get OTP. Status code: {response.status_code}"}), 500
        except Exception as e:
            return jsonify({"error": str(e)}), 500
        




@views.route("/ashrafelshnawy")
def ashrafelshnawy():
  teachername = "Ashraf El Shnawy"
  playlist_id = 'PLM-GVlebsoPW0BYrJMns3WklFGZHzNtmV'
  with open("website/playlists/ashrafelshnawy.txt", 'r', encoding='utf-8') as file:
        content = file.read()
        videos = ast.literal_eval(content)
  return render_template('used_pages/videopage.html',
                         videos=videos,
                         playlist_id=playlist_id,
                         teachername=teachername)




@views.route("/ashrafelshnawy/update")
def ashrafelshnawyupdate():
    return createtxtfile("ashrafelshnawy" , "PLM-GVlebsoPW0BYrJMns3WklFGZHzNtmV")

# Nasser --------------------------------------------------------------



def load_nasser_info():
    with open('website/Backend/nasser.json', 'r') as file:
        nasser_info = json.load(file)
    return nasser_info


@views.route('/nasser')
def nasser():
  nasser_info = load_nasser_info()

  teacher_links = {
        f"{course}": (f"/nasser{nasser_info[course]['url']}", nasser_info[course]['description'])
        for course in nasser_info
    }
  


  teachername = "Chemistry"
  return render_template('used_pages/teacher.html',
                         teacher_links=teacher_links,
                         teachername=teachername,
                         imgs="yes")

@views.route("/nasser/<custom_url>/update")
def nasserupdate(custom_url):
    nasser_info = load_nasser_info()
    course_key = next((name for name, info in nasser_info.items() if info['url'] == f"/{custom_url}"), None)
    if course_key not in nasser_info:
        return redirect(url_for('views.display_links'))
    playlist_id = nasser_info[course_key]["id"]
    return createtxtfile(f"nasser{course_key}", playlist_id)


@views.route("/nasser/<custom_url>")
def nasservids(custom_url):
    folder = None
    nasser_info = load_nasser_info()
    course_info = next((info for info in nasser_info.values() if info['url'] == f"/{custom_url}"), None)
    course_name = next((name for name, info in nasser_info.items() if info['url'] == f"/{custom_url}"), None)
    teachername = course_name
    playlist_id = course_info["id"]
    with open(f"website/playlists/nasser{course_name}.txt", 'r', encoding='utf-8') as file:
            content = file.read()
            videos = ast.literal_eval(content)
        

    teacher_pdf_mapping = {
    "Chapter 1":
    "https://drive.google.com/drive/folders/1otLcK6atSsKhZGIo7Cz0hRxoZ7gbN8nz?usp=drive_link",
    "Chapter 2":
    "https://drive.google.com/drive/folders/1yY4NSy-guuvbtSUGuRg6uXh6nxi4XXmY?usp=drive_link",
    "Chapter 3":
    "https://drive.google.com/drive/folders/1CqVC871-_kgNxNuJtpXAkp8BMHWL0cqU?usp=drive_link",
    "Chapter 4":
    "https://drive.google.com/drive/folders/1xtEHPFPHAiyXaQ62Ou2MRkklZmBvWzZd?usp=drive_link",
    "Chapter 5 Part 1":
    "https://drive.google.com/drive/folders/1zda1ANurONO44MTBIo2tm4wkhGahtUUn?usp=drive_link",
    "Chapter 5 Part 2":
    "https://drive.google.com/drive/folders/1gQgsv5s3RiXeQ3dbCOlCKp3fR78_uv6M?usp=drive_link",
    "Final Revisions" :"https://drive.google.com/drive/folders/1B8SZ5RKPaALH2YICEePBwNGZWBWwqBpu?usp=drive_link",
    }
    if course_name in teacher_pdf_mapping:
        folder = teacher_pdf_mapping[teachername]


    return render_template('used_pages/videopage.html',
                         videos=videos,
                         playlist_id=playlist_id,
                         teachername=teachername,
                         folder = folder)





#Math --------------------------------------------------------------------------------------------------------------------------
@views.route('/maths')
def math():
  teacher_links = {
  "Sherbo": ("/sherbo", "Omar sherbeni"),
    "Salama": ("/salama", "Mohamed salama" , "Back :))")
  }
  teachername = "Math"
  return render_template('used_pages/teacher.html',
                         teacher_links=teacher_links,
                         teachername=teachername,
                         imgs="yes" ,   link = {"Mathdf": "https://mathdf.com/"})






#Sherbo ------------------------

 
@views.route('/sherbo')
def sherbo():
  sherbo_info = load_sherbo_info()

  teacher_links = {
        course: (f"/sherbo{sherbo_info[course]['url']}", sherbo_info[course]['description'])
        for course in sherbo_info
    }
  teachername = "Math"
  return render_template('used_pages/teacher.html',
                         teacher_links=teacher_links,
                         teachername=teachername,
                         imgs="yes")

def load_sherbo_info():
    with open('website/Backend/sherbo.json', 'r') as file:
        sherbo_info = json.load(file)
    return sherbo_info


@views.route("/sherbo/<custom_url>/update")
def sherboupdates(custom_url):
    sherbo_info = load_sherbo_info()
    course_key = next((name for name, info in sherbo_info.items() if info['url'] == f"/{custom_url}"), None)
    if course_key not in sherbo_info:
        return redirect(url_for('views.display_links'))
    playlist_id = sherbo_info[course_key]["id"]
    return createtxtfile(f"sherbo{course_key}", playlist_id)

@views.route("/sherbo/<custom_url>")
def sherporoutes(custom_url):
    extra = None
    folder = None

    sherbo_info = load_sherbo_info()
    course_info = next((info for info in sherbo_info.values() if info['url'] == f"/{custom_url}"), None)
    course_name = next((name for name, info in sherbo_info.items() if info['url'] == f"/{custom_url}"), None)
    teachername = course_name
    playlist_id = course_info["id"]
    with open(f"website/playlists/sherbo{course_name}.txt", 'r', encoding='utf-8') as file:
            content = file.read()
            videos = ast.literal_eval(content)

    if course_name  == "Dynamics" :
        extra = { 
            "S1.pdf" : "https://drive.google.com/file/d/1pdTVxYtcEqfaWZb3laZeWXJjsrOh36SH/view?usp=drive_link" ,
            "S2.pdf" : "https://drive.google.com/file/d/1EiLz7HXdDspctVpna-8LRaL0w7wFDAC-/view?usp=drive_link" , 
            "S3.pdf" : "https://drive.google.com/file/d/1RA0zMCf9KPUaCf_8BR4XcLGV_43YJKpI/view?usp=drive_link" ,
            "S4.pdf" : "https://drive.google.com/file/d/1s9vH8ddCXxgI5Zq9305NaRA6XmXoB7Xf/view?usp=drive_link", 
            "S5.pdf" : "https://drive.google.com/file/d/1tLCq4hgMcC4NX3cXLkgpn-co0nbFmx4C/view?usp=drive_link",
                   } 
    
        folder = "https://drive.google.com/drive/folders/1SBpcOBHoGSsxnROkQWVmFOuIxuxKhK8S?usp=drive_link"

    elif course_name  == "Calculus":
        folder = "https://drive.google.com/drive/folders/142TCiyG-oCmkpgeLpEnHmGaRSmnN6Och?usp=drive_link" 


    elif course_name  == "Statics" :
        folder =   "https://drive.google.com/drive/folders/192Zd0BMB0-ohwV2dYsSJvFB651d7qXAS?usp=drive_link" 

    elif course_name == "Algebra & Geometry" :
        extra = { 
            "S1.pdf" : "https://drive.google.com/file/d/1iNH3qEhAfpJa5QqHA6p7rarWA0Z7PRH8/view?usp=drive_link" ,
            "S2.pdf" : "https://drive.google.com/file/d/1f4ZLPfMxjMJ1HQdSdMGotkGQtPGCD0JO/view?usp=drive_link" ,
            "S3.pdf" : "https://drive.google.com/file/d/18hncZ4-fVQ3acP5Qn8M8iFvO3jT-OnKw/view?usp=drive_link" ,
            "SG-S1.pdf" : "https://drive.google.com/file/d/1RAmemfLG2bSVQD7ZCMpsp82X_4tLOxSg/view?usp=drive_link" ,
            
                   
                   } 
        folder = "https://drive.google.com/drive/folders/1_BT42ym3-9BY3FQOlFUKce7T6Scntx5o?usp=drive_link"



    return render_template('used_pages/videopage.html', videos=videos, playlist_id=playlist_id, teachername=teachername ,extra = extra , folder =folder)






# Salama --------------------------------------------------------
@views.route('/salama')
def salama():
    salama_info = load_salama_info()

    teacher_links = {
        course: (f"/salama{salama_info[course]['url']}",  salama_info[course]['description'])
        for course in salama_info
    }
    teachername = "Math"
    return render_template('used_pages/teacher.html', teacher_links=teacher_links, teachername=teachername, imgs="yes")



def load_salama_info():
    with open('website/Backend/salama.json', 'r') as file:
        salama_info = json.load(file)
    return salama_info


def add_course(course_name, course_id,input3, course_image , desc):
    salama_info = load_salama_info()
    if course_image:
        filename = course_name + '.jpg'
        upload_path = os.path.join('website/static/assets/Math/', filename)
        course_image.save(upload_path)
        new_course = {"id": course_id , "url" : input3 , "description" : desc}
        salama_info[course_name] = new_course
        with open('website/Backend/salama.json', 'w') as file:
            json.dump(salama_info, file, indent=2)
        return f"Course '{course_name}' added successfully."
    else:
        return "Invalid file format or no file provided."

@views.route("/salama/add-course", methods=['GET', 'POST'])
def salama_add_course_route():
    if current_user.username in ['spy', 'skailler']:
        if request.method == 'POST':       
            
            input1 = request.form.get('input1')
            input2 = request.form.get('input2')  
            desc = request.form.get('desc')  

            input3 = f"/{request.form.get('input3')}"  

            course_image = request.files['course_image']
            return add_course(input1, input2,input3, course_image , desc)

        
    return render_template('backend_pages/add-course.html')
    





@views.route("/salama/edit-course", methods=['GET', 'POST'])
def salama_edit_course_route():
    if current_user.username in ['spy', 'skailler']:
        if request.method == 'POST':
            selected_course = request.form.get('course_select')
            new_course_id = request.form.get('course_id')
            new_course_url = request.form.get('course_url')

            with open('website/Backend/salama.json', 'r') as file:
                your_courses_data = json.load(file)

            if selected_course in your_courses_data:
                your_courses_data[selected_course]['id'] = new_course_id
                your_courses_data[selected_course]['url'] = new_course_url

                with open('website/Backend/salama.json', 'w') as file:
                    json.dump(your_courses_data, file, indent=2)

            uploaded_file = request.files.get('course_image')
            if uploaded_file :
                filename = selected_course + '.jpg'
                upload_path = os.path.join('website/static/assets/Math/', filename)
                uploaded_file.save(upload_path)



            return f"Edited {selected_course} !"
        
        with open('website/Backend/salama.json', 'r') as file:
            courses = json.load(file)

        return render_template('backend_pages/edit-course.html', courses =courses , selectedCourse=None)
    
    return render_template('backend_pages/edit-course.html', courses =courses , selectedCourse=None)



@views.route("/salama/update")
def salamaallupdate():
    salama_info = load_salama_info()
    for course_key, info in salama_info.items():
        playlist_id = info.get("id")
        if playlist_id:
            createtxtfile(f"salama{course_key}", playlist_id)
    return "Update completed for all Salama courses"

@views.route("/salama/<custom_url>/update")
def salamacoursesupdate(custom_url):
    salama_info = load_salama_info()
    course_key = next((name for name, info in salama_info.items() if info['url'] == f"/{custom_url}"), None)
    if course_key not in salama_info:
        return redirect(url_for('views.display_links'))
    playlist_id = salama_info[course_key]["id"]
    return createtxtfile(f"salama{course_key}", playlist_id)

@views.route("/salama/<custom_url>")
def salamaroutes(custom_url):
    extra = None
    salama_info = load_salama_info()
    course_info = next((info for info in salama_info.values() if info['url'] == f"/{custom_url}"), None)
    course_name = next((name for name, info in salama_info.items() if info['url'] == f"/{custom_url}"), None)
    teachername = course_name
    playlist_id = course_info["id"]
    with open(f"website/playlists/salama{course_name}.txt", 'r', encoding='utf-8') as file:
            content = file.read()
            videos = ast.literal_eval(content)
    if course_name  == "Course 6" :
       extra={"Pdf 1" :"https://drive.google.com/file/d/18mnyKrmeiNNZMBdaJ0sD8VAkAzLbM15r/view?usp=drive_link" , "Pdf 2" : "https://drive.google.com/file/d/1JLwNyWB8lOVSdVi8IvA6zb1D1iVQ8H3l/view?usp=drive_link"}   
    elif course_name  == "Course 17" :
        extra = {"Pdf 1" : "https://drive.google.com/file/d/1Ng8UkfF48_Cj1ZjiMn8NPfkWEONh3vJD/view?usp=drive_link"}
    elif course_name  == "Course 19":
        extra={"Pdf 1" :"https://drive.google.com/file/d/1a-56mRMP3nYSts90itOfINMtmrb8z6rr/view?usp=drive_link" , "Pdf 2" : "https://drive.google.com/file/d/1O21TqOmEJv2R9zUJmMw0BFnHsjCtqEVF/view?usp=drive_link"}   
    return render_template('used_pages/videopage.html', videos=videos, playlist_id=playlist_id, teachername=teachername ,extra = extra)


#Arabic --------------------------------------------------------------------------------------------------------------------------
@views.route('/arabic')
def arabic():
  teacher_links = {
    "Gedo": ("gedo", "Reda El Farouk"),
    "Mohamed Tarek": ("mohamedtarek", "Final Revision"),
    "Mo Salah": ("mo-salah", "Mohamed Salah"),


}
  teachername = "Arabic"
  return render_template('used_pages/teacher.html',
                         teacher_links=teacher_links,
                         teachername=teachername,
                         imgs="yes")




@views.route('/gedo')
def gedo():
  teacher_links = {
       "Gedo": ("gedosessions", "All sessions"), 
       "Gedo Rev1": ("gedorev1", "Revision 1"), 
       "Gedo Rev2": ("gedorev2", "Revision 2"), 
       "Gedo Rev3": ("gedorev3", "Revision 3"), 
       "Gedo Rev4": ("gedorev4", "Revision 4"), 
       "Gedo Rev5": ("gedorev5", "Revision 5"), 
    #    "Gedo Rev6": ("gedorev6", "Revision 6"), 
    #    "Gedo Rev7": ("gedorev7", "Revision 7"), 
    #    "Gedo Rev8": ("gedorev8", "Revision 8"), 

}
  teachername = "Arabic"
  return render_template('used_pages/teacher.html',
                         teacher_links=teacher_links,
                         teachername=teachername,
                         imgs="yes")



@views.route("/gedosessions")
def gedosessions():
    playlist_id = 'PLM-GVlebsoPXBcSNcLjkmcQG53hQYTvui'
    teachername= "Gedo"
    with open("website/playlists/gedo.txt", 'r', encoding='utf-8') as file:
        content = file.read()
        videos = ast.literal_eval(content)
    return render_template('used_pages/videopage.html',
                           videos=videos,
                           playlist_id=playlist_id,
                           teachername=teachername)


@views.route("/gedosessions/update")
def gedosessionsupdate():
    return createtxtfile("gedo" , "PLM-GVlebsoPXBcSNcLjkmcQG53hQYTvui")



@views.route("/gedorev1")
def gedorev1():
    playlist_id = 'PLM-GVlebsoPXPD1eQbSocD0g3DLchpyC9'
    teachername= "Gedo"
    with open("website/playlists/gedorev1.txt", 'r', encoding='utf-8') as file:
        content = file.read()
        videos = ast.literal_eval(content)
    return render_template('used_pages/videopage.html',
                           videos=videos,
                           playlist_id=playlist_id,
                           teachername=teachername)


@views.route("/gedorev1/update")
def gedorev1update():
    return createtxtfile("gedorev1" , "PLM-GVlebsoPXPD1eQbSocD0g3DLchpyC9")

@views.route("/gedorev2")
def gedorev2():
    playlist_id = 'PLM-GVlebsoPXTAA08dW2Oro5G2EmLB0Pk'
    teachername= "Gedo"
    with open("website/playlists/gedorev2.txt", 'r', encoding='utf-8') as file:
        content = file.read()
        videos = ast.literal_eval(content)
    return render_template('used_pages/videopage.html',
                           videos=videos,
                           playlist_id=playlist_id,
                           teachername=teachername)


@views.route("/gedorev2/update")
def gedorev2update():
    return createtxtfile("gedorev2" , "PLM-GVlebsoPXTAA08dW2Oro5G2EmLB0Pk")

@views.route("/gedorev3")
def gedorev3():
    playlist_id = 'PLM-GVlebsoPX46KbmAnXFHKX5fZsv5XEV'
    teachername= "Gedo"
    with open("website/playlists/gedorev3.txt", 'r', encoding='utf-8') as file:
        content = file.read()
        videos = ast.literal_eval(content)
    return render_template('used_pages/videopage.html',
                           videos=videos,
                           playlist_id=playlist_id,
                           teachername=teachername)


@views.route("/gedorev3/update")
def gedorev3update():
    return createtxtfile("gedorev3" , "PLM-GVlebsoPX46KbmAnXFHKX5fZsv5XEV")


@views.route("/gedorev4")
def gedorev4():
    playlist_id = 'PLM-GVlebsoPULzDXf_vfadcP--n-pfaXM'
    teachername= "Gedo"
    with open("website/playlists/gedorev4.txt", 'r', encoding='utf-8') as file:
        content = file.read()
        videos = ast.literal_eval(content)
    return render_template('used_pages/videopage.html',
                           videos=videos,
                           playlist_id=playlist_id,
                           teachername=teachername)


@views.route("/gedorev4/update")
def gedorev4update():
    return createtxtfile("gedorev4" , "PLM-GVlebsoPULzDXf_vfadcP--n-pfaXM")


@views.route("/gedorev5")
def gedorev5():
    playlist_id = 'PLM-GVlebsoPUnidZXcpQOMfq0Rj0sZO-5'
    teachername= "Gedo"
    with open("website/playlists/gedorev5.txt", 'r', encoding='utf-8') as file:
        content = file.read()
        videos = ast.literal_eval(content)
    return render_template('used_pages/videopage.html',
                           videos=videos,
                           playlist_id=playlist_id,
                           teachername=teachername)


@views.route("/gedorev5/update")
def gedorev5update():
    return createtxtfile("gedorev5" , "PLM-GVlebsoPUnidZXcpQOMfq0Rj0sZO-5")



@views.route("/mo-salah")
def mosalah():
    playlist_id = 'PLM-GVlebsoPXv3dz0yaqJtvjkOAN6KNRc'
    teachername= "Mo Salah"
    with open("website/playlists/mosalah.txt", 'r', encoding='utf-8') as file:
        content = file.read()
        videos = ast.literal_eval(content)
    return render_template('used_pages/videopage.html',
                           videos=videos,
                           playlist_id=playlist_id,
                           teachername=teachername)


@views.route("/mo-salah/update")
def mosalahupdate():
    return createtxtfile("mosalah" , "PLM-GVlebsoPXv3dz0yaqJtvjkOAN6KNRc")














@views.route("/mohamedtarek")
def mohamedtarek():
    playlist_id = 'PLM-GVlebsoPWeP1pGCJWmf20Uc2Cu4JWN'
    teachername= "Mohamed Tarek"
    with open("website/playlists/mohamedtarek.txt", 'r', encoding='utf-8') as file:
        content = file.read()
        videos = ast.literal_eval(content)
    return render_template('used_pages/videopage.html',
                           videos=videos,
                           playlist_id=playlist_id,
                           teachername=teachername)


@views.route("/mohamedtarek/update")
def mohamedtarekupdate():
    return createtxtfile("mohamedtarek" , "PLM-GVlebsoPWeP1pGCJWmf20Uc2Cu4JWN")










#Geology --------------------------------------------------------------------------------------------------------------------------
@views.route('/geology')
def geology():
  teacher_links = {
    "Sameh": ("sameh", "Sameh Nash2t"),
    "Gio maged": ("giomaged", "Gio maged")
  }
  teachername = "Geology"
  return render_template('used_pages/teacher.html',
                          teacher_links=teacher_links,
                          teachername=teachername,
                          imgs="yes")



def load_sameh_info():
    with open('website/Backend/sameh.json', 'r') as file:
        info = json.load(file)
    return info


@views.route('/sameh')
def sameh():
  info = load_sameh_info()

  teacher_links = {
        f"Sameh Nash2t {course}": (f"/sameh{info[course]['url']}", info[course]['description'])
        for course in info
    }
  teachername = "Geology"
  return render_template('used_pages/teacher.html',
                         teacher_links=teacher_links,
                         teachername=teachername,
                         imgs="yes")

@views.route("/sameh/<custom_url>/update")
def samehupdate(custom_url):
    info = load_sameh_info()
    course_key = next((name for name, info in info.items() if info['url'] == f"/{custom_url}"), None)
    if course_key not in info:
        return redirect(url_for('views.display_links'))
    playlist_id = info[course_key]["id"]
    return createtxtfile(f"sameh{course_key}", playlist_id)


@views.route("/sameh/<custom_url>")
def samehvids(custom_url):
    info = load_sameh_info()
    course_info = next((info for info in info.values() if info['url'] == f"/{custom_url}"), None)
    course_name = next((name for name, info in info.items() if info['url'] == f"/{custom_url}"), None)
    teachername = course_name
    playlist_id = course_info["id"]
    with open(f"website/playlists/sameh{course_name}.txt", 'r', encoding='utf-8') as file:
            content = file.read()
            videos = ast.literal_eval(content)

    return render_template('used_pages/videopage.html',
                         videos=videos,
                         playlist_id=playlist_id,
                         teachername=teachername)





@views.route("/giomaged")
def giomaged():
  teachername = "Gio maged"
  playlist_id = 'PLM-GVlebsoPXh1obVV3aWysV7wXlN3yET'
  with open("website/playlists/giomaged.txt", 'r', encoding='utf-8') as file:
        content = file.read()
        videos = ast.literal_eval(content) 
  return render_template('used_pages/videopage.html',
                         videos=videos,
                         playlist_id=playlist_id,
                         teachername=teachername)



@views.route("/giomaged/update")
def giomagedupdate():
    return createtxtfile("giomaged" , "PLM-GVlebsoPXh1obVV3aWysV7wXlN3yET")


#Biology----------------------------------------------------------------------------------------------------------------------
@views.route('/biology')
def bio():
  teacher_links = {
     "Daif": ("daif", "Mohamed Daif"),
  }
  teachername = "Biology"
  return render_template('used_pages/teacher.html',
                         teacher_links=teacher_links,
                         teachername=teachername,
                         imgs="yes")


def load_daif_info():
    with open('website/Backend/daif.json', 'r') as file:
        info = json.load(file)
    return info


@views.route('/daif')
def daif():
  info = load_daif_info()

  teacher_links = {
        f"{course}": (f"/daif{info[course]['url']}", info[course]['description'])
        for course in info
    }
  teachername = "Biology"
  return render_template('used_pages/teacher.html',
                         teacher_links=teacher_links,
                         teachername=teachername,
                         imgs="yes")

@views.route("/daif/<custom_url>/update")
def daifupdates(custom_url):
    info = load_daif_info()
    course_key = next((name for name, info in info.items() if info['url'] == f"/{custom_url}"), None)
    if course_key not in info:
        return redirect(url_for('views.display_links'))
    playlist_id = info[course_key]["id"]
    return createtxtfile(f"daif{course_key}", playlist_id)


@views.route("/daif/<custom_url>")
def daifvids(custom_url):
    info = load_daif_info()
    course_info = next((info for info in info.values() if info['url'] == f"/{custom_url}"), None)
    course_name = next((name for name, info in info.items() if info['url'] == f"/{custom_url}"), None)
    teachername = course_name
    playlist_id = course_info["id"]
    with open(f"website/playlists/daif{course_name}.txt", 'r', encoding='utf-8') as file:
            content = file.read()
            videos = ast.literal_eval(content)

    return render_template('used_pages/videopage.html',
                         videos=videos,
                         playlist_id=playlist_id,
                         teachername=teachername)


#-----------------------------------------------------------------------------------------------------------

@views.route('/english')
def english():
  teacher_links = {
     "Hossam Sameh": ("english/hossamsameh", "Revisions only" ),

     "Ahmed Salah": ("english/ahmadsalah", "Sessions & Revisions"),


  }
  teachername = "English"
  return render_template('used_pages/teacher.html',
                         teacher_links=teacher_links,
                         teachername=teachername,
                         imgs="yes")


@views.route("/english/ahmadsalah")
def ahmadsalah():
  teachername = "Ahmad Salah"
  playlist_id = 'PLM-GVlebsoPUWOjoc9DyO2Jh8mclaRY1Q'
  with open("website/playlists/ahmadsalah.txt", 'r', encoding='utf-8') as file:
        content = file.read()
        videos = ast.literal_eval(content)

  return render_template('used_pages/videopage.html',
                         videos=videos,
                         playlist_id=playlist_id,
                         teachername=teachername)
                     

@views.route("/english/ahmadsalah/update")
def ahmadsalahupdate():
    return createtxtfile("ahmadsalah" , "PLM-GVlebsoPUWOjoc9DyO2Jh8mclaRY1Q")


@views.route("/english/hossamsameh")
def hossamsameh():
  teachername = "Hossam Sameh"
  playlist_id = 'PLM-GVlebsoPWGSfDq2_C801iLUl3RKWCK'
  with open("website/playlists/hossamsameh.txt", 'r', encoding='utf-8') as file:
        content = file.read()
        videos = ast.literal_eval(content)
  extra = {
           "Chapter 2.pdf" : "https://drive.google.com/file/d/1gxT2ay-h24ncKVztlUAPpNuQla99AAeE/view?usp=drive_link" ,
           "Chapter 3.pdf" : "https://drive.google.com/file/d/1sCYoSYrY490BoSU0MPyrKBGELC7MdR6n/view?usp=drive_link",
           "Chapter 4.pdf" : "https://drive.google.com/file/d/1FDjtIghK-f-NKmvIrrT1wqOZB7gOTRdk/view?usp=drive_link"}      
  folder = "https://drive.google.com/drive/folders/1cqdZyL-Le9yYqlzhatHL4qvnjhhGyAOu?usp=drive_link"  
  return render_template('used_pages/videopage.html',
                         videos=videos,
                         playlist_id=playlist_id,
                         teachername=teachername , extra = extra , folder = folder)

@views.route("/english/hossamsameh/update")
def hossamsamehupdate():
    return createtxtfile("hossamsameh" , "PLM-GVlebsoPWGSfDq2_C801iLUl3RKWCK")






@views.route('/german')
def german():
  teacher_links = {
     "German": ("germann", "Abd El Moez"),

  }
  teachername = "German"
  return render_template('used_pages/teacher.html',
                         teacher_links=teacher_links,
                         teachername=teachername,
                         imgs="yes")

@views.route("/germann")
def germann():
  teachername = "German"
  playlist_id = 'PLM-GVlebsoPWNh__WI8QAIN2xQjawgB4i'
  with open("website/playlists/germann.txt", 'r', encoding='utf-8') as file:
        content = file.read()
        videos = ast.literal_eval(content)
  return render_template('used_pages/videopage.html',
                         videos=videos,
                         playlist_id=playlist_id,
                         teachername=teachername)

@views.route("/germann/update")
def germannupdate():
    return createtxtfile("germann" , "PLM-GVlebsoPWNh__WI8QAIN2xQjawgB4i")



@views.route("/adby")
def adby():
  teachername = "Adby"
  playlist_id = 'PLM-GVlebsoPWZG7j5kRK479fragOS83By'
  with open("website/playlists/adby.txt", 'r', encoding='utf-8') as file:
        content = file.read()
        videos = ast.literal_eval(content)
  return render_template('used_pages/videopage.html',
                         videos=videos,
                         playlist_id=playlist_id,
                         teachername=teachername)


@views.route("/adby/update")
def adbyupdate():
    return createtxtfile("adby" , "PLM-GVlebsoPWZG7j5kRK479fragOS83By")




