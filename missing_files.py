#!usr/bin/env python

# script to check which files are still missing from the corpus after initial scrape session.

# dependencies:
import re
import os

semicolon = re.compile(r"\;")

def main():
	print "Checking for missing files..."
	# load the lookupkeys for the decade-file specified
	f = open("missing_files.txt", 'w+')
	for decade in ["1920s", "1930s", "1940s", "1950s", "1960s", "1970s", "1980s", "1990s", "2000s"]:
		files_that_we_do_have = os.listdir(os.sep.join(["..", "rich_texts_txt",decade]))
		f.write(decade+": ")
		print(decade)
		decade_file = open(os.sep.join(["..", "lookupkeys", decade+".csv"]), 'r')
		lines = decade_file.readlines()
		decade_file.close()
		# iterate over texts that should be in the decade
		for i in range(1,len(lines)):
			line = lines[i].strip()
			# check the cells
			data_items = semicolon.split(line)
			if len(data_items) != 7:
				continue
			# extract loopupkey
			lookupkey = str(data_items[0])
			if lookupkey+".tag.txt" not in files_that_we_do_have:
				print(lookupkey)
				f.write(lookupkey+", ")
		f.write("\n")
	f.close()
	print("Script terminated...")
	return

if __name__ == "__main__":
	main()
