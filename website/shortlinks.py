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
@shortlinks.route("/short/<key>")
def shorturl(key):
    try :
        with open('website/Backend/shortlinks.json', 'r') as f:
            shortlinks = json.load(f)
            url= shortlinks.get(key)
        if url :
            return redirect(url)
    except:
        return jsonify({"error": "URL not found"}), 404





