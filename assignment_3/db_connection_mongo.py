from pymongo import MongoClient

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

def createPage(col, url, html, status_message):
    page = {
        "url": url,
        "html": html,
        "status_message": status_message,
        "target": False
    }
    col.insert_one(page)

def findPage(col, query):
    return col.find_one(query)

def flagPage(col, url):
    return col.update_one({ 'url': url }, { "$set": { "target": True } })

def addProfessor(col, name, title, office, phone, email, website):
    professor = {
        "name": name,
        "title": title,
        "office": office,
        "phone": phone,
        "email": email,
        "website": website
    }
    col.insert_one(professor)
    