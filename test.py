from server import Server, redirect, render_template, session, req
from mysql import connector

db = connector.connect(
    host="localhost",
    user="root",
    passwd="",
    database="website"
)

cur = db.cursor()

http = Server()
http.info = True


def logged():
    if session.get("logged"):
        return True
    return False


@http.path("/")
def index():
    cur.execute("SELECT urldecoder(name), urldecoder(descr) FROM gifts")
    res = cur.fetchall()
    if len(res) < 1:
        return render_template("index.html", logged=logged())
    else:
        gifts = []
        for r in res:
            gifts.append("{}: {}".format(r[0], r[1]))
        cur.reset()
        return render_template("index.html", gifts=gifts, logged=logged())


@http.path("/<str:testt>")
def test(testt):
    return testt


@http.path("/gift")
def gift():
    if req.method == "GET":
        return render_template("gift.html", logged=logged())
    elif req.method == "POST":
        if req.post["name"] == "" or req.post["desc"] == "":
            return render_template("gift.html", error="All fields must be filled", logged=logged())
        elif len(req.post["name"]) < 5 or len(req.post["desc"]) < 5:
            return render_template("gift.html", error="Field length must be above 5 characters.",
                                   logged=logged())
        elif len(req.post["name"]) > 30:
            return render_template("gift.html", error="Username cannot be more than 15 characters.", logged=logged())
        else:
            name = req.post["name"]
            desc = req.post["desc"]
            cur.execute("INSERT INTO gifts (id, name, descr) VALUES (NULL, %s, %s)",
                        (name.replace("+", " "), desc.replace("+", " ")))
            db.commit()
            cur.reset()
            return render_template("gift.html", error="Gift sent.", logged=logged())


@http.path("/login")
def login():
    if req.method == "GET":
        return render_template("login.html", logged=logged())
    elif req.method == "POST":
        if req.post["username"] == "" or req.post["password"] == "":
            return render_template("login.html", error="All fields must be filled.", logged=logged())
        elif len(req.post["username"]) < 5 or len(req.post["password"]) < 5:
            return render_template("login.html", error="Field length must be above 5 characters.",
                                   logged=logged())
        elif len(req.post["username"]) > 15:
            return render_template("login.html", error="Username cannot be more than 15 characters.",
                                   logged=logged())
        else:
            username = req.post["username"]
            password = req.post["password"]
            cur.execute(
                "SELECT id, urldecoder(username) FROM users WHERE username = '{}' AND password = '{}'".format(username,
                                                                                                              password))
            res = cur.fetchall()
            cur.reset()
            if len(res) < 1:
                return render_template("login.html", error="Wrong username/password.", logged=logged())
            else:
                db_id = str(res[0][0])
                db_username = res[0][1]
                session.put("logged", True)
                session.put("username", db_username)
                session.put("id", db_id)
                return redirect("/")


@http.path("/register")
def register():
    if req.method == "GET":
        return render_template("login.html", logged=logged())
    elif req.method == "POST":
        if req.post["username"] == "" or req.post["password"] == "":
            return render_template("login.html", error="All fields must be filled", logged=logged())
        elif len(req.post["username"]) < 5 or len(req.post["password"]) < 5:
            return render_template("login.html", error="Field length must be above 5 characters.",
                                   logged=logged())
        elif len(req.post["username"]) > 15:
            return render_template("login.html", error="Username cannot be more than 15 characters.",
                                   logged=logged())
        else:
            username = req.post["username"]
            password = req.post["password"]
            cur.execute("INSERT INTO users (id, username, password) VALUES (NULL, %s, %s)",
                        (username.replace("+", " "), password.replace("+", " ")))
            db.commit()
            cur.reset()
            return render_template("login.html", error="You've created account successfully.", logged=logged())


@http.path("/logout")
def logout():
    session.clear()
    return redirect("/")


http.start()
