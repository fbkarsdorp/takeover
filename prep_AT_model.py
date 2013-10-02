import os
import sys

from collections import defaultdict
from top100 import count_persons
from joblib import Parallel, delayed

top100 = set(line.strip().lower() for line in open('../top100.txt'))

def extract_filenames(decade):
    print decade
    files = defaultdict(set)
    for filename in os.listdir(decade):
        previous_person = []
        with open(os.path.join(decade, filename)) as infile:
            for line in infile:
                word, _, _, named_entity = line.strip().split('\t')
                if named_entity == 'PERSON':
                    previous_person.append(word)
                elif previous_person:
                    previous_person = ' '.join(previous_person).lower()
                    if previous_person in top100:
                        files[os.path.join(decade, filename)].add(previous_person)
                    previous_person = []
    return files

def read_text(text):
    return ' '.join(line.split('\t')[0].lower() for line in text if line.split('\t')[2].startswith(('V', 'N')))

root = sys.argv[1]
filedicts = Parallel(n_jobs=-1, verbose=5)(
    delayed(extract_filenames)(
        os.path.join(root, decade)) for decade in os.listdir(root))
maindict = defaultdict(set)
with open('../AT_model.docs.txt', 'w') as out:
    for filedict in filedicts:
        for filename, persons in filedict.iteritems():
            with open(os.path.join(root, filename)) as text:
                out.write("%s\t%s\t%s\t%s\n" % (
                    filename, ','.join(persons), "XXX", read_text(text)))

