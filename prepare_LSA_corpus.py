
import cPickle
import sys

from gensim.corpora import TextCorpus, MmCorpus

def identity(x): return x

def get_words(text, cond, pos):
	return [elt[pos] for elt in text if cond(elt)]

class TIMECorpus(TextCorpus):
	def __init__(self, input=None):
		TextCorpus.__init__(self, input)

	def get_texts(self, cond=identity, pos=0):
		length = 0
		with open(self.input) as infile:
    		while True:
	    		try:
		            (decade, year, filename, text) = cPickle.load(infile)
        			length += 1
		        	yield get_words(text)
		        except EOFError:
		        	break
		self.length = length

if __name__ == '__main__':
	root = sys.argv[1]
	corpus = TIMECorpus(root)
    corpus.dictionary.save("TIME.dict")
    MmCorpus.serialize("TIME.mm", corpus)

