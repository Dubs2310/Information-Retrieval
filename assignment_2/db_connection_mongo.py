from pymongo import MongoClient
import datetime

def connectDataBase():
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
    user = {
        "_id": id,
        "name": name,
        "email": email,
    }
    col.insert_one(user)


def updateUser(col, id, name, email):
    user = {"$set": {"name": name, "email": email} }
    col.update_one({"_id": id}, user)


def deleteUser(col, id):
    col.delete_one({"_id": id})


def getUser(col, id):
    user = col.find_one({"_id":id})
    if user:
        return str(user['_id']) + " | " + user['name'] + " | " + user['email']
    else:
        return []


def createComment(col, id_user, dateTime, comment):
    comments = {
        "$push": {
            "comments": {
                "datetime": datetime.datetime.strptime(dateTime, "%m/%d/%Y %H:%M:%S"),
                "comment": comment
            }
        }
    }
    col.update_one({"_id": id_user}, comments)


def updateComment(col, id_user, dateTime, new_comment):
    comment = {"$set": {"comments.$.comment": new_comment} }
    col.update_one({"_id": id_user, "comments.datetime": datetime.datetime.strptime(dateTime, "%m/%d/%Y %H:%M:%S")}, comment)


def deleteComment(col, id_user, dateTime):
    comments = {"$pull": {"comments": {"datetime": datetime.datetime.strptime(dateTime, "%m/%d/%Y %H:%M:%S")} }}
    col.update_one({"_id": id_user}, comments)


def getChat(col):
    pipeline = [
        {"$unwind": { "path": "$comments" }},
        {"$sort": {"comments.datetime": 1}}
    ]
    comments = col.aggregate(pipeline)
    chat = ""
    for com in comments:
        chat += com['name'] + " | " + com['comments']['comment'] + " | " + str(com['comments']['datetime']) + "\n"
    return chat



def createDocument(col, id, text, title, date, category):
    doc = {
        "_id": id,
        "text": text,
        "title": title,
        "date": datetime.datetime.strptime(date, "%Y-%m-%d"),
        "category": category
    }
    col.insert_one(doc)


def updateDocument(col, id, text, title, date, category):
    where = { "_id": id }
    set = {
        "$set": {
            "text": text,
            "title": title,
            "date": datetime.datetime.strptime(date, "%Y-%m-%d"),
            "category": category
        }
    }
    col.update_one(where, set)


def deleteDocument(col, id):
    where = { "_id": id }
    col.delete_one(where)

def getIndex(col):
    pipeline = [
        { 
            "$project": { 
                "terms": {
                    "$split": [
                        {
                            "$toLower": { 
                                "$replaceAll": { 
                                    "input": {
                                        "$replaceAll": { 
                                            "input": {
                                                "$replaceAll": { 
                                                    "input": {
                                                        "$replaceAll": { 
                                                            "input": "$text", 
                                                            "find": "?", 
                                                            "replacement": "" 
                                                        }
                                                    }, 
                                                    "find": "!", 
                                                    "replacement": "" 
                                                }
                                            }, 
                                            "find": ",", 
                                            "replacement": "" 
                                        }
                                    }, 
                                    "find": ".", 
                                    "replacement": "" 
                                }
                            }
                        },
                        " "
                    ] 
                }, 
                "title": 1,
                "_id": 0
            } 
        },
        { "$unwind": "$terms" },
        {
            "$group": {
                "_id": {
                    "title": "$title",
                    "term": "$terms"
                },
                "term_count": { "$count": {} },
            }
        },
        {
            "$project": {
                "term": "$_id.term",
                "title_term_count_map": { 
                    "$concat": ["$_id.title", ":", {"$toString" : "$term_count"}] 
                },
                "_id": 0,
            }
        },
        { 
            "$group": { 
                "_id": "$term",
                "term_count_per_title_array": { "$push": "$title_term_count_map" }
            }
        },
        {
            "$addFields": {
                "term_counts_per_title": {
                    "$reduce": {
                        "input": "$term_count_per_title_array",
                        "initialValue": "",
                        "in": {
                            "$cond": {
                                "if": { "$eq": [ { "$indexOfArray": [ "$term_count_per_title_array", "$$this" ] }, 0 ] },
                                "then": { "$concat": [ "$$value", "$$this" ] },
                                "else": { "$concat": [ "$$value", ", ", "$$this" ] }
                            }
                        }
                    }
                }
            }
        },
        {
            "$project": {
                "kvObject": { 
                    "k": "$_id", 
                    "v": "$term_counts_per_title" 
                },
                "_id": 0
            }
        },
        {
            "$group": {
                "_id": "null",
                "kvObjects": { "$push": "$kvObject" }
            }
        },
        {
            "$project": {
                "results": {
                    "$arrayToObject": "$kvObjects"
                }
            }
        }
    ]
    for result in col.aggregate(pipeline):
        return result["results"]