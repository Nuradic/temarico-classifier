import numpy as np
from tabulate import tabulate
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize

stop_words = set(stopwords.words("english"))
ps = PorterStemmer()

# Read from file
def read_text_files_from_folder(folder_path):
    # documents = []
    # for file_name in os.listdir(folder_path):
    #     file_path = os.path.join(folder_path, file_name)
    #     if os.path.isfile(file_path):
    #         with open(file_path, "r") as file:
    #             documents.append(file.read())
    # return documents

    documents = []
    for i in range(1, 4):
        with open(f"{folder_path}/doc{i}.txt", "r") as file:
            documents.append(file.read())
    return documents
def start_indexing():
    inv_index = {}
    docs=read_text_files_from_folder("docs")
    docIndex=0

    for doc in docs:
        tokens = word_tokenize(doc)
        docs[docIndex]=tokens
        res=0
        for term in tokens:
            if term in stop_words:
                continue
            term = ps.stem(term)
            if term not in inv_index:
                inv_index[term] = {}
                inv_index[term]["df"] = 0
                inv_index[term]["cf"] = 0
                inv_index[term]["tfs"] =[]
                inv_index[term]["docs"]=[]
            if(docIndex not in inv_index[term]["docs"]):
                inv_index[term]["tfs"].append(1)
                inv_index[term]["docs"].append(docIndex)
            else:
                ind=inv_index[term]["docs"].index(docIndex)
                inv_index[term]["tfs"][ind]+=1
            inv_index[term]["df"] += 1
            inv_index[term]["cf"] += 1
        docIndex+=1

    sorted_dict = dict(sorted(inv_index.items()))
    with open("index3.py", "w") as file:
        file.write(f"index={sorted_dict}")
    meta={"total_doc":len(docs),"tw":[len(item) for item in docs]}
    with open("index3.py","a") as file:
        file.write(f"\nmeta={meta}")


# folder_path = "docs"  # Replace with the actual folder path
# documents = read_text_files_from_folder(folder_path)



def search(query):
    import index3
    import math
    query_vector = {term:0 for term in index3.index}
    toknized_q=word_tokenize(query)

    for term in toknized_q:
        raw_t=term
        if term in stop_words: continue
        term = ps.stem(term)
        if term in index3.index:
            tf=toknized_q.count(raw_t)/len(toknized_q)
            print(tf)
            idf=math.log2(index3.meta["total_doc"]/index3.index[term]["df"])
            query_vector[term] = tf*idf
    vectors = []
    print(query_vector)
    for i in range(index3.meta["total_doc"]):
        vector = []
        for term in index3.index  :
            if query_vector[term] == 0 :
                vector.append(0)
                continue
            if i in index3.index[term]["docs"]:
                tf=(index3.index[term]["tfs"][index3.index[term]["docs"].index(i)])/index3.meta["tw"][i]
                idf=math.log2(index3.meta["total_doc"]/index3.index[term]["df"])
                vector.append(tf*idf)
            else:
                vector.append(0)
        vectors.append(vector)
    query_vector=list(query_vector.values())
    print(query_vector)
    similarities = [np.dot(query_vector, vector) for vector in vectors]
    print(similarities)

    ranked = sorted(enumerate(similarities, 1), key=lambda x: x[1], reverse=True)
    headers = ["Rank", "Score", "Document"]
    data = []

    r = 0
    for rank, score in ranked:
        r = r + 1
        data.append([r, score, f"doc{rank}"])
    print(tabulate(data, headers, tablefmt="fancy_grid"))



# Create vector space model
# vectors = []
# for doc in documents:
#     vector = []
#     terms = doc.split()
#     for term in inv_index:
#         tf = terms.count(term) / len(terms)
#         vector.append(tf)
#     vectors.append(vector)

# Calculate similarity
# query = "machine learning"
# query_vector = [0] * len(inv_index)
# for term in word_tokenize(query):
#     stemmer = PorterStemmer()
#     term = stemmer.stem(term)
#     if term in inv_index:
#         query_vector[list(inv_index).index(term)] = 1
# similarities = [np.dot(query_vector, vector) for vector in vectors]
# ranked = sorted(enumerate(similarities, 1), key=lambda x: x[1], reverse=True)

# Print results in table format


# start_indexing()
search("machine learning Science")


if __name__ == "__main__":
    pass