from flask import Blueprint, render_template, request, redirect, session, flash, url_for
from googleapiclient.discovery import build
import random
import json
import requests
from flask_login import login_user, logout_user, login_required
from .models import User
from werkzeug.security import check_password_hash , generate_password_hash
from . import db
from functools import lru_cache

views = Blueprint('views', __name__)
print('Running!')










@views.route('/all')
def display_links():
    # with open('website/links.txt', 'r') as file:
    #     lines = file.readlines()
    lines = ["nawar", "chem", "gedo","sherbo","salama","sameh", "bio","english"]
    return render_template('used_pages/all.html', lines=lines, teachername="All")





@views.route('/login', methods=['GET', 'POST'])
def login():
  if request.method == 'POST':
    username = request.form.get('username')
    password = request.form.get('password')
    user = User.query.filter_by(username=username).first()

    if user and check_password_hash(user.password, password):
      login_user(user)
      flash('Login successful!', category='success')
      return redirect(url_for('views.home'))
    else:
      flash('Login unsuccessful. Please check your username and password.',
            category='error')

  return render_template('login.html')


# @views.route('/logout')
# @login_required
# def logout():
#   logout_user()
#   return redirect(url_for('views.home'))



# @views.route('/register', methods=['GET', 'POST'])
# def register():
#     if request.method == 'POST':
#         username = request.form.get('username')
#         password = request.form.get('password')
#         hashed_password = generate_password_hash(password, method='scrypt')

#         new_user = User(username=username, password=hashed_password)
#         db.session.add(new_user)
#         db.session.commit()

#         flash('Account created successfully!', category='success')
#         return redirect(url_for('views.home'))

#     return render_template('register.html')

YOUTUBE_API_KEY = 'AIzaSyAbrVMIzmLLhHQSrMVUG8gS3d6IAYE0qVc'


def get_playlist_videos(playlist_id):
    youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY, static_discovery=False)

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

    videos = [{'id': item['snippet']['resourceId']['videoId'], 'title': item['snippet']['title']}
              for item in playlist_items]

    return videos


@views.route("/")
def home():
    return redirect(url_for('views.display_links'))






@views.route('/nawar')
def nawar():
  teacher_links = {
  "Nawar Chapter 1": ("/nawarch1", "Chapter 1"),
    "Nawar Chapter 1 Revision": ("nawarch1rev", "Chapter 1 Revision"),
    "Nawar Chapter 2": ("nawarch2", "Chapter 2"),
    "Nawar Chapter 2 Revision": ("nawarch2rev", "Chapter 2 Revision"),
    "Nawar Chapter 3": ("nawarch3", "Chapter 3"),

    "Nawar Files": ("nawarpdfs", "Google Drive")

  }

  teachername = "Nawar"
  return render_template('used_pages/teacher.html',
                         teacher_links=teacher_links,
                         teachername=teachername,
                         imgs="yes")


@views.route("/nawarch1")
def nawarch1():
  teachername = "Nawar Chapter 1"
  playlist_id = 'PLM-GVlebsoPXpGe3wzMN7SKYvmTr0jACa'
  videos = get_playlist_videos(playlist_id)
  return render_template('used_pages/videopage.html',
                         videos=videos,
                         playlist_id=playlist_id,
                         teachername=teachername)


@views.route("/nawarch1rev")
def nawarch1rev():
  teachername = "Nawar"
  playlist_id = 'PLM-GVlebsoPXELEhVJi-nBm-oZXpE85K2'
  videos = get_playlist_videos(playlist_id)
  return render_template('used_pages/videopage.html',
                         videos=videos,
                         playlist_id=playlist_id,
                         teachername=teachername)
@views.route("/nawarch2rev")
def nawarch2rev():
  teachername = "Nawar"
  playlist_id = 'PLM-GVlebsoPVAd_O1EYC8ORRkYGQ_latH'
  videos = get_playlist_videos(playlist_id)
  return render_template('used_pages/videopage.html',
                         videos=videos,
                         playlist_id=playlist_id,
                         teachername=teachername)

@views.route("/nawarch2")
def nawarch2():
  teachername = "Nawar Chapter 2"
  playlist_id = 'PLM-GVlebsoPWU4v5bcndzPBt6e7PsiCwQ'
  videos = get_playlist_videos(playlist_id)
  # videos += [{'url': '/nawarstorj', 'title': 'More'}]
  return render_template('used_pages/videopage.html',
                         videos=videos,
                         playlist_id=playlist_id,
                         teachername=teachername)

