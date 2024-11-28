from flask import Flask, render_template, redirect, session, request
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

if __name__ == "__main__":
    app.run(debug=True, port=6500)