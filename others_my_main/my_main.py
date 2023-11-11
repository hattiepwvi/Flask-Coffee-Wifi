from flask import Flask, render_template,request
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import csv
import os

'''
Red underlines? Install the required packages first: 
Open the Terminal in PyCharm (bottom left). 

On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from requirements.txt for this project.
'''




app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)


class CafeForm(FlaskForm):
    cafe = StringField('Cafe name', validators=[DataRequired()])
    cafe_location = StringField('Cafe Location on Google Maps (URL)', validators=[DataRequired()])
    cafe_start_time = StringField('Cafe Time e.g. 8AM', validators=[DataRequired()])
    cafe_end_time = StringField('Cafe Time e.g. 5PM', validators=[DataRequired()])
    cafe_rating = StringField('Cafe Rating', validators=[DataRequired()])
    wifi_rating = StringField('Wifi Strength Rating', validators=[DataRequired()])
    power = StringField('Power Socket Availability', validators=[DataRequired()])
    submit = SubmitField('Submit')

# Exercise:
# add: Location URL, open time, closing time, coffee rating, wifi rating, power outlet rating fields
# make coffee/wifi/power a select element with choice of 0 to 5.
#e.g. You could use emojis ☕️/💪/✘/🔌
# make all fields required except submit
# use a validator to check that the URL field has a URL entered.
# ---------------------------------------------------------------------------


# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=['POST'])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        print("True")
        if request.method == 'POST':
            form_data = {
                'cafe': request.form.get('cafe'),
                'cafe_location': request.form.get('cafe_location'),
                'cafe_start_time': request.form.get('cafe_start_time'),
                'cafe_end_time': request.form.get('cafe_end_time'),
                'cafe_rating': request.form.get('cafe_rating'),
                'wifi_rating': request.form.get('wifi_rating'),
                'power': request.form.get('power'),

            }
            write_to_csv(form_data)
    # Exercise:
    # Make the form write a new row into cafe-data.csv
    # with   if form.validate_on_submit()
    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    with open('../cafe-data.csv', newline='', encoding='utf-8') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
        print(list_of_rows)
    return render_template('cafes.html', cafes=list_of_rows)


def write_to_csv(data):
    csv_file_path = 'form_data.csv'

    # Check if the CSV file already exists, and create headers if it's a new file
    is_new_file = not os.path.isfile(csv_file_path)

    with open(csv_file_path, mode='a', newline='') as file:
        fieldnames = list(data.keys())
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        if is_new_file:
            writer.writeheader()

        writer.writerow(data)


if __name__ == '__main__':
    app.run(debug=True)
