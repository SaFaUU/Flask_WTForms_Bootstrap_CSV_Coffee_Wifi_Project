from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, validators
from wtforms.validators import DataRequired
import csv

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)


class CafeForm(FlaskForm):
    cafe = StringField('Cafe name', validators=[DataRequired()])
    submit = SubmitField('Submit')


# Exercise:
# add: Location URL, open time, closing time, coffee rating, wifi rating, power outlet rating fields
# make coffee/wifi/power a select element with choice of 0 to 5.
# e.g. You could use emojis ☕️/💪/✘/🔌
# make all fields required except submit
# use a validator to check that the URL field has a URL entered.
# ---------------------------------------------------------------------------


# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")


class MyForm(FlaskForm):
    cafename = StringField('Cafe Name')
    location = StringField('Location', [validators.data_required(), validators.url()])
    opentime = StringField('Open Time')
    closetime = StringField('Close Time')
    coffee = StringField('Coffee')
    wifi = StringField('Wi-Fi')
    power = StringField('Power')
    submit = SubmitField('submit')


@app.route('/add', methods=['GET', 'POST'])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        print("True")
    # Exercise:
    # Make the form write a new row into cafe-data.csv
    # with   if form.validate_on_submit()
    form = MyForm()
    if request.method == 'POST' and form.validate_on_submit():
        with open("cafe-data.csv", mode="a") as file:
            append_list = []
            # file.write(form)
            for key in form.data.keys():
                append_list.append(form.data[key])
            print(append_list)
            for item in range(0, 7):
                file.write(append_list[item]+',')
            file.write('\n')
    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    with open('cafe-data.csv', newline='', encoding='utf-8') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
    return render_template('cafes.html', cafes=list_of_rows)


if __name__ == '__main__':
    app.run(debug=True)
