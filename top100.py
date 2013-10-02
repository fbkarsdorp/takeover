import os
import sys

from collections import Counter
from heapq import nlargest
from itertools import combinations

import numpy as np
import pandas as pd

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
    counters = Parallel(n_jobs=-1, verbose=5)(
        delayed(count_persons)(
            os.path.join(root, decade)) for decade in os.listdir(root))
    counts = sum(counters, Counter())
    top100 = dict((name, i) for i, name in enumerate(nlargest(50, counts, key=counts.__getitem__)))
    cooccurrences = np.zeros((50, 50))
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
                        if previous_person.lower() in top100:
                            persons.add(previous_person.lower())
                        previous_person = ''
            for person_a, person_b in combinations(persons, 2):
                cooccurrences[top100[person_a], top100[person_b]] += 1
                cooccurrences[top100[person_b], top100[person_a]] += 1
    names = sorted(top100, key=top100.__getitem__)
    df = pd.DataFrame(cooccurrences, columns=names, index=names)
    df.to_csv("top100.csv")

