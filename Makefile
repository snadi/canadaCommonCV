INCS=scripts/common.pm

default: creatdir confs journals

creatdir:
	rm -rf output/*
	mkdir -p output

journals: journals.xml journals.bib

confs: confs.xml confs.bib

confs.xml: scripts/processConfs.pl $(INCS) input/confs.txt
	perl $< input/confs.txt > tmp.tmp && mv tmp.tmp  output/$@

journals.xml: scripts/processJournals.pl $(INCS) input/journals.txt
	perl $< input/journals.txt > tmp.tmp && mv tmp.tmp  output/$@

confs.bib: scripts/txtToLatexConfs.pl $(INCS)  input/confs.txt
	perl $< input/confs.txt > tmp.tmp && mv tmp.tmp  output/$@

journals.bib:  scripts/txtToLatexJournals.pl $(INCS) input/journals.txt
	perl $< input/journals.txt > tmp.tmp && mv tmp.tmp  output/$@

clean:
	rm -f output/journals.bib output/confs.bib output/journals.xml output/confs.xml

bibs:	output/confs.bib output/journals.bib

xmls:   output/confs.xml output/journals.xml
