from flask import Flask
from openaq import OpenAQ
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = OpenAQ()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
DB = SQLAlchemy(app)

class Record(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    datetime = DB.Column(DB.String(25))
    value = DB.Column(DB.Float, nullable=False)

    def __repr__(self):
        return 'Record {} {}'.format(self.datetime, self.value)

@app.route('/')
def root():
    data = Record.query.filter(Record.value>=10).all()
    return str(data)

@app.route('/refresh')
def refresh():
    """Pull fresh data from Open AQ and replace existing data."""
    DB.drop_all()
    DB.create_all()
    data = api.measurements(city='Los Angeles', parameter='pm25')
    for entry in data[1]['results']:
        record = Record(datetime=(str(entry['date']['utc'])), value=entry['value'])
        DB.session.add(record)
    DB.session.commit()
    return 'Data refreshed!'