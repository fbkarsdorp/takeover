import os

from collections import Counter
from heapq import nlargest

from joblib import Parallel, delayed


def disambiguate(persons):


def count_persons(decade):
    print 'Counting PERSONS in ', decade
    decade_counter = Counter()
    for filename in os.listdir(decade):
        previous_person = ''
        with open(os.path.join(decade, filename)) as infile:
            for line in infile:
                word, _, _, named_entity = line.strip().split("\t")
                if named_entity == 'PERSON':
                    previous_person += ' ' + word
                elif previous_person:
                    decade_counter[previous_person] += 1
                    previous_person = ''
    return decade_counter

root = '../rich_texts_txt'
counters = Parallel(n_jobs=-1, verbose=5)(
    delayed(count_persons)(
        os.path.join('../rich_texts_txt', decade)) for decade in os.listdir(root))
person_counter = sum(counters, Counter())
        
top100 = nlargest(100, person_counter, key=mention_counter.__getitem__)
