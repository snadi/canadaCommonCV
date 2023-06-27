INCS=scripts/common.pm
INPUT=input/
OUTPUT=output/

default: $(OUTPUT) createintermediate confs journals

$(OUTPUT):
	mkdir -p $@

journals: $(OUTPUT)journals.xml $(OUTPUT)journals.bib

confs: $(OUTPUT)confs.xml $(OUTPUT)confs.bib
	
createintermediate: input/$(INPUT_BIB) scripts/bib_to_json.py scripts/json_to_dmg.py
	python scripts/bib_to_json.py --bibfile input/$(INPUT_BIB) --outputfile $(OUTPUT)pubs.json
	python scripts/json_to_dmg.py --jsonfile $(OUTPUT)pubs.json

$(OUTPUT)confs.xml: scripts/processConfs.pl $(INCS) $(OUTPUT)confs.txt
	perl $< $(OUTPUT)confs.txt > tmp.tmp && mv tmp.tmp  $@

$(OUTPUT)journals.xml: scripts/processJournals.pl $(INCS) $(OUTPUT)journals.txt
	perl $< $(OUTPUT)journals.txt > tmp.tmp && mv tmp.tmp $@

$(OUTPUT)confs.bib: scripts/txtToLatexConfs.pl $(INCS) $(OUTPUT)confs.txt
	perl $< $(OUTPUT)confs.txt > tmp.tmp && mv tmp.tmp $@

$(OUTPUT)journals.bib:  scripts/txtToLatexJournals.pl $(INCS) $(OUTPUT)journals.txt
	perl $< $(OUTPUT)journals.txt > tmp.tmp && mv tmp.tmp $@

clean:
	rm -f output/*
