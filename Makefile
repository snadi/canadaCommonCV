INCS=scripts/common.pm
INPUT=input/
OUTPUT=output/

default: $(OUTPUT) processedfiles confs journals rmtmpfiles

$(OUTPUT):
	mkdir -p $@

processedfiles: $(OUTPUT)confs.txt $(OUTPUT)journals.txt

journals: $(OUTPUT)journals.xml $(OUTPUT)journals.bib

confs: $(OUTPUT)confs.xml $(OUTPUT)confs.bib

$(OUTPUT)pubs.json: input/$(INPUT_BIB) bib_to_json.py
	python bib_to_json.py --bibfile input/$(INPUT_BIB) > $@

$(OUTPUT)confs.txt $(OUTPUT)journals.txt: $(OUTPUT)pubs.json json_to_dmg.py
	python json_to_dmg.py --jsonfile $(OUTPUT)pubs.json

$(OUTPUT)confs.xml: scripts/processConfs.pl $(INCS) processedfiles
	perl $< $(OUTPUT)confs.txt > tmp.tmp && mv tmp.tmp  $@

$(OUTPUT)journals.xml: scripts/processJournals.pl $(INCS) processedfiles
	perl $< $(OUTPUT)journals.txt > tmp.tmp && mv tmp.tmp $@

$(OUTPUT)confs.bib: scripts/txtToLatexConfs.pl $(INCS) processedfiles
	perl $< $(OUTPUT)confs.txt > tmp.tmp && mv tmp.tmp $@

$(OUTPUT)journals.bib:  scripts/txtToLatexJournals.pl $(INCS) processedfiles
	perl $< $(OUTPUT)journals.txt > tmp.tmp && mv tmp.tmp $@

rmtmpfiles:
	rm -f $(OUTPUT)*.txt $(OUTPUT)*.json

clean:
	rm -f output/*

bibs:	$(OUTPUT)confs.bib $(OUTPUT)journals.bib

xmls:   $(OUTPUT)confs.xml $(OUTPUT)journals.xml
