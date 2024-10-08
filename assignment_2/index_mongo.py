#-------------------------------------------------------------------------
# AUTHOR: Abdullah Irfan Siddiqui
# FILENAME: index_mongo.py
# SPECIFICATION: A menu based program for CRUD applications into a mongo db database
# FOR: CS 5180- Assignment #2
# TIME SPENT: 1 hr
#-----------------------------------------------------------*/

from pymongo import MongoClient  # import mongo client to connect
from db_connection_mongo import *

if __name__ == '__main__':
    db = connectDataBase()
    documents = db["documents"]

    print("")
    print("######### Menu ##############")
    print("#a - Create a document")
    print("#b - Update a document")
    print("#c - Delete a document.")
    print("#d - Output the inverted index ordered by term.")
    print("#q - Quit")

    option = ""
    while option != "q":
        print("")
        option = input("Enter a menu choice: ")

        if (option == "a"):
            docId = input("Enter the ID of the document: ")
            docText = input("Enter the text of the document: ")
            docTitle = input("Enter the title of the document: ")
            docDate = input("Enter the date of the document: ")
            docCat = input("Enter the category of the document: ")
            createDocument(documents, docId, docText, docTitle, docDate, docCat)

        elif (option == "b"):
            docId = input("Enter the ID of the document: ")
            docText = input("Enter the text of the document: ")
            docTitle = input("Enter the title of the document: ")
            docDate = input("Enter the date of the document: ")
            docCat = input("Enter the category of the document: ")
            updateDocument(documents, docId, docText, docTitle, docDate, docCat)

        elif (option == "c"):
            docId = input("Enter the document ID to be deleted: ")
            deleteDocument(documents, docId)

        elif (option == "d"):
            index = getIndex(documents)
            print(index)

        elif (option == "q"):
             print("Leaving the application ... ")

        else:
             print("Invalid Choice.")