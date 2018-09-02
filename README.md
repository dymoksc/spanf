Signal Processing Analysis and Notification Framework
=====================================================

This a prototype of a framework designed to receive raw signal readouts from sensors, belonging to the specified set of
clients. Those readouts are afterwards to be processed by the specified set of so called data transformers - any
executable capable of receiving a binary input on STDIN and then responding in the specified format to STDOUT.
Processing by any of these data transforming modules can lead to one of the two possible outcomes: creation of a new
data entry in the output format of this data transformer, or creation of a new event log entry. Event log entries are
then processed separately by the another executable in order to notify registered clients about an event registered and
recognized in readouts of their sensors.

Requirements
------------
* Python 2.7.14
* One of supported database systems:
	* SQLite
	* PostgreSQL
	* MySQL
	* Oracle
* pip 9.0.1
* Desktop web browser software, supporting JS arrow functions:
	* MS Edge
	* Mozilla Firefox >= 61
	* Google Chrome >= 49
	* Apple Safari >= 11.1
* bower 1.8.4

Installation
------------

All commands are provided on the condition, that the current working directory is set to the project's root, and are
provided for bash environment. Other terminal environments are expected to function in the similar way, although they
were not tested.  

1. Before any part of the framework is configured, it is necessary to copy config.json.dist file contents to config.json
and then set it up accordingly to the local system setup. This configuration is then passed to the `db.bind()` of Pony
ORM (more about supported systems in [the official Pony ORM documentation](https://docs.ponyorm.com/database.html)).
Database structure should be created automatically by the ORM on the first start of any of the provided services.

2. Then install all the required packages using pip:
```bash
$ pip install -r requirements.txt
```

3. Finally, install frontend bower dependencies using bower:
```bash
$ bower install
```

Parts of the framework
----------------------

### Backend

The framework prototype offers following core executable scripts:

* upload_raw_data.py - used for the initial upload of the raw readouts from sensors, for detailed usage run: 
	`./upload_raw_data.py -h `
* process_data.py - data processing unit, used without arguments
* process_notifications.py - notification processing unit, used without arguments

Then, the prototype contains following sample scripts, which you could use, when testing your setup:

* data_transformers/sample_raw_transformer.py - sample data transformer, returns the length of the accepted data
* data_transformers/sample_event_emitter.py - sample event-emitting data transformer, randomly detects an event of the
	type with an ID = 1 (*please, make sure, that such event type is present in the database, before using this
	transformer*) 
* notifiers/sample_notifier.py - sample notifier, simply appending a message about any event it receives (*please, make
	sure, that the sample_notifier.log file in the same directory as the script is accessible and writable by it*)
	
### Frontend

The frontend is presented with the database administration interface with the three main views, available on the
following endpoints:

1. /\<entityName\> - a database table listing in the form of a datagrid allowing to easily navigate between different
	entities' details, observe their relations and delete entities
	
2. /\<entityName\>/\<entityId\> - detailed view, used for modifying of existing entities and creating new ones

3. /downloadData/\<dataId\> - data download view, serving data saved as contents of Data entities

#### Running frontend

After the installation of all the dependencies listed in requirements.txt, you should have installed
[Flask server](http://flask.pocoo.org/) in your system. Then server is started like this:

```bash
$ FLASK_APP=web/app.py python -m flask run
```

By default, it should start on the port 5000, on which you can connect with your web browser.