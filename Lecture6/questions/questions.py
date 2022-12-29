import nltk
import sys
import os
import string
import math

FILE_MATCHES = 1
SENTENCE_MATCHES = 1


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    files = dict()
    for file in os.listdir(directory):
        files[os.path.basename(file)] = open(
            os.path.join(directory, file), encoding="utf-8").read()
    return files


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    words = nltk.word_tokenize(document)
    words = [word.lower() for word in words if word not in nltk.corpus.stopwords.words(
        'english') and word not in string.punctuation]
    return words


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    idf_dict = dict()

    unique_words = set(sum(documents.values(), []))

    for word in unique_words:
        count = 0
        for doc in documents.values():
            if word in doc:
                count += 1
        idf_dict[word] = math.log(len(documents)/count)

    return idf_dict


def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    scores = {}
    for filename, wordlist in files.items():
        file_score = 0
        for word in query:
            if word in wordlist:
                file_score += wordlist.count(word) * idfs[word]
        if file_score != 0:
            scores[filename] = file_score

    sorted_scores = [x[0] for x in sorted(scores.items(), key=lambda x: x[1], reverse=True)]

    return sorted_scores[:n]



def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    scores = {}
    for sentence, sentence_words in sentences.items():
        score = 0
        for word in query:
            if word in sentence_words:
                score += idfs[word]
        if score != 0:
            density = sum([sentence_words.count(x) for x in query]) / len(sentence_words)
            scores[sentence] = (score, density)
            
    sorted_scores = [x[0] for x in sorted(scores.items(), key=lambda x: (x[1][0], x[1][1]), reverse=True)]
    return sorted_scores[:n]


if __name__ == "__main__":
    main()
