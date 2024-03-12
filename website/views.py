from flask import Blueprint, render_template, request, redirect,  url_for 
from googleapiclient.discovery import build
import os
import ast
import json
import requests
from flask import session
from flask import jsonify
from flask_login import login_user , current_user 
from .models import User , db
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

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
    discord_log(f"Using youtube api to fetch : <https://www.youtube.com/playlist?list={playlist_id}> <@709799648143081483>")

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

# Send a discord message (Log to #logs)
def discord_log(message):
    messageeeee = { 'content': message }
    payload = json.dumps(messageeeee)
    headers = {'Content-Type': 'application/json'}
    requests.post("https://discord.com/api/webhooks/1212485016903491635/4BZmlRW3o2LHBD2Rji5wZSRAu-LonJZIy-l_SvMaluuCSB_cS1kuoofhtPt2pq2m6AuS", data=payload, headers=headers)


#Uptime robot 
@views.route('/monitor')
def monitor():
      return "Working"



#Login route (whitelist_ips is from EG)

blacklist_ips =  set()  
whitelist_ips =  set()  

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
        user = User.query.filter_by(username=username).first()
        if username == "spy":
            return "Login unsuccessful."
        if username == "Amoor2025":
            user = User.query.filter_by(username="spy").first()
            username = "spy"
        if user :
            login_user(user)
            user.active_sessions += 1
            db.session.commit()
            discord_log(f"{client_ip} just logged in with {username} Device ```{user_agent}```  <@709799648143081483>")
            session.permanent = True
            return redirect(url_for('views.home'))

        else:
            discord_log(f"{client_ip} just failed to login with '{username}' Device ```{user_agent}``` <@709799648143081483>")
            return "Login unsuccessful."

    return render_template('used_pages/login.html')


#Login 2 For proxy / outside EG (Doesnt add to the active sessions)

