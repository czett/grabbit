from flask import Flask, render_template, redirect, session, request, url_for
import funcs

app = Flask(__name__)
app.secret_key = "wlfuiqhwelfiuwehfliwuehfwhevfjkhvgrlidzuf"

def check_login_status():
    if session.get("logged_in"):
        if session["logged_in"]:
            return True
    else:
        session["logged_in"] = False
        return False
    
    return True

@app.route("/")
def startpoint():
    return render_template("index.html", session=session)

@app.route("/login")
def login():    
    return render_template("logreg.html", action="login", msg=None, session=session)

@app.route("/login/process", methods=["POST"])
def process_login():    
    try:
        username = request.form["username"]
        password = request.form["password"]

        if username and password:
            response = funcs.login(username, password)
            if response[0] == True:
                session["user"] = username
                session["logged_in"] = True
                return redirect("/")
            else:
                return render_template("logreg.html", action="login", msg=response[1], session=session)
    except:
        return redirect("/")

    return "Congrats, you worked around my code :)"

@app.route("/register")
def register():    
    return render_template("logreg.html", action="register", msg=None, session=session)

@app.route("/register/process", methods=["POST"])
def process_register():    
    try:
        username = request.form["username"]
        password = request.form["password"]

        if username and password:
            response = funcs.register(username, password)
            if response[0] == True:
                session["user"] = username
                session["logged_in"] = True
                return redirect("/")
            else:
                return render_template("logreg.html", action="register", msg=response[1], session=session)
    except:
        return redirect("/")
    
    return "Congrats, you worked around my code :)"

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route("/profile/<int:pid>")
def profile(pid):
    # if not funcs.check_user_exists(pid):
    #     return redirect("/")

    pid = int(pid)
    
    #ratings = funcs.get_user_ratings(pid)
    uname = funcs.get_username_by_user_id(pid)

    #user_achievements = funcs.get_achievements_by_user_id(pid)[1]

    # return str(ratings)

    # Calculate the average latitude and longitude for all rated toilets
    # if ratings != []:
    #     avg_lat = sum(rating['latitude'] for rating in ratings) / len(ratings)
    #     avg_lon = sum(rating['longitude'] for rating in ratings) / len(ratings)
    # else:
    #     # Default center if no ratings
    #     avg_lat, avg_lon = 51.505, -0.09 # default is uk or so

    if session.get("user"):
        if session["user"] == uname:
            own = True
        else:
            own = False

    # return nots as list of notifications, as of now list of dicts
    if uname == session["user"]:
        if session.get("notifications"):
            nots = session["notifications"]
        else:
            nots = []
    else:
        nots = []

    return render_template("profile.html", ratings=[], session=session, name=uname, own=own)

@app.route("/profile/<username>")
def profile_by_username(username):
    # Fetch the user ID using the username
    user_id = funcs.get_user_id_by_username(username)
    
    if not user_id:
        return redirect("/")  # Redirect to homepage if username does not exist
    
    # Redirect to the original profile route with user ID
    return redirect(url_for('profile', pid=user_id))

@app.route("/myprofile")
def my_profile():
    if not check_login_status():
        return redirect("/")
    
    username = session["user"]
    return redirect(f"/profile/{username}")

@app.route("/post")
def post():
    if not check_login_status():
        return redirect("/")

    return render_template("get_location.html", session=session)

@app.route("/post/process", methods=["POST"])
def process_rating():
    if not check_login_status():
        return redirect("/")

    query = request.form["location_query"]
    lat, lng = funcs.get_coordinates(query)

    session["coords"] = (lat, lng)
    departments = ["Backtheke", "Milchwaren", "Süßes", "Obst & Gemüse", "Fleisch", "Getränke", "Alkohol", "Tiefkühlwaren", "Sushi", "Snacks"]

    return render_template("post.html", lat=lat, lng=lng, msg=None, session=session, departments=departments)

@app.route("/post/finish", methods=["POST"])
def finish_purchase():
    if not check_login_status():
        return redirect("/")

    paid_price = request.form.get("paid")
    usual_price = request.form.get("usual")
    departments = request.form.getlist("department")
    comment = request.form.get("comment")
    user = session["user"]
    coords = session.get("coords")

    if not (paid_price and usual_price and coords):
        return render_template("post.html", msg="Bitte fülle alle Pflichtfelder aus.", session=session)

    response = funcs.post_purchase(
        paid_price=float(paid_price),
        usual_price=float(usual_price),
        departments=departments,
        comment=comment or "",
        coords=coords,
        user=user,
    )
    
    if response[0]:
        return redirect("/")
    else:
        return render_template("post.html", msg=response[1], session=session)

if __name__ == "__main__":
    app.run(debug=True, port=6500)