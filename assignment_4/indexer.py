from typing import List, Tuple
from db_connection_mongo import *
import numpy as np
import math
import re

class Indexer:
    def __init__(self):
        self.db = connectDataBase()
        self.documents = self.db['documents']
        self.terms = self.db['terms']
        self.documents.drop()
        self.terms.drop()
        self.doc_id_counter = 1
        self.term_id_counter = 1
        self.vocabulary = {}

    def preprocess_text(self, text):
        text = re.sub(r'[^\w\s]', '', text.lower())
        return text.split()

    def generate_ngrams(self, tokens):
        ngrams = tokens.copy()                                          # Unigrams
        for i in range(len(tokens) - 1):                                # Bigrams
            ngrams.append(f"{tokens[i]} {tokens[i+1]}")
        for i in range(len(tokens) - 2):                                # Trigrams
            ngrams.append(f"{tokens[i]} {tokens[i+1]} {tokens[i+2]}")
        return ngrams

    def calculate_tf_idf(self, term_freq, total_docs, docs_with_term):
        tf = 1 + math.log(term_freq) if term_freq > 0 else 0
        idf = math.log(total_docs / (1 + docs_with_term))
        return tf * idf

    def build_index(self, documents):
        self.doc_id_counter = 1
        self.term_id_counter = 1
        self.vocabulary = {}
        
        for doc_text in documents:
            createDocument(self.documents, self.doc_id_counter, doc_text)
            tokens = self.preprocess_text(doc_text)
            ngrams = self.generate_ngrams(tokens)
            
            doc_term_freq = {}
            for token in ngrams:
                doc_term_freq[token] = doc_term_freq.get(token, 0) + 1
            
            for term in set(ngrams):
                if term not in self.vocabulary:
                    self.vocabulary[term] = self.term_id_counter
                    self.term_id_counter += 1
                
                docs_with_term = getDocumentCountUsingTerm(self.terms, term)
                tf_idf = self.calculate_tf_idf(doc_term_freq[term], len(documents), docs_with_term + 1)
                upsertTermWithDocumentAndTfIdf(self.terms, term, self.doc_id_counter, tf_idf)
            
            self.doc_id_counter += 1

    def rank_documents(self, query):
        query_tokens = self.preprocess_text(query)
        query_ngrams = self.generate_ngrams(query_tokens)
        
        matching_docs = {}
        query_term_weights = {}
        
        for term in query_ngrams:
            term_entry = findFirstTerm(self.terms, term)
            if term_entry:
                for doc_ref in term_entry.get('docs', []):
                    doc_id = doc_ref['doc_id']
                    tf_idf = doc_ref['tf_idf']
                    
                    if doc_id not in matching_docs:
                        matching_docs[doc_id] = {}
                    
                    matching_docs[doc_id][term] = tf_idf
                    query_term_weights[term] = 1

        ranked_docs = []
        for doc_id, doc_terms in matching_docs.items():
            doc = self.documents.find_one({'_id': doc_id})
            
            doc_vector = []
            query_vector = []
            
            for term in query_ngrams:
                doc_weight = doc_terms.get(term, 0)
                query_weight = query_term_weights.get(term, 0)
                
                if doc_weight > 0 or query_weight > 0:
                    doc_vector.append(doc_weight)
                    query_vector.append(query_weight)
            
            if doc_vector and query_vector:
                doc_norm = np.linalg.norm(doc_vector)
                query_norm = np.linalg.norm(query_vector)
                
                dot_product = np.dot(doc_vector, query_vector)
                cosine_sim = dot_product / (doc_norm * query_norm) if doc_norm * query_norm != 0 else 0
                ranked_docs.append((doc['content'], round(cosine_sim, 2)))

        return sorted(ranked_docs, key=lambda x: x[1], reverse=True)