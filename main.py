from flask import Flask, render_template, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_bootstrap import Bootstrap
STATES = ["Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar", "Jharkhand", "Goa", "Gujrat", "Haryana",
          "Himachal Pradesh", "Chhattisgarh", "Karnataka", "Kerala", "Madhya Pradesh", "Maharashtra", "Manipur",
          "Meghalaya", "Mizoram", "Nagaland", "Odisha", "Punjab", "Rajasthan", "Sikkim", "Tamil Nadu", "Telangana",
          "Tripura", "Uttarakhand", "Uttar Pradesh", "West Bengal", "Andaman & Nicobar Islands", "Chandigarh",
          "Dadra & Nagar Haveli & Daman & Diu", "Delhi", "Jammu & Kashmir", "Ladakh", "Lakshadweep", "Puducherry"]
guessed = []

app = Flask(__name__)
app.config['SECRET_KEY'] = "ddfigrksmgdksxlgdktngkceoutb"
Bootstrap(app)


# WTForm
class StateName(FlaskForm):
    state = StringField("Guess a State/UT name:", validators=[DataRequired()])
    submit = SubmitField("Submit")


@app.route('/', methods=['GET', 'POST'])
def home():
    form = StateName()
    if form.validate_on_submit():
        guess = form.state.data.title()
        if guess in STATES:
            return redirect(url_for('state', guess=guess))
        else:
            flash("wrong guess. Try again.")
    return render_template('index.html', form=form, guessed=guessed, states=STATES)


@app.route('/state/<guess>', methods=['GET', 'POST'])
def state(guess):
    global guessed
    guessed.append(guess)
    form = StateName()
    if form.validate_on_submit():
        guess = form.state.data.title()
        if guess in guessed:
            flash("Already guessed. Try some other state.")
        if guess in STATES:
            return redirect(url_for('state', guess=guess))
        else:
            flash("wrong guess. Try again.")

    if len(guessed) == len(STATES):
        return render_template("welldone.html")

    return render_template('index.html', guessed=guessed, form=form, states=STATES)


@app.route('/remaining', methods=['GET', 'POST'])
def remaining():
    left = []
    for st in STATES:
        if st not in guessed:
            left.append(st)
    return render_template("quit.html", left=left)


if __name__ == "__main__":
    app.run(debug=True)