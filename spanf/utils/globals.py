from pony.orm import Database

if 'db' not in globals():
    global db
    db = Database()
    db.bind(provider = 'mysql', host='localhost', user = 'signal', passwd = 'signal', db = 'signal')