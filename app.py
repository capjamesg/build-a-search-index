import string
import time

documents = [
    {
        "title": "tolerate it",
        "lyric": "I made you my temple, my mural, my sky"
    },
    {
        "title": "my tears ricochet",
        "lyric": "And I still talk to you when I'm screaming at the sky",
    },
    {
        "title": "The Bolter",
        "lyric": "Started with a kiss"
    }
]

def transform_text(text):
    return text.lower().translate(str.maketrans("", "", string.punctuation))
    
index = {}

for i, doc in enumerate(documents):
    lyric = transform_text(doc["lyric"])
    for word in lyric.split():
        if word not in index:
            index[word] = set({})
        index[word].add(i)

def search(query):
    words = transform_text(query).split()
    results = set()

    for word in words:
        if word in index:
            results.update(index[word])
            
    titles = [documents[idx] for idx in results]
            
    return titles

start = time.time()

for _ in range(20):
    search("sky")

end = time.time()

print("Time taken for index:", end - start)

def search_by_words(query):
    lyric = transform_text(query).split()

    results = []

    for word in lyric:
        for doc in documents:
            if word in transform_text(doc["lyric"]):
                results.append(doc)

    titles = [doc["title"] for doc in results]

    return titles

start = time.time()
for _ in range(20):
    search_by_words("sky")

end = time.time()

print("Time taken for manual comparisons:", end - start)
