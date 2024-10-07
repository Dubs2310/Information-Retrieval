from pymongo import MongoClient
import datetime

def connectDataBase():

    # Creating a database connection object using pymongo

    DB_NAME = "CPP"
    DB_HOST = "localhost"
    DB_PORT = 27017

    try:

        client = MongoClient(host=DB_HOST, port=DB_PORT)
        db = client[DB_NAME]

        return db

    except:
        print("Database not connected successfully")

def createUser(col, id, name, email):

    # Value to be inserted
    user = {"_id": id,
            "name": name,
            "email": email,
            }

    # Insert the document
    col.insert_one(user)

def updateUser(col, id, name, email):

    # User fields to be updated
    user = {"$set": {"name": name, "email": email} }

    # Updating the user
    col.update_one({"_id": id}, user)

def deleteUser(col, id):

    # Delete the document from the database
    col.delete_one({"_id": id})

def getUser(col, id):

    user = col.find_one({"_id":id})

    if user:
        return str(user['_id']) + " | " + user['name'] + " | " + user['email']
    else:
        return []

def createComment(col, id_user, dateTime, comment):

    # Comments to be included
    comments = {"$push": {"comments": {
                                       "datetime": datetime.datetime.strptime(dateTime, "%m/%d/%Y %H:%M:%S"),
                                       "comment": comment
                                       } }}

    # Updating the user document
    col.update_one({"_id": id_user}, comments)

def updateComment(col, id_user, dateTime, new_comment):

    # User fields to be updated
    comment = {"$set": {"comments.$.comment": new_comment} }

    # Updating the user
    col.update_one({"_id": id_user, "comments.datetime": datetime.datetime.strptime(dateTime, "%m/%d/%Y %H:%M:%S")}, comment)

def deleteComment(col, id_user, dateTime):

    # Comments to be delete
    comments = {"$pull": {"comments": {"datetime": datetime.datetime.strptime(dateTime, "%m/%d/%Y %H:%M:%S")} }}

    # Updating the user document
    col.update_one({"_id": id_user}, comments)

def getChat(col):

    # creating a document for each message
    pipeline = [
                 {"$unwind": { "path": "$comments" }},
                 {"$sort": {"comments.datetime": 1}}
               ]

    comments = col.aggregate(pipeline)

    chat = ""

    for com in comments:
        chat += com['name'] + " | " + com['comments']['comment'] + " | " + str(com['comments']['datetime']) + "\n"

    return chat