from flask import redirect, Blueprint
from flask_login import login_required

shortlinks = Blueprint('shortlinks', __name__)

#------------------------------------------------------------------------------------------------------


@shortlinks.route("/yt")
def youtube():
    return redirect("https://studio.youtube.com/")


@shortlinks.route("/netflix")
def netflix():
    return redirect("")


@shortlinks.route("/books")
def books():
    return redirect("https://drive.google.com/drive/folders/12OIgF6ceqUP6yxHdaX22fpQfGWvB-5e8?usp=sharing")


@shortlinks.route("/tools")
def tools():
    return redirect("https://github.com/spyisme/spynet/releases/download/ols/Spy.zip")




shortlinks.route("/data")
def final():
    return redirect("https://spysnet.com/static/final.json")
