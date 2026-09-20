from flask import Flask, render_template, request, session, redirect
from flask_sqlalchemy import SQLAlchemy
from flask import send_from_directory

app = Flask(__name__)

app.secret_key = "hopehub-secret-key"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///hopehub.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


# =========================
# DATABASE TABLES
# =========================

class HelpRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(200), nullable=False)
    help_type = db.Column(db.String(100), nullable=False)
    contact = db.Column(db.String(20), nullable=False)
    problem = db.Column(db.Text, nullable=False)


class Donation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    contact = db.Column(db.String(20), nullable=False)
    location = db.Column(db.String(200), nullable=False)
    donation_type = db.Column(db.String(200), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)


class Volunteer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    contact = db.Column(db.String(20), nullable=False)
    location = db.Column(db.String(200), nullable=False)
    support = db.Column(db.Text, nullable=False)


with app.app_context():
    db.create_all()


# =========================
# HOME
# =========================

@app.route("/")
def home():
    return render_template("index.html")


# =========================
# REQUEST HELP
# =========================

@app.route("/request-help-page")
def request_help_page():
    return render_template("request_help.html")


@app.route("/request-help", methods=["POST"])
def request_help():

    new_request = HelpRequest(
        name=request.form["name"],
        location=request.form["location"],
        help_type=request.form["help_type"],
        contact=request.form["contact"],
        problem=request.form["problem"]
    )

    db.session.add(new_request)
    db.session.commit()

    return render_template("success.html")


# =========================
# DONATE PAGE
# =========================

@app.route("/donate-page")
def donate_page():
    return render_template("donate.html")


# =========================
# BOOK DONATION
# =========================

@app.route("/donate-books")
def donate_books():
    return render_template("donate_books.html")


@app.route("/donate", methods=["POST"])
def donate():

    new_donation = Donation(
        name=request.form["name"],
        contact=request.form["contact"],
        location=request.form["location"],
        donation_type="Books",
        quantity=request.form["quantity"]
    )

    db.session.add(new_donation)
    db.session.commit()

    return render_template("success.html")


# =========================
# CLOTHES DONATION
# =========================

@app.route("/donate-clothes-page")
def donate_clothes_page():
    return render_template("donate_clothes.html")


@app.route("/donate-clothes", methods=["POST"])
def donate_clothes():

    new_donation = Donation(
        name=request.form["name"],
        contact=request.form["contact"],
        location=request.form["location"],
        donation_type="Clothes",
        quantity=request.form["quantity"]
    )

    db.session.add(new_donation)
    db.session.commit()

    return render_template("success.html")


# =========================
# MEDICINE DONATION
# =========================

@app.route("/donate-medicines-page")
def donate_medicines_page():
    return render_template("donate_medicines.html")


@app.route("/donate-medicines", methods=["POST"])
def donate_medicines():

    medicine = request.form["medicine"]

    new_donation = Donation(
        name=request.form["name"],
        contact=request.form["contact"],
        location=request.form["location"],
        donation_type="Medicine: " + medicine,
        quantity=request.form["quantity"]
    )

    db.session.add(new_donation)
    db.session.commit()

    return render_template("success.html")


# =========================
# FOOD DONATION
# =========================

@app.route("/donate-food-page")
def donate_food_page():
    return render_template("donate_food.html")


@app.route("/donate-food", methods=["POST"])
def donate_food():

    food_type = request.form["food_type"]

    new_donation = Donation(
        name=request.form["name"],
        contact=request.form["contact"],
        location=request.form["location"],
        donation_type="Food: " + food_type,
        quantity=request.form["quantity"]
    )

    db.session.add(new_donation)
    db.session.commit()

    return render_template("success.html")
# =========================
# VOLUNTEER
# =========================

@app.route("/volunteer-page")
def volunteer_page():
    return render_template("volunteer.html")


@app.route("/volunteer", methods=["POST"])
def volunteer():

    new_volunteer = Volunteer(
        name=request.form["name"],
        contact=request.form["contact"],
        location=request.form["location"],
        support=request.form["support"]
    )

    db.session.add(new_volunteer)
    db.session.commit()

    return render_template("success.html")


# =========================
# ADMIN LOGIN
# =========================

@app.route("/admin-login", methods=["GET", "POST"])
def admin_login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        if username == "admin" and password == "1234":
            session["admin_logged_in"] = True
            return redirect("/admin")

        return render_template(
            "admin_login.html",
            error="Invalid username or password"
        )

    return render_template("admin_login.html")


# =========================
# ADMIN DASHBOARD
# =========================

@app.route("/admin")
def admin():

    if not session.get("admin_logged_in"):
        return redirect("/admin-login")

    help_requests = HelpRequest.query.all()
    donations = Donation.query.all()
    volunteers = Volunteer.query.all()

    return render_template(
        "admin.html",
        help_requests=help_requests,
        donations=donations,
        volunteers=volunteers
    )


# =========================
# LOGOUT
# =========================

@app.route("/admin-logout")
def admin_logout():

    session.pop("admin_logged_in", None)
    return redirect("/admin-login")


# =========================
# START SERVER
# =========================

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )

