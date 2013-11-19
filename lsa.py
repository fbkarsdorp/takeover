import logging
from gensim import corpora, models, matutils, similarities

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', 
	                level=logging.INFO)

dictionary = corpora.dictionary.Dictionary.load(sys.argv[1])
corpus = corpora.MmCorpus(sys.argv[2])

lsi = models.lsimodel.LsiModel(
	corpus=corpus, dictionary=dictionary, num_topics=300)

termcorpus = matutils.Dense2Corpus(lsi.projection.u.T)
index = similarities.MatrixSimilarity(termcorpus)

references = set([line.strip() for line in open(sys.argv[3])])

def get_similarities(query, references):
	sims = index[query]
	return [(dictionary.id2word(other), sim) for other, sim in enumerate(sims)
	        if dictionary.id2word(other) in references]

for reference in references:
	print get_similarities(reference, references)

