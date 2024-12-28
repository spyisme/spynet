from flask import redirect, Blueprint , redirect , abort , request , render_template
import json
from flask_login import current_user
shortlinks = Blueprint('shortlinks', __name__)

#------------------------------------------------------------------------------------------------------


@shortlinks.route("/yt")
def youtube():
    return redirect("https://studio.youtube.com/")


@shortlinks.route("/tools")
def tools():
    return redirect("https://github.com/spyisme/new/releases/download/new/Spy.zip")


@shortlinks.route("/books")
def books():
    return redirect("https://drive.google.com/drive/folders/12OIgF6ceqUP6yxHdaX22fpQfGWvB-5e8?usp=sharing")

#------------------------------------------------------------------------------------------------------
@shortlinks.route("/<key>")
def shorturl(key):
    try :
        with open('website/Backend/shortlinks/shortlinks.json', 'r') as f:
            shortlinks = json.load(f)
            url= shortlinks.get(key)
        if url :
            return redirect(url)
        else : 
            return abort(404)
    except:
         return abort(404)

@shortlinks.route("/desktop/<key>", methods=["GET", "POST"])
def desktop(key):
    headers = dict(request.headers)
    print(headers)
    full_url = request.url
    print(full_url)
    print(key)
    return ""
#Short links manage--------------------------------------------------------------------------------------
def load_shortlinks():
    with open('website/Backend/shortlinks/shortlinks.json', 'r') as f:
        return json.load(f)
    return {}


def save_shortlinks(shortlinks):
    with open('website/Backend/shortlinks/shortlinks.json', 'w') as f:
        json.dump(shortlinks, f, indent=4)

@shortlinks.route("/shortlinks/manage", methods=["GET", "POST"])
def shortlinks_manage_urls():
    if current_user.username != 'spy':
        return abort(404)
    if request.method == "POST":

        action = request.form.get("action")
        key = request.form.get("key")
        url = request.form.get("url")
        
        shortlinks = load_shortlinks()

        if action == "add" and key and url:
            shortlinks[key] = url
            save_shortlinks(shortlinks)
        elif action == "delete" and key:
            if key in shortlinks:
                del shortlinks[key]
                save_shortlinks(shortlinks)

    shortlinks = load_shortlinks()
    return render_template('admin/shortlinks.html', shortlinks=shortlinks)