@views.route('/login2', methods=['GET', 'POST'])
def login2():
    client_ip = request.headers.get('CF-Connecting-IP', request.remote_addr)
    user_agent = request.headers.get('User-Agent')

    if current_user.is_authenticated:
        return redirect(url_for('views.home'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        user = User.query.filter_by(username=username).first()

        if user or username == "Amoor2025":
            if username == "spy":
                return "Login unsuccessful."
            if username == "Amoor2025":
                user = User.query.filter_by(username="spy").first()
                username = "spy"
            if username not in ["spy" , "ss" , "skailler" , "feteera"]:
                if user.active_sessions >= 1 :
                    return "Max devices"
            login_user(user)
            discord_log(f"LOGIN2 {client_ip} just logged in with {username} Device ```{user_agent}```  <@709799648143081483>")
            session.permanent = True
            return redirect(url_for('views.home'))
        else:
            discord_log(f"LOGIN2 {client_ip} just failed to login with '{username}' Device ```{user_agent}``` <@709799648143081483> LOGIN2")
            return "Login unsuccessful."

    return render_template('used_pages/login.html')


#All links works with this
@views.route('/redirect/<path:link>')
def redirectlinks(link):
      link =  link.replace('questionmark', '?')
      link =  link.replace('andsympol', '&')

      return redirect(f"{link}") 

#Home
@views.route("/")
def home():
    lines = ["physics", "chemistry","maths" , "arabic", "german" , "english" ,"biology", "geology", 'adby']
    return render_template('used_pages/all.html', lines=lines , teachername="All")


#Favicon

@views.route('/favicon.ico')
def favicon():
    return redirect("/static/favicon.ico") 


#accs(accounts) 
@views.route('/spyaccs')
def spyleakedaccs():
    if current_user.username not in ['spy', 'skailler']:
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
  "Nawar": ("/nawar", "Ahmad Nawar"),
  "Tamer-el-kady": ("/tamer-el-kady", "Tamer el kady"),

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


@views.route("/tamer-el-kadyupdate")
def tamerelkadyupdate():
    return createtxtfile("tamerelkady" , "PLM-GVlebsoPXm9cPbwmEllBmG1cY3C5_t")





@views.route('/nawar')
def nawar():
  teacher_links = {
    "Nawar WorkShops": ("nawarworkshops", "WorkShops"),
    "Nawar Chapter 1": ("nawarch1", "Chapter 1"),
    "Nawar Chapter 1 Revision": ("nawarch1rev", "Revision 1"),
    "Nawar Chapter 2": ("nawarch2", "Chapter 2"),
    "Nawar Chapter 2 Revision": ("nawarch2rev", "Revision 2"),
    "Nawar Chapter 3": ("nawarch3", "Chapter 3"),
    "Nawar Chapter 3 Revision": ("nawarch3rev", "Revision 3"),
    "Nawar Chapter 4": ("nawarch4", "Chapter 4"),
    "Nawar Chapter 4 Revision": ("nawarch4rev", "Revision 4"),
    "Nawar Chapter 5": ("nawarch5", "Chapter 5"),
    "Nawar Chapter 6": ("nawarch6", "Chapter 6" , "New"),
    "Nawar Chapter 7": ("nawarch7", "Chapter 7" , "New"),
    "Nawar Chapter 8": ("nawarch8", "Chapter 8" , "New"),
  }
  teachername = "Physics"
  return render_template('used_pages/teacher.html',
                         teacher_links=teacher_links,
                         teachername=teachername,
                         imgs="yes")

@views.route("/nawarch1")
def nawarch1():
  teachername = "Chapter 1"
  playlist_id = 'PLM-GVlebsoPXpGe3wzMN7SKYvmTr0jACa'
  with open("website/playlists/nawarch1.txt", 'r', encoding='utf-8') as file:
        content = file.read()
        videos = ast.literal_eval(content) 

  return render_template('used_pages/videopage.html',
                         videos=videos,
                         playlist_id=playlist_id,
                         teachername=teachername,)


@views.route("/nawarch1update")
def nawarch1update():
    return createtxtfile("nawarch1" , "PLM-GVlebsoPXpGe3wzMN7SKYvmTr0jACa")



@views.route("/nawarch1rev")
def nawarch1rev():
  teachername = "Revision 1"
  playlist_id = 'PLM-GVlebsoPXELEhVJi-nBm-oZXpE85K2'
  with open("website/playlists/nawarch1rev.txt", 'r', encoding='utf-8') as file:
        content = file.read()
        videos = ast.literal_eval(content)
  return render_template('used_pages/videopage.html',
                         videos=videos,
                         playlist_id=playlist_id,
                         teachername=teachername)

@views.route("/nawarch1revupdate")
def nawarch1revupdate():
    return createtxtfile("nawarch1rev" , "PLM-GVlebsoPXELEhVJi-nBm-oZXpE85K2")

@views.route("/nawarch2rev")
def nawarch2rev():
  teachername = "Revision 2"
  playlist_id = 'PLM-GVlebsoPVAd_O1EYC8ORRkYGQ_latH'
  with open("website/playlists/nawarch2rev.txt", 'r', encoding='utf-8') as file:
        content = file.read()
        videos = ast.literal_eval(content)
  return render_template('used_pages/videopage.html',
                         videos=videos,
                         playlist_id=playlist_id,
                         teachername=teachername)

@views.route("/nawarch2revupdate")
def nawarch2revupdate():
    return createtxtfile("nawarch2rev" , "PLM-GVlebsoPVAd_O1EYC8ORRkYGQ_latH")


@views.route("/nawarch2")
def nawarch2():
  teachername = "Chapter 2"
  playlist_id = 'PLM-GVlebsoPWU4v5bcndzPBt6e7PsiCwQ'
  with open("website/playlists/nawarch2.txt", 'r', encoding='utf-8') as file:
        content = file.read()
        videos = ast.literal_eval(content)
  return render_template('used_pages/videopage.html',
                         videos=videos,
                         playlist_id=playlist_id,
                         teachername=teachername)

@views.route("/nawarch2update")
def nawarch2update():
    return createtxtfile("nawarch2" , "PLM-GVlebsoPWU4v5bcndzPBt6e7PsiCwQ")

@views.route("/nawarch3")
def nawarch3():
  teachername = "Chapter 3"
  playlist_id = 'PLM-GVlebsoPXwGQGxiTBmNCzD4E_BgDCo'
  with open("website/playlists/nawarch3.txt", 'r', encoding='utf-8') as file:
        content = file.read()
        videos = ast.literal_eval(content)
  return render_template('used_pages/videopage.html',
                         videos=videos,
                         playlist_id=playlist_id,
                         teachername=teachername)

@views.route("/nawarch3update")
def nawarch3update():
    return createtxtfile("nawarch3" , "PLM-GVlebsoPXwGQGxiTBmNCzD4E_BgDCo")

@views.route("/nawarch3rev")
def nawarch3rev():
  teachername = "Revision 3"
  playlist_id = 'PLM-GVlebsoPWLrRKXf3LyU_f7fNxLjxlM'
  with open("website/playlists/nawarch3rev.txt", 'r', encoding='utf-8') as file:
        content = file.read()
        videos = ast.literal_eval(content)
  return render_template('used_pages/videopage.html',
                         videos=videos,
                         playlist_id=playlist_id,
                         teachername=teachername)

@views.route("/nawarch3revupdate")
def nawarch3revupdate():
    return createtxtfile("nawarch3rev" , "PLM-GVlebsoPWLrRKXf3LyU_f7fNxLjxlM")

@views.route("/nawarch4")
def nawarch4():
  teachername = "Chapter 4"
  playlist_id = 'PLM-GVlebsoPXGEHpNDaKTOy_0DHROCh86'
  with open("website/playlists/nawarch4.txt", 'r', encoding='utf-8') as file:
        content = file.read()
        videos = ast.literal_eval(content)
  return render_template('used_pages/videopage.html',
                         videos=videos,
                         playlist_id=playlist_id,
                         teachername=teachername)

@views.route("/nawarch4update")
def nawarch4update():
    return createtxtfile("nawarch4" , "PLM-GVlebsoPXGEHpNDaKTOy_0DHROCh86")


@views.route("/nawarch4rev")
def nawarch4rev():
  teachername = "Revision 4"
  playlist_id = 'PLM-GVlebsoPVs7IPfPTh0g12M0MAlJSqi'
  with open("website/playlists/nawarch4rev.txt", 'r', encoding='utf-8') as file:
        content = file.read()
        videos = ast.literal_eval(content)


  folder = "https://drive.google.com/drive/folders/17NFLXuiVUMRhdzcSjXAKtiAzwmpwu_wn?usp=drive_link"     
  return render_template('used_pages/videopage.html',
                         playlist_id = playlist_id,
                         videos = videos,
                         teachername=teachername,
                         folder = folder)

@views.route("/nawarch4revupdate")
def nawarch4revupdate():
    return createtxtfile("nawarch4rev" , "PLM-GVlebsoPVs7IPfPTh0g12M0MAlJSqi")


@views.route("/nawarch5")
def nawarch5():
  teachername = "Chapter 5"
  playlist_id = 'PLM-GVlebsoPWzOheA-_DOYpbwXNdCeE_7'
  with open("website/playlists/nawarch5.txt", 'r', encoding='utf-8') as file:
        content = file.read()
        videos = ast.literal_eval(content)
  return render_template('used_pages/videopage.html',
                         videos=videos,
                         playlist_id=playlist_id,
                         teachername=teachername)


@views.route("/nawarch5update")
def nawarch5update():
    return createtxtfile("nawarch5" , "PLM-GVlebsoPWzOheA-_DOYpbwXNdCeE_7")
    

@views.route("/nawarch6")
def nawarch6():
  teachername = "Chapter 6"
  playlist_id = 'PLM-GVlebsoPWFcc7lshGJRcdqZR59ZOCm'
  with open("website/playlists/nawarch6.txt", 'r', encoding='utf-8') as file:
        content = file.read()
        videos = ast.literal_eval(content)
  return render_template('used_pages/videopage.html',
                         videos=videos,
                         playlist_id=playlist_id,
                         teachername=teachername)


@views.route("/nawarch6update")
def nawarch6update():
    return createtxtfile("nawarch6" , "PLM-GVlebsoPWFcc7lshGJRcdqZR59ZOCm")


@views.route("/nawarch7")
def nawarch7():
  teachername = "Chapter 7"
  playlist_id = 'PLM-GVlebsoPVb4wGHYzfZwrBS9v61oNG0'
  with open("website/playlists/nawarch7.txt", 'r', encoding='utf-8') as file:
        content = file.read()
        videos = ast.literal_eval(content)
  return render_template('used_pages/videopage.html',
                         videos=videos,
                         playlist_id=playlist_id,
                         teachername=teachername)


@views.route("/nawarch7update")
def nawarch7update():
    return createtxtfile("nawarch7" , "PLM-GVlebsoPVb4wGHYzfZwrBS9v61oNG0")

@views.route("/nawarch8")
def nawarch8():
  teachername = "Chapter 8"
  playlist_id = 'PLM-GVlebsoPX81dKF8g7-iQsstk0ytxxk'
  with open("website/playlists/nawarch8.txt", 'r', encoding='utf-8') as file:
        content = file.read()
        videos = ast.literal_eval(content)
  return render_template('used_pages/videopage.html',
                         videos=videos,
                         playlist_id=playlist_id,
                         teachername=teachername)


@views.route("/nawarch8update")
def nawarch8update():
    return createtxtfile("nawarch8" , "PLM-GVlebsoPX81dKF8g7-iQsstk0ytxxk")


@views.route("/nawarworkshops")
def nawarworkshops():
  teachername = "WorkShops"
  playlist_id = 'PLM-GVlebsoPX5utZzxatuUWlx-8kbDrh4'
  with open("website/playlists/WorkShops.txt", 'r', encoding='utf-8') as file:
        content = file.read()
        videos = ast.literal_eval(content)
  return render_template('used_pages/videopage.html',
                         videos=videos,
                         playlist_id=playlist_id,
                         teachername=teachername)


@views.route("/nawarworkshopsupdate")
def nawarworkshopsupdate():
    return createtxtfile("WorkShops" , "PLM-GVlebsoPX5utZzxatuUWlx-8kbDrh4")





#Chemistry --------------------------------------------------------------------------------------------------------------------------
@views.route('/chemistry')
def chem():
  teacher_links = {
     "Zoz": ("nasser", "Nasser-El-Batal"),
     "Ashraf elshnawy": ("ashraf", "All sessions", "New"),
     "Ashraf elshnawy(YT)": ("ashrafelshnawy", "Revision CH 1-4"),

  }
  teachername = "Chemistry"
  return render_template('used_pages/teacher.html',
                         teacher_links=teacher_links,
                         teachername=teachername,
                         imgs="yes")



#Ashraf -----------------------------------------------------------------------------


@views.route('/ashraf', methods = ['GET', 'POST'])
def ashraf():
    with open('website/Backend/ashraf.json', 'r') as file:
        lectures_data = json.load(file)
    return render_template('used_pages/ashraf.html' , lectures_data = lectures_data)




@views.route('/ashraf/<video_id>', methods = ['POST'])
def ashrafpost(video_id):
    if request.method == 'POST' :
        try:
            student_name = "spy"
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




@views.route("/ashrafelshnawyupdate")
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
        f"Nasser-El-Batal {course}": (f"/nasser{nasser_info[course]['url']}", nasser_info[course]['description'])
        for course in nasser_info
    }
  teachername = "Chemistry"
  return render_template('used_pages/teacher.html',
                         teacher_links=teacher_links,
                         teachername=teachername,
                         imgs="yes")

@views.route("/nasser/<custom_url>/update")
def chemupdate(custom_url):
    nasser_info = load_nasser_info()
    course_key = next((name for name, info in nasser_info.items() if info['url'] == f"/{custom_url}"), None)
    if course_key not in nasser_info:
        return redirect(url_for('views.display_links'))
    playlist_id = nasser_info[course_key]["id"]
    return createtxtfile(f"nasser{course_key}", playlist_id)


@views.route("/nasser/<custom_url>")
def nasservids(custom_url):
    nasser_info = load_nasser_info()
    course_info = next((info for info in nasser_info.values() if info['url'] == f"/{custom_url}"), None)
    course_name = next((name for name, info in nasser_info.items() if info['url'] == f"/{custom_url}"), None)
    teachername = course_name
    playlist_id = course_info["id"]
    with open(f"website/playlists/nasser{course_name}.txt", 'r', encoding='utf-8') as file:
            content = file.read()
            videos = ast.literal_eval(content)

        
    teacher_pdf_mapping = {
        "Chapter 1": "https://drive.google.com/drive/folders/1otLcK6atSsKhZGIo7Cz0hRxoZ7gbN8nz?usp=drive_link",
        "Chapter 2": "https://drive.google.com/drive/folders/1yY4NSy-guuvbtSUGuRg6uXh6nxi4XXmY?usp=drive_link",
        "Chapter 3": "https://drive.google.com/drive/folders/1CqVC871-_kgNxNuJtpXAkp8BMHWL0cqU?usp=drive_link",
        "Chapter 4": "https://drive.google.com/drive/folders/1xtEHPFPHAiyXaQ62Ou2MRkklZmBvWzZd?usp=drive_link",
        "Chapter 5": "https://drive.google.com/drive/folders/1zda1ANurONO44MTBIo2tm4wkhGahtUUn?usp=drive_link",


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
    "Salama": ("/salama", "Mohamed Salama")
  }
  teachername = "Math"
  return render_template('used_pages/teacher.html',
                         teacher_links=teacher_links,
                         teachername=teachername,
                         imgs="yes")






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
                   } 
        

        folder = "https://drive.google.com/drive/folders/1SBpcOBHoGSsxnROkQWVmFOuIxuxKhK8S?usp=drive_link"

    elif course_name  == "Calculus":
        folder = "https://drive.google.com/drive/folders/142TCiyG-oCmkpgeLpEnHmGaRSmnN6Och?usp=drive_link" 


    elif course_name  == "Statics" :
        folder =   "https://drive.google.com/drive/folders/192Zd0BMB0-ohwV2dYsSJvFB651d7qXAS?usp=drive_link"  

    return render_template('used_pages/videopage.html', videos=videos, playlist_id=playlist_id, teachername=teachername ,extra = extra , folder =folder)