@views.route("/nawarch3")
def nawarch3():
  teachername = "Nawar Chapter 3"
  playlist_id = 'PLM-GVlebsoPXwGQGxiTBmNCzD4E_BgDCo'
  videos = get_playlist_videos(playlist_id)
  return render_template('used_pages/videopage.html',
                         videos=videos,
                         playlist_id=playlist_id,
                         teachername=teachername)

@views.route('/chem')
def chem():
  teacher_links = {
     "Nasser-El-Batal Chapter 1": ("chemch1", "Chapter 1"),
    "Nasser-El-Batal Chapter 2": ("chemch2", "Chapter 2"),
    "Nasser-El-Batal Chapter 3": ("chemch3", "Chapter 3"),
    "Nasser-El-Batal Files": ("chempdfs", "Google Drive")


  }

  teachername = "Nasser-El-Batal"
  return render_template('used_pages/teacher.html',
                         teacher_links=teacher_links,
                         teachername=teachername,
                         imgs="yes")


@views.route("/chemch1")
def chemch1():
  teachername = "Nasser-El-Batal"
  playlist_id = 'PLM-GVlebsoPXWpBDCzn4h0L36UNRYuFb2'
  videos = get_playlist_videos(playlist_id)
  return render_template('used_pages/videopage.html',
                         videos=videos,
                         playlist_id=playlist_id,
                         teachername=teachername)


@views.route("/chemch2")
def chemch2():
    teachername = "Nasser-El-Batal"
    playlist_id = 'PLM-GVlebsoPVYwDkN3DxFcyS1QWCKfAjv'
    videos = get_playlist_videos(playlist_id)
    #return videos
    return render_template('used_pages/videopage.html',
                          videos=videos,
                          playlist_id=playlist_id,
                          teachername=teachername)



@views.route("/chemch2test")
def chemch2test():
    teachername = "Nasser-El-Batal"
    playlist_id = 'PLM-GVlebsoPVYwDkN3DxFcyS1QWCKfAjv'
    videos = get_playlist_videos(playlist_id)
    #return videos
    return render_template('videopagesplits.html',
                          videos=videos,
                          playlist_id=playlist_id,
                          teachername=teachername)
                         
@views.route("/chemch3")
def chemch3():
    teachername = "Nasser-El-Batal"
    playlist_id = 'PLM-GVlebsoPVXmash3q9sfG5bsD3Mt88x'
    videos = get_playlist_videos(playlist_id)
    #videos += [{'url': '/chemstorj', 'title': 'More'}]
    return render_template('used_pages/videopage.html',
                           videos=videos,
                           playlist_id=playlist_id,
                           teachername=teachername)

@views.route('/learn-more')
def learnmore():
  return render_template('backend_pages/more.html')

@views.route('/sherbo')
def sherbo():
  teacher_links = {
    "Sherbo Statics": ("sherbostatics", "Statics"),
    "Sherbo Calculus": ("sherbocalc", "Calculus"),
    "Sherbo Files": ("sherbopdfs", "Google Drive")

  }

  teachername = "Sherbo"
  return render_template('used_pages/teacher.html',
                         teacher_links=teacher_links,
                         teachername=teachername,
                         imgs="yes")


@views.route("/sherbostatics")
def sherbostatics():
  teachername = "Sherbo Statics"
  playlist_id = 'PLM-GVlebsoPX_3mlaOeWIjCPY8jH8MpfJ'
  videos = get_playlist_videos(playlist_id)
  videos += [
    {'url': 'https://iframe.mediadelivery.net/play/33074/5fd08bd7-0920-4685-b99d-7c02b4f45aab', 'title': 'Save mystatics Ch1'},
    {'url': 'https://iframe.mediadelivery.net/play/33074/88e41628-26d6-48fc-a431-064ca36fd253', 'title': 'Save mystatics Ch2Part1'},
    {'url': 'https://iframe.mediadelivery.net/play/33074/e816faf2-2866-4d68-a5f7-9ed5f3002afd', 'title': 'Save mystatics Ch2Part2'},
    {'url': 'https://iframe.mediadelivery.net/play/33074/22808708-26e9-46a6-ba6e-afcdb84a6b31', 'title': 'Save mystatics Ch3Part1'},
    {'url': 'https://iframe.mediadelivery.net/play/33074/bc116916-ad29-47a7-856d-0660ad0e3033', 'title': 'Save mystatics Ch3Part2'},
    {'url': 'https://iframe.mediadelivery.net/play/33074/917ad2d8-f268-46d0-8eb8-c82f3ee48568', 'title': 'Save mystatics Ch4'},
    {'url': 'https://iframe.mediadelivery.net/play/33074/a7f0f898-432f-4b08-a793-0dc942c7fbd8', 'title': 'Save my statics Ch6'}
  ]

  return render_template('used_pages/videopage.html',
                         videos=videos,
                         playlist_id=playlist_id,
                         teachername=teachername)



