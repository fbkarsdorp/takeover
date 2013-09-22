#!usr/bin/env python

from optparse import OptionParser
import xml.dom.minidom
import os, re

# from command line:
# python -u xml2txt.py --decade="1920s"

extension = re.compile(r"\.xml")

def main():
	print "Starting conversion from xml to txt..."
	# parse the options
	usage = "usage: %prog [options] arg1 arg2"
	parser = OptionParser(usage)
	parser.add_option("-d", "--decade", dest="decade", default="test")
	(options, args) = parser.parse_args()
	print "Extracting decade: "+options.decade
	# whether whether the relevant output dirs exist; create them if not
	if not os.path.isdir(os.sep.join(["..", "rich_texts_txt"])):
		os.mkdir(os.sep.join(["..", "rich_texts_txt"]))
	if not os.path.isdir(os.sep.join(["..", "rich_texts_txt",options.decade])):
			os.mkdir(os.sep.join(["..", "rich_texts_txt",options.decade]))
	else:
		# delete the content of the file if it already existed
		for fi in os.listdir(os.sep.join(["..","rich_texts_txt",options.decade])):
			os.remove(os.sep.join(["..","rich_texts_txt",options.decade,fi]))
	for root, dirs, files in os.walk("..","rich_texts_xml/"+options.decade):
		for f_obj in files:
			if not f_obj.endswith(".xml"):
				continue
			f_name = extension.sub("",f_obj)
			try:
				doc = xml.dom.minidom.parse(os.sep.join(["..","rich_texts_xml",options.decade,f_obj]))
				doc_txt = open(os.sep.join(["..","rich_texts_txt",options.decade,f_name+".txt"]),'w+')
				token_list = doc.getElementsByTagName('word')
				lemma_list = doc.getElementsByTagName('lemma')
				pos_list = doc.getElementsByTagName('POS')
				ner_list = doc.getElementsByTagName('NER')
				if len(token_list) == len(lemma_list) == len(pos_list) == len(ner_list):
					for i in range(len(token_list)):
						try:
							token = str(token_list[i].firstChild.nodeValue)
							lemma = str(lemma_list[i].firstChild.nodeValue)
							pos = str(pos_list[i].firstChild.nodeValue)
							ner = str(ner_list[i].firstChild.nodeValue)
							doc_txt.write("\t".join([token,lemma,pos,ner]))
							doc_txt.write("\n")
						except UnicodeEncodeError:
							pass
				doc_txt.close()
			except IOError:
				# unable to retrieve file
				pass
	print "Conversion terminated!"
	return

if __name__ == "__main__":
	main()