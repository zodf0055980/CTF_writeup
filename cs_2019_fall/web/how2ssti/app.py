from flask import Flask, request, render_template, redirect, url_for, session, render_template_string
import os

app = Flask(__name__)

def magic(str):
    return str.replace(".", "").replace("_", "").replace("{{", "")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/ssti')
def ssti():
    content = request.args.get("payload")
    return render_template_string("OK... Here is your ssti result: " + magic(content))

if __name__ == "__main__":
    app.run(threaded=True, ssl_context='adhoc')