@views.route("/sherbocalc")
def sherbocalc():
  teachername = "Sherbo Calculus"
  playlist_id = 'PLM-GVlebsoPXrU733HavPf8k-P5h_aFFq'
  videos = get_playlist_videos(playlist_id)
  return render_template('used_pages/videopage.html',
                         videos=videos,
                         playlist_id=playlist_id,
                         teachername=teachername)


@views.route('/sameh')
def sameh():
  teacher_links = {
    "Sameh Nash2t Chapter 1": ("samehh1", "Chapter 1"),
    "Sameh Nash2t Chapter 2": ("samehh2", "Chapter 2"),
    "Sameh Nash2t Chapter 3": ("samehh3", "Chapter 3")

  }

  teachername = "Sameh Nash2t"
  return render_template('used_pages/teacher.html',
                         teacher_links=teacher_links,
                         teachername=teachername,
                         imgs="yes")


@views.route("/samehh1")
def samehh1():
  teachername = "Sameh Nash2t"
  playlist_id = 'PLM-GVlebsoPXd5COr54fuG-1lNCfpDdwl'
  videos = get_playlist_videos(playlist_id)
  return render_template('used_pages/videopage.html',
                         videos=videos,
                         playlist_id=playlist_id,
                         teachername=teachername)


@views.route("/samehh2")
def samehh2():
  teachername = "Sameh Nash2t"
  playlist_id = 'PLM-GVlebsoPUckTjXcvKP483XHykKHH-m'
  videos = get_playlist_videos(playlist_id)
  return render_template('used_pages/videopage.html',
                         videos=videos,
                         playlist_id=playlist_id,
                         teachername=teachername)


@views.route("/samehh3")
def samehh3():
  teachername = "Sameh Nash2t"
  playlist_id = 'PLM-GVlebsoPX1xJ0JSvE7gLfkPEKIo3kA'
  videos = get_playlist_videos(playlist_id)
  return render_template('used_pages/videopage.html',
                         videos=videos,
                         playlist_id=playlist_id,
                         teachername=teachername)
@views.route('/gedo')
def gedo():
  teacher_links = {
    "Gedo": ("gedoo", "Gedo"),
    # Add other entries with the correct structure
}
  teachername = "Gedo"
  return render_template('used_pages/teacher.html',
                         teacher_links=teacher_links,
                         teachername=teachername,
                         imgs="yes")


@views.route("/gedoo")
def gedoo():
  teachername = "Gedo"
  playlist_id = 'PLM-GVlebsoPXBcSNcLjkmcQG53hQYTvui'
  videos = get_playlist_videos(playlist_id)
  #videos += [{'url': '/gedostorj', 'title': 'More'}]

  return render_template('used_pages/videopage.html',
                         videos=videos,
                         playlist_id=playlist_id,
                         teachername=teachername)


@views.route('/bio')
def bio():
  teacher_links = {
      "Chapter 1": ("bioch1", "S2 Not Available"),
    "Chapter 2": ("bioch2", "Chapter 2"),
    "Chapter 3": ("bioch3", "Chapter 3"),


  }

  teachername = "Daif"
  return render_template('used_pages/teacher.html',
                         teacher_links=teacher_links,
                         teachername=teachername,
                         imgs="yes")


@views.route("/bioch1")
def bioch1():
  teachername = "Daif"
  playlist_id = 'PLM-GVlebsoPWYFgg9hks2GaWKC2kI1r7X'
  videos = get_playlist_videos(playlist_id)
  return render_template('used_pages/videopage.html',
                         videos=videos,
                         playlist_id=playlist_id,
                         teachername=teachername)


@views.route("/bioch2")
def bioch2():
  teachername = "Daif"
  playlist_id = 'PLM-GVlebsoPVXxEs5mtOyS-4QLolBXjlX'
  videos = get_playlist_videos(playlist_id)
  return render_template('used_pages/videopage.html',
                         videos=videos,
                         playlist_id=playlist_id,
                         teachername=teachername)

