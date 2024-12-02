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

def createDocument(docs, id, content):
    page = {
        "_id": id,
        "content": content
    }
    docs.insert_one(page)

def getDocumentCountUsingTerm(terms, term):
    return terms.count_documents({ 'term': term })

def upsertTermWithDocumentAndTfIdf(terms, term, doc_id, tf_idf):
    terms.find_one_and_update(
        {'term': term},
        {'$push': {
            'docs': {
                'doc_id': doc_id,
                'tf_idf': tf_idf
            }
        }},
        upsert=True
    )

def findFirstTerm(terms, term):
    return terms.find_one({'term': term})
