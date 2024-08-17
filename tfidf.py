import math
import string
from collections import defaultdict
import time

documents = [
    {
        "title": "tolerate it",
        "lyric": "I made you my temple, my mural, my sky"},
    {
        "title": "my tears ricochet",
        "lyric": "And I still talk to you when I'm screaming at the sky",
    },
    {
        "title": "The Bolter",
        "lyric": "Started with a kiss"
    },
] * 20000

document_count = len(documents)

word_counts = defaultdict(int)
document_term_frequencies = {}
inverse_document_frequencies = {}

for doc in documents:
    lyric = doc["lyric"].lower().translate(str.maketrans("", "", string.punctuation))
    number_of_words = len(lyric.split())

    document_term_frequencies[doc["title"]] = defaultdict(int)

    for word in lyric.split():
        word_counts[word] += 1
        document_term_frequencies[doc["title"]][word] += 1

    document_term_frequencies[doc["title"]] = {
        word: count / number_of_words
        for word, count in document_term_frequencies[doc["title"]].items()
    }

for word, count in word_counts.items():
    inverse_document_frequencies[word] = (
        math.log(document_count / count)
    )


def tfidf(query, documents = documents):
    words = query.split()
    results = {}

    for doc in documents:
        tfidfs = [
            document_term_frequencies[doc["title"]].get(word, 0)
            * inverse_document_frequencies.get(word, 0)
            for word in words
        ]

        results[doc["title"]] = sum(tfidfs)

    results = sorted(results.items(), key=lambda x: x[1], reverse=True)

    return results

start = time.time()

for _ in range(10):
    for result in tfidf("my sky started with a kiss"):
        print(result)

end = time.time()

print("Time taken for tfidf:", end - start)
