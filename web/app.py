import re

from flask import Flask, render_template, url_for, redirect, request, Response, abort
from pony.flask import Pony
from pony.orm import ObjectNotFound, flush
from werkzeug.exceptions import MethodNotAllowed, NotFound, BadRequest

from spanf.entities import db, Data
from spanf.entity_classes import EntityClasses, select
from spanf.entity_factory import EntityFactory
from spanf.no_child_entities_found import NoChildEntitiesFound

app = Flask(__name__)
Pony(app)


def getNavigation():
    # type: () -> dict
    navigation = {}
    for entityName in EntityClasses.getAllClassNames():
        navigation[url_for('listEntities', entityName=entityName)] = entityName

    return navigation


def renderInLayout(templateFileName, **context):
    # type: (str, **object) -> Response
    return render_template(
        templateFileName,
        navigation=getNavigation(),
        request=request,
        **context
    )


# Routes
@app.route('/<string:entityName>')
def listEntities(entityName):
    # type: (str) -> Response
    kwargs={
        'entities': select(entity for entity in EntityClasses.getClassByName(entityName))[:],
        'entityName': entityName,
    }
    if entityName == 'Data':
        kwargs['downloadLink'] = url_for('downloadRawData', dataId=0).replace('0', '%d')

    return renderInLayout('page/datagrid.html', **kwargs)


@app.route('/<string:entityName>/<int:entityId>', methods=['GET', 'POST', 'DELETE'])
def detail(entityName, entityId):
    # type: (str, int) -> Response
    try:
        entity = EntityClasses.getClassByName(entityName)[entityId]
    except ObjectNotFound as e:
        if entityId != 0:
            raise NotFound(description='Entity not found: %s' % e.message)
        try:
            entity = EntityFactory.build(entityName)
            flush()
        except NotImplementedError:
            raise MethodNotAllowed(description='Manual entity creation not allowed for this entity')
        except NoChildEntitiesFound as e:
            raise BadRequest(description=e.message)

    if request.method == 'DELETE':
        entity.delete()
        return Response('Entity successfully removed')

    if request.method == 'POST':
        nullableFieldNames = entity.getNullableFieldClass().keys()
        for fieldName, fieldValue in request.form.iteritems():
            if fieldName in nullableFieldNames and len(fieldValue) == 0:
                fieldValue = None
            setattr(entity, fieldName, fieldValue)

    return renderInLayout(
        'page/detail.html',
        entity=entity,
        entityName=entityName,
        goBackLink=url_for('listEntities', entityName=entityName),
        formProcessLink=url_for('detail', entityName=entityName, entityId=entity.id)
    )


@app.route('/downloadData/<int:dataId>')
def downloadRawData(dataId):
    # type: (int) -> Response
    try:
        data = Data[dataId]
    except ObjectNotFound as e:
        raise NotFound(description='Entity not found: %s' % e.message)

    return Response(
        data.content,
        mimetype=data.dataFormat.mimeType,
    )


@app.route('/')
def index():
    # type: () -> Response
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


@app.template_filter('pascalCaseToPretty')
def pascalCaseToPretty(input):
    # type: (str) -> str
    return ' '.join(re.findall('([A-Z]?[^A-Z]+)', input)).capitalize()


@app.template_filter('newEntityLink')
def getNewEntityLink(entityName):
    # type: (str) -> str
    return url_for('detail', entityName=entityName, entityId=0)
