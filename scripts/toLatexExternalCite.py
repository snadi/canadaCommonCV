import argparse
import json
from pybtex.database import parse_file

def parseCCVEntries(ccvfile):
    ccv_data = {}
    with open(ccvfile, 'r') as f:
        #read each line and split by ;
        for line in f:
            line = line.strip().strip('.')
            line = line.split(';')
            # key is title and value is the CCV ref
            ccv_data[line[1]] = line[0]

    return ccv_data

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--bibfile')
    parser.add_argument('--ccvfile')
    args = parser.parse_args()

    bib_data = parse_file(args.bibfile)
    ccv_data = parseCCVEntries(args.ccvfile)

    for bib_entry in bib_data.entries.values():
        papertitle = bib_entry.fields['title']

        if papertitle not in ccv_data:
            continue
        ccv_ref = ccv_data[papertitle]
        refkey = bib_entry.key
        print(fr"\bibcite{{{refkey}}}{{{ccv_ref}}}")

if __name__ == "__main__":
    main()