@views.route("/bioch3")
def bioch3():
  teachername = "Daif"
  playlist_id = 'PLM-GVlebsoPV0ylAbm7LFlKCD9_X0CGEK'
  videos = get_playlist_videos(playlist_id)
 # videos += [{'url': '/biostorj', 'title': 'More'}]

  return render_template('used_pages/videopage.html',
                         videos=videos,
                         playlist_id=playlist_id,
                         teachername=teachername)

@views.route("/english")
def english():
  teachername = "English"
  playlist_id = 'PLM-GVlebsoPUWOjoc9DyO2Jh8mclaRY1Q'
  videos = get_playlist_videos(playlist_id)
  return render_template('used_pages/videopage.html',
                         videos=videos,
                         playlist_id=playlist_id,
                         teachername=teachername)


@views.route('/salama')
def salama():
  teacher_links = {
  "PreStudy": ("/salamapre", "PreStudy"),
    "Course 1": ("/salamach1", "Course 1"),
    "Course 2": ("/salamach2", "Course 2"),
    "Course 3": ("/salamach3", "Course 3"),
    "Course 4": ("/salamach4", "Course 4"),
    "Course 5": ("/salamach5", "Course 5"),
    "Course 6 (Revision)": ("/salamach6", "Course 6 (Revision)"),
    "Course 7": ("/salamach7", "Course 7"),
    "Course 8": ("/salamach8", "Course 8"),
    "Course 9": ("/salamach9", "Course 9"),
    "Course 10": ("/salamach10", "Course 10"),
    "Course 11": ("/salamach11", "S21 not available"),
    "Course 12": ("/salamach12", "Course 12 "),
    "Course 13": ("/salamach13", "Course 13"),
    "Course 14": ("/salamach14", "Course 14"),
    "Course 15": ("/salamach15", "Course 15")



  }
  teachername = "Mohamed Salama"
  return render_template('used_pages/teacher.html',
                         teacher_links=teacher_links,
                         teachername=teachername,
                         imgs="yes")


@views.route("/salamapre")
def salamapre():
  teachername = "Mohamed Salama PreStudy"
  playlist_id = 'PLM-GVlebsoPVEULTnn90gqVL0AL99KtU0'
  videos = get_playlist_videos(playlist_id)
  return render_template('used_pages/videopage.html',
                         videos=videos,
                         playlist_id=playlist_id,
                         teachername=teachername)


@views.route("/salamach1")
def salamach1():
  teachername = "Mohamed Salama Course 1"
  playlist_id = 'PLM-GVlebsoPWfuCf4h_ucKPOBKjH6No-W'
  videos = get_playlist_videos(playlist_id)
  return render_template('used_pages/videopage.html',
                         videos=videos,
                         playlist_id=playlist_id,
                         teachername=teachername)


@views.route("/salamach2")
def salamach2():
  teachername = "Mohamed Salama Course 2"
  playlist_id = 'PLM-GVlebsoPUubsCYnPGc27tihI0pz4hi'
  videos = get_playlist_videos(playlist_id)
  return render_template('used_pages/videopage.html',
                         videos=videos,
                         playlist_id=playlist_id,
                         teachername=teachername)


@views.route("/salamach3")
def salamach3():
  teachername = "Mohamed Salama Course 3"
  playlist_id = 'PLM-GVlebsoPUSSsoABHH059FBapcSjvGg'
  videos = get_playlist_videos(playlist_id)
  return render_template('used_pages/videopage.html',
                         videos=videos,
                         playlist_id=playlist_id,
                         teachername=teachername)


@views.route("/salamach4")
def salamach4():
  teachername = "Mohamed Salama Course 4"
  playlist_id = 'PLM-GVlebsoPXWSZDCjeDfvdMV5QXYwg4x'
  videos = get_playlist_videos(playlist_id)
  return render_template('used_pages/videopage.html',
                         videos=videos,
                         playlist_id=playlist_id,
                         teachername=teachername)


@views.route("/salamach5")
def salamach5():
  teachername = "Mohamed Salama Course 5"
  playlist_id = 'PLM-GVlebsoPWEGxQu5D0hVrUCJjTMqYvd'
  videos = get_playlist_videos(playlist_id)
  return render_template('used_pages/videopage.html',
                         videos=videos,
                         playlist_id=playlist_id,
                         teachername=teachername)


@views.route("/salamach6")
def salamach6():
  teachername = "Mohamed Salama Course 6"
  playlist_id = 'PLM-GVlebsoPWZKrvX8MvfJxfxXhKXvqR3'
  videos = get_playlist_videos(playlist_id)
  return render_template('used_pages/videopage.html',
                         videos=videos,
                         playlist_id=playlist_id,
                         teachername=teachername)