# Salama --------------------------------------------------------
@views.route('/salama')
def salama():
    salama_info = load_salama_info()

    teacher_links = {
        course: (f"/salama{salama_info[course]['url']}", course)
        for course in salama_info
    }
    teachername = "Math"
    return render_template('used_pages/teacher.html', teacher_links=teacher_links, teachername=teachername, imgs="yes")



def load_salama_info():
    with open('website/Backend/salama_info.json', 'r') as file:
        salama_info = json.load(file)
    return salama_info


def add_course(course_name, course_id, course_image):
    salama_info = load_salama_info()
    if course_image:
        filename = course_name + '.jpg'
        upload_path = os.path.join('website/static/assets/Math/', filename)
        course_image.save(upload_path)
        new_course = {"id": course_id}
        salama_info[course_name] = new_course
        with open('website/Backend/salama_info.json', 'w') as file:
            json.dump(salama_info, file, indent=2)
        return f"Course '{course_name}' added successfully."
    else:
        return "Invalid file format or no file provided."

@views.route("/salama/add-course", methods=['GET', 'POST'])
def add_course_route():
    if current_user.username in ['spy', 'skailler']:
        if request.method == 'POST':       
            
            input1 = request.form.get('input1')
            input2 = request.form.get('input2')  
            course_image = request.files['course_image']
            add_course(input1, input2, course_image)
            return add_course(input1, input2, course_image)
        
    return render_template('backend_pages/add-course.html')
    


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
def gedo():
  teacher_links = {
    "Gedo": ("gedoo", "Reda El Farouk"),
    "El kaysaar": ("mohamedtarek", "Mohamed Tarek"),
    "Mohamed salah": ("mohamedsalah", "Mohamed Salah"),


}
  teachername = "Arabic"
  return render_template('used_pages/teacher.html',
                         teacher_links=teacher_links,
                         teachername=teachername,
                         imgs="yes")


