import os

from flask import Flask
from flask import render_template

from redheads.graphql import GraphQL
from redheads.analyzer import Analyzer

app = Flask(__name__)


@app.route('/capture')
def capture():
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "config/cloud_credentials.json"
    return render_template('capture.html')


@app.route('/products')
def get_graphql_products():
    return str(GraphQL.get_products())


@app.route('/checkout/<path:target>')
def create_checkout(target):
    return str(GraphQL.create_checkout(target))


@app.route('/images/<id>', methods=["GET"])
def images(id):
    file_path = "images/" + id + ".png"
    analyzer = Analyzer(file_path)

    color = analyzer.analyze()

    return GraphQL.create_checkout(color)['data']['checkoutCreate']['checkout']['webUrl']


if __name__ == '__main__':
    # This is used when running locally. Gunicorn is used to run the
    # application on Google App Engine. See entrypoint in app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
