import os
import random
import sys
import time

from collections import Counter, OrderedDict
from heapq import nlargest

from multiprocessing import Process as Task, Queue, log_to_stderr


def print_progress(progress):
    sys.stdout.write('\033[2J\033[H') #clear screen
    for filename, percent in progress.items():
        bar = ('=' * int(percent * 20)).ljust(20)
        percent = int(percent * 100)
        sys.stdout.write("%s [%s] %s%%\n" % (filename, bar, percent))
    sys.stdout.flush()

def main(root):
    status = Queue()
    result = Queue()
    progress = OrderedDict()
    workers = []
    for decade in sorted(os.listdir(root)):
        decade = os.path.join(root, decade)
        child = Task(target=count_persons, args=(status, decade, result))
        child.start()
        workers.append(child)
        progress[decade] = 0.0
    while any(worker.is_alive() for worker in workers):
       time.sleep(0.1) 
       while not status.empty():
            decade, percent = status.get()
            progress[decade] = percent
            print_progress(progress)
    return [result.get() for worker in workers]

def count_persons(status, decade, result):
    decade_counter = Counter()
    filenames = os.listdir(decade)
    filenumber = len(filenames)
    for i, filename in enumerate(filenames):
        status.put([decade, (i+1.0)/filenumber])
        time.sleep(0.1)
        previous_person = ''
        with open(os.path.join(decade, filename)) as infile:
            for line in infile:
                word, _, _, named_entity = line.strip().split("\t")
                if named_entity == 'PERSON':
                    previous_person += ' ' + word
                elif previous_person:
                    decade_counter[previous_person] += 1
                    previous_person = ''
    result.put(decade_counter)

counters = main(sys.argv[1])
person_counter = sum(counters, Counter())
        
top100 = nlargest(100, person_counter.iteritems(), key=lambda i: i[1])
for name, freq in top100:
    print name, freq
