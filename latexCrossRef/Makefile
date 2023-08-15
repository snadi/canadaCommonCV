default: ccv_references.aux

CCV=ccv-nserc
INPUT_CCV_PDF=$(CURDIR)/../input/$(CCV).pdf
BIB=$(CURDIR)/../input/$(INPUT_BIB)

ccvReferences.txt: ../scripts/extractIndexes.rb $(CCV).txt
	ruby $< $(CCV).txt > ccvReferences.txt

$(CCV).txt: $(INPUT_CCV_PDF)
	pdftotext $(INPUT_CCV_PDF) $@

ccv_references.aux: ../scripts/toLatexExternalCite.py ccvReferences.txt $(BIB)
	python ../scripts/toLatexExternalCite.py --bibfile $(BIB) --ccvfile ccvReferences.txt > $@

clean:
	rm -f ccvReferences.txt ccv_references.aux