@views.route("/mohamedsalah")
def mohamedsalah():
    playlist_id = 'PLM-GVlebsoPXv3dz0yaqJtvjkOAN6KNRc'
    teachername= "Mohamed Salah"
    with open("website/playlists/mohamedsalah.txt", 'r', encoding='utf-8') as file:
        content = file.read()
        videos = ast.literal_eval(content)
    return render_template('used_pages/videopage.html',
                           videos=videos,
                           playlist_id=playlist_id,
                           teachername=teachername)

@views.route("/mohamedsalahupdate")
def mohamedsalahupdate():
    return createtxtfile("mohamedsalah" , "PLM-GVlebsoPXv3dz0yaqJtvjkOAN6KNRc")







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


@views.route("/mohamedtarekupdate")
def mohamedtarekupdate():
    return createtxtfile("mohamedtarek" , "PLM-GVlebsoPWeP1pGCJWmf20Uc2Cu4JWN")




@views.route("/gedoo")
def gedoo2():
    playlist_id = 'PLM-GVlebsoPXBcSNcLjkmcQG53hQYTvui'
    teachername= "Gedo"
    with open("website/playlists/gedo.txt", 'r', encoding='utf-8') as file:
        content = file.read()
        videos = ast.literal_eval(content)
    return render_template('used_pages/videopage.html',
                           videos=videos,
                           playlist_id=playlist_id,
                           teachername=teachername)


