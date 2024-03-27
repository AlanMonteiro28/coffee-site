from flask import Flask, render_template
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, URL
import csv

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
app.config['SECRET_KEY'] = 'YOUR SECRET KEY'
Bootstrap5(app)


class CafeForm(FlaskForm):
    cafe = StringField(label='Cafe name', validators=[DataRequired()])
    location = StringField(label='Cafe Location on Google Maps (URL)', validators=[DataRequired(),
                                                                                   URL(message='Invalid URL')])
    open_time = StringField(label='Opening Time e.g. 8 AM', validators=[DataRequired()])
    close_time = StringField(label='Closing Time e.g. 6:30 PM', validators=[DataRequired()])
    rating = SelectField(label='Coffee Rating',
                         choices=[('☕️'*i) for i in range(1, 6)],
                         validators=[DataRequired()])
    wifi = SelectField(label='Wifi Strenght Rating', 
                       choices=[('✘') if i == 0 else ('💪'*i) for i in range(0, 6)],
                       validators=[DataRequired()])
    power = SelectField(label='Power Socket ', 
                        choices=[('✘') if i == 0 else ('🔌'*i) for i in range(0, 6)],
                        validators=[DataRequired()])
    submit = SubmitField('Submit')


@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=['GET', 'POST'])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        with open('cafe-data.csv', mode='a', encoding='utf-8', newline='') as file:
            data = csv.writer(file)
            data.writerow([form.cafe.data, form.location.data, form.open_time.data,
                             form.close_time.data, form.rating.data, form.wifi.data, form.power.data])
        return render_template('add.html', form=form)
    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    with open('cafe-data.csv', newline='', encoding='utf-8') as csv_file:
        csv_data = csv.reader(csv_file)
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
    return render_template('cafes.html', cafes=list_of_rows)


if __name__ == '__main__':
    app.run(debug=True)
