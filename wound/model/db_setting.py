import click
import pymongo
import pymongo.collection
import pymongo.database
import pymongo.collection
import pymongo.cursor
import pymongo.command_cursor
import pymongo.results
from flask import current_app, g
from flask.cli import with_appcontext
from bson import ObjectId

def get_db() -> pymongo.database.Database:
    mongocon = current_app.config['MONGO_CON']
    dbclient = pymongo.MongoClient(mongocon)
    g.db = dbclient[current_app.config['DATABASE']]
    return g.db

def get_collection(collection_name) -> pymongo.collection.Collection:
    if 'db' not in g:
        get_db()
    return g.db[collection_name]

def get_from_collection(collection_name: str, filters: dict = {}) -> pymongo.cursor.Cursor:
    collection = get_collection(collection_name)
    row = collection.find(filters)
    return row

def get_one_from_collection(collection_name: str, filters: dict = {}) -> pymongo.collection.ReturnDocument:
    collection = get_collection(collection_name)
    row = collection.find_one(filters)
    return row

def aggregate_to_collection(collection_name: str, pipeline: list = []) -> pymongo.command_cursor.CommandCursor:
    collection = get_collection(collection_name)
    row = collection.aggregate(pipeline)
    return row

def insert_to_collection(collection_name: str, data: dict) -> pymongo.results.InsertOneResult:
    collection = get_collection(collection_name)
    row = collection.insert_one(data)
    return row

def update_from_collection(collection_name: str, id: str, data: dict) -> pymongo.results.UpdateResult:
    collection = get_collection(collection_name)
    id = ObjectId(id)
    filters = {'_id': id}
    return collection.update_one(filters, update={'$set': data}, upsert=False)
    # return collection.update_one(filters, {'$set': data})

def replace_from_collection(collection_name: str, id: str, data: dict) -> pymongo.results.UpdateResult:
    collection = get_collection(collection_name)
    id = ObjectId(id)
    filters = {'_id': id}
    return collection.replace_one(filters, replacement=data, upsert=False)

def delete_from_collection(collection_name: str, id: str) -> pymongo.results.DeleteResult:
    collection = get_collection(collection_name)
    id = ObjectId(id)
    filters = {'_id': id}
    return collection.delete_one(filters)

def close_db(e = None):
    db = g.pop(current_app.config['DATABASE'], None)
    
    if db is not None:
        db.close() 

def init_db():
    """clear the existing data and create new tables."""    
    db = get_db()    
    db.client.drop_database(current_app.config['DATABASE'])
    
@click.command('init-db')
@with_appcontext
def init_db_command():    
    init_db()
    click.echo('Initialized the database.')

def init_app(app):
    "app.teardown_appcontext(close_db)"
    app.cli.add_command(init_db_command)