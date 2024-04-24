import os
import random
import re
import sys
import copy
from numpy.random import choice

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1]) #parses all the HTML files and returns a dictionary: keys=pages, values=pages linked to key
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES) #estimates pagerank by sampling -> returns dict
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING) #calculates pagerank by using iterative formula method
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
corpus = {"1.html":{"2.html","3.html"}, "2.html":{"3.html"}, "3.html":{"2.html"}, "4.html":{}}


def transition_model(corpus, page, damping_factor): #dict representing prob dist over which
    d = damping_factor # page a random surfer would visit next
    N = len(corpus)
    prob = {i:(1-d)/N for i in corpus}
    pg_rank = len(corpus[page])
    for neigh in corpus[page]:
        prob[neigh] += d/pg_rank
    print(sum(prob.values()))
    return prob



# def transition_model(corpus, page, damping_factor):
#     #return dict representing probability pagerank
#     #page=page random surfer is currently on
#     rank = {}
#     count = {}
#     N=len(corpus)
#     refPage=page
#     d=damping_factor
#     for i in corpus:  #initiating pagerank dict
#         rank[i]=1/N 
#         count[i]=0

#     if len(corpus[page])==0:  #page has no outgoing links
#         return rank

#     for i in range(SAMPLES):
#         draw = choice([0,1], p=[d, 1-d])
#         if draw: 
#             chosenPage = choice(tuple(corpus))
#             count[chosenPage] += 1
        
#         else:
#              chosenPage = choice(tuple(corpus[refPage]))
#              count[chosenPage] += 1
#              refPage = chosenPage

#     for i in corpus:
#         rank[i]=count[i]/SAMPLES

#     return rank



    # N=len(corpus)
    # d=damping_factor
    # choice1=(1-d)/N
    # choice2 = 0
    # if len(corpus[page])==0:
        
    # for i in range(len(corpus[page])):
    #     nowpage = corpus[page][i]
    #     choice2 += sample_pagerank(corpus,damping_factor,SAMPLES)[nowpage]/len(corpus[nowpage])
    # choice2 = d * choice2
    # return choice1 + choice2

    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    #raise NotImplementedError

#print(transition_model(corpus, "4.html", 0.85))
# def dictMerge(dict1, dict2):
#     dict1c = copy.deepcopy(dict1)
#     dict2c = copy.deepcopy(dict2)
#     dict2c = {i:{dict2c[i]} for i in dict2c}
#     dict1c = {i:{dict1c[i]} for i in dict1c}
#     save = {}
#     for i in dict1c:
#         if i in dict2c:
#             save[i] = dict1c[i] | dict2c[i]
#             print(save[i])
#         else:
#             save[i] = dict1c[i]
#     for j in dict2c:
#         if j not in dict1c:
#             save[j] = dict2c[j]
#     return save



corpus_t = {'1':{'2'}, '2':{'3','1'}, '3':{'2','4'},'4':{'2'}}

def sample_pagerank(corpus, damping_factor, n):
    corp = copy.deepcopy(corpus)
    for i in corp.keys():
        if len(corp[i])==0:
            corp[i]=set([j for j in corp.keys()])
    noLinks = True
    for i in corp:
        if len(corp[i]) != 0:
            noLinks = False
            break
    if noLinks:
        return {i:1/len(corp) for i in corp}

    
    page = choice(list(corp.keys()))
    save = {i:0 for i in corp}
    save[page] +=1

    prob = transition_model(corp,page,damping_factor)
    
    
    for i in range(n-1):
        page = choice(list(prob.keys()), p=list(prob.values()))
        save[page] +=1
        prob = transition_model(corp, page, damping_factor)

    re = {}
    for i in save:
        re[i] = save[i]/n
    return re

#print(sample_pagerank(corpus, 0.85, 100))
#print(sample_pagerank(corpus,0.85,5))
co = {'1':{'2'},'2':{'1','3'},'3':{'2', '5','4'},'4':{ '1', '2'},'5':set()}
#print(sample_pagerank(co, 0.85, 100))
"""
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    #raise NotImplementedError

def iterate_pagerank(corpus, damping_factor):
    corp = copy.deepcopy(corpus)
    for i in corp.keys():
        if len(corp[i])==0:
            corp[i]=set([j for j in corp.keys()])
    N = len(corp)
    d = damping_factor
    leadingTo = {i:[key for key,value in corp.items() if i in value] for i in corp.keys()}
    pagerank = {i:1/N for i in corp.keys()}
    BiggerDiff = True
    
    while BiggerDiff:
        BiggerDiff = False
        last = copy.deepcopy(pagerank)
        for page in corp.keys():
            pt1 = (1-d)/N
            pt2 = 0
            for i in leadingTo[page]:
                pt2 += pagerank[i]/len(corp[i])
            pagerank[page] = pt1 + d*pt2
            
            if abs( last[page] - pagerank[page] ) > 0.001:
                BiggerDiff = True
                
    return pagerank
    
corp2 = {'1':{'2','3'}, '2':{'3','4','1'},'3':{5,'4'}, '4':{'2','6','1','3'},'5':{3}
,'6':{'2','3','1'}}
corp3 = {'1':{'2'}, '2':{'3','1'},'3':{'2','5','4'}, '4':{'2','1'},'5':set() }
print(iterate_pagerank(corp3, 0.85))



# def iterate_pagerank(corpus, damping_factor):
#     N = len(corpus)
#     d = damping_factor
#     save = {i:1/N for i in corpus}
#     links = {i:set() for i in corpus}

#     for i in corpus:
#         for j in corpus[i]:
#             links[j] = links[j] | {i}

#     noLinks = True
#     for i in corpus:
#         if len(corpus[i]) != 0:
#             noLinks = False
#             break
#     if noLinks:
#         return save
    
#     #for k in range(5):
#     biggerDif = True
#     while biggerDif:
#         last = save
#         choice1 = (1-d)/N
#         for j in save:
#             choice2 = 0
             
#             for i in links[j]:
#                 choice2 += save[i]/len(corpus[i])
#             choice2 = d * choice2
#             save[j] = choice1 + choice2
#         biggerDif = False
#         print(save)
#         for i in save:
#             if abs(last[i]-save[i])>0.001:
#                 biggerDif = True
#     return save
#     #return save



"""
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    #raise NotImplementedError
#print(iterate_pagerank(corpus,0.85))


if __name__ == "__main__":
    main()
