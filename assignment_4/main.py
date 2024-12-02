from indexer import *

def main():
    # Documents to index
    documents = [
        "After the medication, headache and nausea were reported by the patient.",
        "The patient reported nausea and dizziness caused by the medication.",
        "Headache and dizziness are common effects of this medication.",
        "The medication caused a headache and nausea, but no dizziness was reported."
    ]

    # Create indexer
    indexer = Indexer()
    
    # Build index
    indexer.build_index(documents)
    
    # Queries to rank
    queries = [
        "nausea and dizziness",
        "effects",
        "nausea was reported",
        "dizziness",
        "the medication"
    ]
    
    # Rank and print results for each query
    for i, query in enumerate(queries, 1):
        print(f"\nQuery q{i}: '{query}'")
        results = indexer.rank_documents(query)
        
        for doc, score in results:
            print(f'"{doc}", {score}')

if __name__ == "__main__":
    main()