from cgi import print_environ
import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    num_links = len(corpus[page])
    if num_links == 0:
        probabilities = {}
        for page in corpus.keys():
            probabilities[page] = 1 / len(corpus)
    else:
        bonus = (1 - damping_factor) / (num_links + 1)
        probabilities = {page: bonus}
        for link in corpus[page]:
            probabilities[link] = damping_factor / num_links
            probabilities[link] += bonus

    return probabilities


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    sample_PR = {}
    for page in corpus:
        sample_PR[page] = 0

    pages = list(corpus.keys())
    first_page = random.choice(pages)
    sample_PR[first_page] += 1

    probabilities = transition_model(corpus, first_page, damping_factor)
    for i in range(n-1):
        page = random.choices(list(probabilities.keys()),
                              list(probabilities.values())).pop()
        sample_PR[page] += 1
        probabilities = transition_model(corpus, page, damping_factor)

    sample_PR = {key: value/n for key, value in sample_PR.items()}

    return sample_PR


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    iterate_PR = {}
    num_pages = len(corpus)

    # Assigning each page a rank of 1 / N, where N is the total number of pages in the corpus.
    for page in corpus:
        iterate_PR[page] = 1/num_pages
    
    changes = 1
    iterations = 1
    while changes > 0.001:
        changes = 0

        previous_state = iterate_PR.copy()

        for page in iterate_PR:
            parents = [link for link in corpus if page in corpus[link]]
            randomSurfer = (1-damping_factor)/num_pages
            linkSurfer = []
            if len(parents) != 0:
                for parent in parents:
                    num_links = len(corpus[parent])
                    linkSurfer.append(previous_state[parent] / num_links)
            linkSurfer = sum(linkSurfer)
            iterate_PR[page] = randomSurfer + (damping_factor * linkSurfer)
            new_change = abs(iterate_PR[page] - previous_state[page])
            if changes < new_change:
                changes = new_change
        iterations += 1
    dictsum = sum(iterate_PR.values())
    iterate_PR = {key: value/dictsum for key, value in iterate_PR.items()}
    return iterate_PR
        
        
    

if __name__ == "__main__":
    main()
