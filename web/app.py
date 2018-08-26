from flask import Flask, render_template, url_for, redirect
from pony.flask import Pony

from spanf.entity_classes import EntityClasses, select

app = Flask(__name__)
Pony(app)


def getNavigation():
    # type: () -> dict

    navigation = {}
    for entityName in EntityClasses.getAllClassNames():
        navigation[url_for('list', entityName=entityName)] = entityName

    return navigation


def renderInLayout(templateFileName, **context):
    return render_template(
        templateFileName,
        navigation=getNavigation(),
        **context
    )


@app.route('/list/<entityName>')
def list(entityName):
    # type: (str) -> str
    return renderInLayout(
        'page/datagrid.html',
        entities=select(entity for entity in EntityClasses.getClassByName(entityName))[:]
    )


@app.route('/')
def index():
    # type: () -> str
    return redirect(getNavigation().keys()[0])
