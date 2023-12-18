from flask import Flask, render_template
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, URL
import json
import os

app = Flask(__name__)
# use a custom string instead of os.environ.get("APPKEY")
app.secret_key = os.environ.get("APPKEY")
bs = Bootstrap5(app)


class CafeForm(FlaskForm):
    cafe_name = StringField('Cafe name', validators=[DataRequired()])
    location_url = StringField("Location URL", validators=[DataRequired(), URL()])
    open_time = StringField('Opening Time', validators=[DataRequired()])
    close_time = StringField('Closing Time', validators=[DataRequired()])
    coffee_rating = SelectField("Coffee Rating", validators=[DataRequired()], choices=["✘", "☕️", "☕️☕️", "☕️☕️☕️", "☕️☕️☕️☕️", "☕️☕️☕️☕️☕️"])
    wifi_rating = SelectField("WiFi Rating", validators=[DataRequired()], choices=["✘", "💪", "💪💪", "💪💪💪", "💪💪💪💪", "💪💪💪💪💪"])
    power_rating = SelectField("Power outlet Rating", validators=[DataRequired()], choices=["✘", "🔌", "🔌🔌", "🔌🔌🔌", "🔌🔌🔌🔌", "🔌🔌🔌🔌🔌"])   
    submit = SubmitField('Submit')

@app.route("/")
def home():
    return render_template("index.html")

@app.route('/add', methods=["GET", "POST"])
def add_cafe():
    form = CafeForm()
    form_data = {}
    if form.validate_on_submit():
        form_data["Cafe Name"] = form.cafe_name.data
        form_data["Location"] = form.location_url.data
        form_data["Open"] = form.open_time.data
        form_data["Close"] = form.close_time.data
        form_data["Coffee"] = form.coffee_rating.data
        form_data["Wifi"] = form.wifi_rating.data
        form_data["Power"] = form.power_rating.data
        with open("cafedata.json", "r") as fd:
        	data = json.load(fd)
        	data.append(form_data)
        with open("cafedata.json", "w") as fd:
        	json.dump(data, fd, indent=4)
        return render_template("index.html")
    return render_template('add.html', form=form)

@app.route('/cafes')
def cafes():
	with open("cafedata.json", "r") as fd:
		cafe_list = json.load(fd)
	return render_template('cafes.html', cafes=cafe_list)

if __name__ == '__main__':
    app.run(debug=True)
