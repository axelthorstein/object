from flask import Flask
from flask import render_template


app = Flask(__name__)


@app.route('/capture')
def capture():
    return render_template('capture.html')


if __name__ == '__main__':
    # This is used when running locally. Gunicorn is used to run the
    # application on Google App Engine. See entrypoint in app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
