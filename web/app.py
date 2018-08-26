from flask import Flask, render_template

app = Flask(__name__)

@app.route('/list/<entityName>')
def list(entityName):
    # type: (str) -> str
    return render_template('layout.html', contents=entityName)

@app.route('/')
def index():
    # type: () -> str
    template = render_template('layout.html', content='index')
    return template

