from flask import Flask, render_template, url_for, redirect, request, Response
from pony.flask import Pony

from spanf.entities import db, Data
from spanf.entity_classes import EntityClasses, select

app = Flask(__name__)
Pony(app)


def getNavigation():
    # type: () -> dict
    navigation = {}
    for entityName in EntityClasses.getAllClassNames():
        navigation[url_for('listEntities', entityName=entityName)] = entityName

    return navigation


def renderInLayout(templateFileName, **context):
    return render_template(
        templateFileName,
        navigation=getNavigation(),
        **context
    )


# Routes
@app.route('/<string:entityName>')
def listEntities(entityName):
    # type: (str) -> str
    kwargs={
        'entities': select(entity for entity in EntityClasses.getClassByName(entityName))[:],
        'entityName': entityName,
    }
    if entityName == 'Data':
        kwargs['downloadLink'] = url_for('downloadRawData', dataId=0).replace('0', '%d')

    return renderInLayout('page/datagrid.html', **kwargs)


@app.route('/<string:entityName>/<int:entityId>', methods=['GET', 'POST'])
def detail(entityName, entityId):
    # type: (str, int) -> str
    entity = EntityClasses.getClassByName(entityName)[entityId]

    if request.method == 'POST':
        nullableFieldNames = entity.getNullableFieldClass().keys()
        for fieldName, fieldValue in request.form.iteritems():
            if fieldName in nullableFieldNames and len(fieldValue) == 0:
                fieldValue = None
            setattr(entity, fieldName, fieldValue)

    return renderInLayout('page/detail.html', entity=entity, request=request, entityName=entityName)


@app.route('/downloadData/<int:dataId>')
def downloadRawData(dataId):
    data = Data[dataId]
    return Response(
        data.content,
        mimetype=data.dataFormat.mimeType,
    )


@app.route('/')
def index():
    # type: () -> str
    return redirect(getNavigation().keys()[0])


# Template filters
@app.template_filter('isEntity')
def isEntity(object):
    # type: (object) -> bool
    return isinstance(object, db.Entity)


@app.template_filter('entityLink')
def getEntityLink(entity):
    # type: (db.Entity) -> str
    return url_for('detail', entityName=entity.__class__.__name__, entityId=entity.id)