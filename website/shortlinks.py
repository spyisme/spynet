from flask import redirect, Blueprint , jsonify , request, redirect , render_template
import json

shortlinks = Blueprint('shortlinks', __name__)

#------------------------------------------------------------------------------------------------------


@shortlinks.route("/yt")
def youtube():
    return redirect("https://studio.youtube.com/")


@shortlinks.route("/tools")
def tools():
    return redirect("https://github.com/spyisme/spynet/releases/download/ols/Spy.zip")


@shortlinks.route("/books")
def books():
    return redirect("https://drive.google.com/drive/folders/12OIgF6ceqUP6yxHdaX22fpQfGWvB-5e8?usp=sharing")

#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
shortlinks_file = 'website/Backend/shortlinks.json'

def load_shortlinks():
    with open(shortlinks_file, 'r') as f:
        return json.load(f)
    return {}


def save_shortlinks(shortlinks):
    with open(shortlinks_file, 'w') as f:
        json.dump(shortlinks, f, indent=4)

@shortlinks.route("/short/manage", methods=["GET", "POST"])
def manage_urls():
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
    return render_template('admin/shortlink.html', shortlinks=shortlinks)

@shortlinks.route("/short/<key>")
def shorturl(key):
    try :
        with open('Backend/shortlinks.json', 'r') as f:
            shortlinks = json.load(f)
            url= shortlinks.get(key)
        if url :
            return redirect(url)
    except:
        return jsonify({"error": "URL not found"}), 404