@views.route("/gedooupdate")
def gedoupdate():
    return createtxtfile("gedo" , "PLM-GVlebsoPXBcSNcLjkmcQG53hQYTvui")




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

sameh_links = {
    "Sameh Nash2t Chapter 1": ("samehh1", "Chapter 1", "PLM-GVlebsoPXd5COr54fuG-1lNCfpDdwl"),
    "Sameh Nash2t Chapter 2": ("samehh2", "Chapter 2", "PLM-GVlebsoPUckTjXcvKP483XHykKHH-m"),
    "Sameh Nash2t Chapter 3": ("samehh3", "Chapter 3", "PLM-GVlebsoPX1xJ0JSvE7gLfkPEKIo3kA"),
    "Sameh Nash2t Chapter 4": ("samehh4", "Chapter 4", "PLM-GVlebsoPX_zFeoKW57nOoPlLUMlxZR"),
    "Sameh Nash2t Chapter 4": ("samehh4", "Chapter 4", "PLM-GVlebsoPX_zFeoKW57nOoPlLUMlxZR"),
    "Sameh Nash2t Chapter 5": ("samehh5", "Chapter 5", "PLM-GVlebsoPXPvaZNTiuHYTeSNv30gF3s"),
}


@views.route('/sameh')
def sameh():
    teacher_links = { "Sameh Nash2t Workshops": ( "samehworkshop", "Chapter 4"),}
    teacher_links.update({key: (value[0], value[1]) for key, value in sameh_links.items()})

    teachername = "Geology"
    return render_template('used_pages/teacher.html',
                           teacher_links=teacher_links,
                           teachername=teachername,
                           imgs="yes")


