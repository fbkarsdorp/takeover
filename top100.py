import os
import sys

from collections import Counter
from heapq import nlargest
from itertools import combinations

import numpy as np
import pandas as pd
import networkx as nx

from joblib import Parallel, delayed


def count_persons(decade):
    counter = Counter()
    for filename in os.listdir(decade):
        previous_person = ''
        with open(os.path.join(decade, filename)) as infile:
            for line in infile:
                word, _, _, named_entity = line.strip().split("\t")
                if named_entity == 'PERSON':
                    previous_person += ' ' + word
                elif previous_person:
                    counter[previous_person.lower()] += 1
                    previous_person = ''
    return counter

if __name__ == '__main__':
    root = sys.argv[1]
    n = int(sys.argv[2])
    counters = Parallel(n_jobs=-1, verbose=5)(
        delayed(count_persons)(
            os.path.join(root, decade)) for decade in os.listdir(root))
    counts = sum(counters, Counter())
    top_n = dict((name, i) for i, name in enumerate(nlargest(n, counts, key=counts.__getitem__)))
    cooccurrences = np.zeros((n, n))
    for decade in os.listdir(root):
        print decade
        decade = os.path.join(root, decade)
        for filename in os.listdir(decade):
            persons = set()
            previous_person = ''
            with open(os.path.join(decade, filename)) as infile:
                for line in infile:
                    word, _, _, named_entity = line.strip().split("\t")
                    if named_entity == 'PERSON':
                        previous_person += ' ' + word
                    elif previous_person:
                        if previous_person.lower() in top_n:
                            persons.add(previous_person.lower())
                        previous_person = ''
            for person_a, person_b in combinations(persons, 2):
                cooccurrences[top_n[person_a], top_n[person_b]] += 1
                cooccurrences[top_n[person_b], top_n[person_a]] += 1
    names = sorted(top_n, key=top_n.__getitem__)
    G = nx.DiGraph()
    for i, name_i in enumerate(names):
        for j, name_j in enumerate(names):
            if j != i:
                G.add_edge(name_i, name_j, weight=cooccurrences[i, j])
    df = pd.DataFrame(cooccurrences, columns=names, index=names)
    df.to_csv("top-%s.csv" % n)

