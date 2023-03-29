from flask import Flask, render_template

app = Flask(__name__)

DEVICE_TABLE = [
  {
    'Device ID': 'ABCD1234',
    'Name': 'Echo Show 10',
    'Location': 'Office'
  },
  {
    'Device ID': 'ABCD7890',
    'Name': 'Echo Show 8',
    'Location': 'Home'
  }
]

@app.route("/")
def home():
  return render_template('home.html')

@app.route("/devices")
def devices():
  return render_template('devices.html', table=DEVICE_TABLE)



if __name__ == "__main__":
  app.run(host='0.0.0.0', debug=True)