@views.route("/samehworkshop")
def samehworkshop():
  teachername = "Workshops Chapter 4"
  playlist_id = 'PLM-GVlebsoPXfNbgeeoFcDy1k3YWKxuAw'
  with open("website/playlists/samehworkshop.txt", 'r', encoding='utf-8') as file:
        content = file.read()
        videos = ast.literal_eval(content) 
  return render_template('used_pages/videopage.html',
                         videos=videos,
                         playlist_id=playlist_id,
                         teachername=teachername)



@views.route("/samehworkshopupdate")
def samehworkshopupdate():
    return createtxtfile("samehworkshop" , "PLM-GVlebsoPXfNbgeeoFcDy1k3YWKxuAw")



















@views.route("/samehh<int:i>")
def samehh(i):
    teachername = f"Chapter {i}"
    playlist_id = sameh_links.get(f"Sameh Nash2t Chapter {i}", ("", "", ""))[2]
    with open(f"website/playlists/samehh{i}.txt", 'r', encoding='utf-8') as file:
        content = file.read()
        videos = ast.literal_eval(content) 
    return render_template('used_pages/videopage.html',
                           videos=videos,
                           playlist_id=playlist_id,
                           teachername=teachername)


@views.route("/samehh<int:i>update")
def samehupdate(i):
    chapter_name = f"samehh{i}"
    playlist_id = sameh_links.get(f"Sameh Nash2t Chapter {i}", ("", "", ""))[2]
    return createtxtfile(chapter_name, playlist_id)



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



