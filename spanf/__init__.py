from pony.orm import Database, set_sql_debug


set_sql_debug(True)

db = Database()
db.bind(provider = 'mysql', host='localhost', user = 'signal', passwd = 'signal', db = 'signal')
db.generate_mapping(create_tables=True)