@views.route("/salamach7")
def salamach7():
  teachername = "Mohamed Salama"
  playlist_id = 'PLM-GVlebsoPUobUeuNIWsitKeP-aHOwif'
  videos = get_playlist_videos(playlist_id)
  return render_template('used_pages/videopage.html',
                         videos=videos,
                         playlist_id=playlist_id,
                         teachername=teachername)


@views.route("/salamach8")
def salamach8():
  teachername = "Mohamed Salama Course 8"
  playlist_id = 'PLM-GVlebsoPUqwS3-Ij-pHBq4_aoEAwMZ'
  videos = get_playlist_videos(playlist_id)
  return render_template('used_pages/videopage.html',
                         videos=videos,
                         playlist_id=playlist_id,
                         teachername=teachername)


@views.route("/salamach9")
def salamach9():
  teachername = "Mohamed Salama Course 9"
  playlist_id = 'PLM-GVlebsoPXe2kZo_cM06BZWXwdSxQ7B'
  videos = get_playlist_videos(playlist_id)
  return render_template('used_pages/videopage.html',
                         videos=videos,
                         playlist_id=playlist_id,
                         teachername=teachername)




@views.route("/salamach10")
def salamach10():
  teachername = "Mohamed Salama Course 10"
  playlist_id = 'PLM-GVlebsoPXZmghd3uMqZWx6wlLZDiiu'
  videos = get_playlist_videos(playlist_id)
  return render_template('used_pages/videopage.html',
                         videos=videos,
                         playlist_id=playlist_id,
                         teachername=teachername)



@views.route("/salamach11")
def salamach11():
  teachername = "Mohamed Salama Course 11"
  playlist_id = 'PLM-GVlebsoPVB0u2fWqO9ep3cuBp_8zTW'
  videos = get_playlist_videos(playlist_id)
 # videos += [{'url': '/salamastorj', 'title': 'More'}]

  return render_template('used_pages/videopage.html',
                         videos=videos,
                         playlist_id=playlist_id,
                         teachername=teachername)


@views.route("/salamach12")
def salamach12():
  teachername = "Mohamed Salama Course 12"
  playlist_id = 'PLM-GVlebsoPU0BwzCsqsPQfKMSPZauuFl'
  videos = get_playlist_videos(playlist_id)
 # videos += [{'url': '/salamastorj', 'title': 'More'}]

  return render_template('used_pages/videopage.html',
                         videos=videos,
                         playlist_id=playlist_id,
                         teachername=teachername)

@views.route("/salamach13")
def salamach13():
  teachername = "Mohamed Salama Course 13"
  playlist_id = 'PLM-GVlebsoPURAU8nu_tU2dphnGXxZeMM'
  videos = get_playlist_videos(playlist_id)
 # videos += [{'url': '/salamastorj', 'title': 'More'}]

  return render_template('used_pages/videopage.html',
                         videos=videos,
                         playlist_id=playlist_id,
                         teachername=teachername)
@views.route("/salamach14")
def salamach14():
  teachername = "Mohamed Salama Course 14"
  playlist_id = 'PLM-GVlebsoPXnRQBjkDqUUAXDKyUJqK9-'
  videos = get_playlist_videos(playlist_id)
 # videos += [{'url': '/salamastorj', 'title': 'More'}]

  return render_template('used_pages/videopage.html',
                         videos=videos,
                         playlist_id=playlist_id,
                         teachername=teachername)
@views.route("/salamach15")
def salamach15():
  teachername = "Mohamed Salama Course 15"
  playlist_id = 'PLM-GVlebsoPWCqnSBAANAy8Wn89lbLmqt'
  videos = get_playlist_videos(playlist_id)

  return render_template('used_pages/videopage.html',
                         videos=videos,
                         playlist_id=playlist_id,
                         teachername=teachername)



@views.route('/iframes', methods=['GET', 'POST'])
def sherboframe():
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
        if "youtube" in url.lower(): 
            url = url.split('/')[4]

            msg = f'```python youtube.py {url} {name}``` {name}'
        else: 
            msg = f'```python iframe.py {url} {name}``` {name}'
        message = {
                'content': f'{msg}'
            }
        payload = json.dumps(message)
        headers = {'Content-Type': 'application/json'}
        requests.post(webhook_url, data=payload, headers=headers)
        return "Message Sent!" 
    return render_template('backend_pages/iframe.html' , url = url , sname= sname)




@views.route("/test")
def test():
  return render_template('test_pages/videoplayer.html' )