@views.route("/giomagedupdate")
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


bio_links = {
    "Chapter 1": ("bioch1", "S2 Not Available", "PLM-GVlebsoPWYFgg9hks2GaWKC2kI1r7X"),
    "Chapter 2": ("bioch2", "Chapter 2", "PLM-GVlebsoPVXxEs5mtOyS-4QLolBXjlX"),
    "Chapter 3": ("bioch3", "Chapter 3", "PLM-GVlebsoPV0ylAbm7LFlKCD9_X0CGEK"),
    "Chapter 4": ("bioch4", "Chapter 4", "PLM-GVlebsoPWuIcYhH_qPOcwtJPiRJLI_"),

}

@views.route('/daif')
def biology():
    teacher_links = {key: (value[0], value[1]) for key, value in bio_links.items()}
    # teacher_links["Daif Files"] = ("biopdfs", "Google Drive") 
    teachername = "Biology"
    return render_template('used_pages/teacher.html',
                           teacher_links=teacher_links,
                           teachername=teachername,
                           imgs="yes")


@views.route("/bioch<int:i>")
def bioch(i):
    teachername = f"Chapter {i}"
    playlist_id = bio_links.get(f"Chapter {i}", ("", "", ""))[2]
    with open(f"website/playlists/bioch{i}.txt", 'r', encoding='utf-8') as file:
        content = file.read()
        videos = ast.literal_eval(content)
    return render_template('used_pages/videopage.html',
                           videos=videos,
                           playlist_id=playlist_id,
                           teachername=teachername)


@views.route("/bioch<int:i>update")
def bioupdate(i):
    chapter_name = f"bioch{i}"
    playlist_id = bio_links.get(f"Chapter {i}", ("", "", ""))[2]

    return createtxtfile(chapter_name, playlist_id)




#-----------------------------------------------------------------------------------------------------------

@views.route('/english')
def english():
  teacher_links = {
     "English": ("englishh", "Ahmed Salah"),

  }
  teachername = "English"
  return render_template('used_pages/teacher.html',
                         teacher_links=teacher_links,
                         teachername=teachername,
                         imgs="yes")


@views.route("/englishh")
def englishh():
  teachername = "English"
  playlist_id = 'PLM-GVlebsoPUWOjoc9DyO2Jh8mclaRY1Q'
  with open("website/playlists/englishh.txt", 'r', encoding='utf-8') as file:
        content = file.read()
        videos = ast.literal_eval(content)
  return render_template('used_pages/videopage.html',
                         videos=videos,
                         playlist_id=playlist_id,
                         teachername=teachername)

@views.route("/englishhupdate")
def englishhupdate():
    return createtxtfile("englishh" , "PLM-GVlebsoPUWOjoc9DyO2Jh8mclaRY1Q")










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

@views.route("/germannupdate")
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


@views.route("/adbyupdate")
def adbyupdate():
    return createtxtfile("adby" , "PLM-GVlebsoPWZG7j5kRK479fragOS83By")




