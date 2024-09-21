#---------------------------------------------------------------------------------------------------------------------------------------------
# AUTHOR: Abdullah Irfan Siddiqui
# FILENAME: indexing.py
# SPECIFICATION: A program to index terms in a document and printing out the tf-idf weights of the terms relative to their documents
# FOR: CS 5180- Assignment #1
# TIME SPENT: 5 hours
#---------------------------------------------------------------------------------------------------------------------------------------------

# Importing some Python libraries ------------------------------------------------------------------------------------------------------------
import math, csv
documents = []

# Function to print the documents (with labels) and their contents
def print_docs(message, documents):
    print(message)
    for i in range(len(documents)):
        print(f'\td{i + 1}.', documents[i])
    print()

# Reading the data in a csv file -------------------------------------------------------------------------------------------------------------
with open('collection.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)    
    for i, row in enumerate(reader):
        if i > 0:
            documents.append(row[0])

print_docs("\nPrinting all documents (original):", documents)

# Conducting stopword removal for pronouns/conjunctions. Hint: use a set to define your stopwords. -------------------------------------------
stop_words = {'i', 'and', 'she', 'her', 'they', 'their'}
print("Stopwords:", stop_words)

for i in range(len(documents)):
    words = documents[i].split()
    for word in words:
        if word.lower() in stop_words:
            words.remove(word)
    documents[i] = ' '.join(words)

print_docs("Printing all documents (after stopward removal):", documents)


# Conducting stemming. Hint: use a dictionary to map word variations to their stem. ----------------------------------------------------------
stemming = {}

# Function to check if a stem exists for a word, and to return the stem if found or None, with a status message of success or failure
def does_stem_exist_for_(word):
    stems = stemming.keys()
    if not stems:
        return None, "failure: stem set is empty"
    for stem in stems:
        if word == stem:
            return None, "success: word is itself a stem"
        if word.startswith(stem):
            return stem, "success: word is a variation of stem"
        if stem.startswith(word):
            return stem, "success: stem is a variation of word"
    return None, "failure: no stem found for word"

# Creating map of variations to their stem
for doc in documents:
    words = doc.split()
    for word in words:
        stem, status_message = does_stem_exist_for_(word)
        if status_message == "failure: stem set is empty" or status_message == "failure: no stem found for word":
            stemming[word] = set()
        elif status_message == "success: word is itself a stem":
            pass
        elif status_message == "success: word is a variation of stem":
            stemming[stem].add(word)
        elif status_message == "success: stem is a variation of word":
            stemming[word] = stemming[stem].union([stem])
            stemming.pop(stem)

print("Stem variations map:", stemming)

# Function to retrieve the stem of a word
def get_stem_for_(word):
    for stem, variations in stemming.items():
        if word == stem or word in variations:
            return stem
    return None

# Stemming documents using stem-variation map
for i in range(len(documents)):
    words = documents[i].split()
    stemmed_words = [get_stem_for_(word) for word in words]
    documents[i] = ' '.join(stemmed_words)

print_docs("Printing all documents (after stemming):", documents)

# Identifying the index terms. ----------------------------------------------------------------------------------------------------------------
terms = []
for doc in documents:
    words = doc.split()
    for word in words:
        if not word in terms:
            terms.append(word)

print("Printing all terms:", terms, '\n')

# Building the document-term matrix by using the tf-idf weights. ------------------------------------------------------------------------------

# Calculating the term counts per document
term_counts = [
    [doc.split().count(term) for term in terms]
    for doc in documents
]

# Calculating the term frequencies per document, i.e. the normalized term counts per document
term_frequencies = [
    [term_count / sum(term_count_row) for term_count in term_count_row]
    for term_count_row in term_counts
]

# Calculating the document frequency per term, i.e. the number of documents that contain the term
document_frequencies = [[]]
for term in terms:
    document_frequency = 0
    for doc in documents:
        if term in doc:
            document_frequency += 1
    document_frequencies[0].append(document_frequency)

# Calculating the inverse document frequencies, i.e. the inverse log ratio of the total number of documents to the document frequency per term
inverse_document_frequencies = [
    [math.log10(len(documents) / document_frequency) for document_frequency in document_frequencies[0]]
]

# Calculating the term frequency - inverse document frequency weights per term
term_frequency_inverse_document_frequencies = [
    [(term_frequency_row[i] * inverse_document_frequencies[0][i]) for i in range(len(term_frequency_row))] 
    for term_frequency_row in term_frequencies
]

# Printing the document-term matrix. ----------------------------------------------------------------------------------------------------------
def print_doc_term_matrix(metric, doc_term_matrix):
    print(
        ("{:<35} " * (len(doc_term_matrix[0]) + 1)).format(
            f"\nDocument-Term Matrix ({metric})", 
            *(f'Term {i + 1} - "{terms[i]}"' for i in range(len(terms)))
        )
    )
    for i in range(len(doc_term_matrix)):
        row = doc_term_matrix[i]
        print(("{:<35} " * (len(row) + 1)).format(f"d{i + 1}" if not metric in ["df", "idf"] else "D", *row))
    print()

print_doc_term_matrix("count", term_counts)
print_doc_term_matrix("tf", term_frequencies)
print_doc_term_matrix("df", document_frequencies)
print_doc_term_matrix("idf", inverse_document_frequencies)
print_doc_term_matrix("tf-idf", term_frequency_inverse_document_frequencies)