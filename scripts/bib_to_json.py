from pybtex.database import parse_file
import argparse
import json
import re
from hqp import hqp, students

def remove_umlauts(author):
    author = re.sub(r'\\\'{a}',r'ae',author)
    author = re.sub(r'\\"{a}',r'ae',author)
    author = re.sub(r'\\"{o}',r'oe',author)
    author = re.sub(r'\\"{u}',r'ue',author)
    return author

def process_authors(authors, tex=False):
    author_list = []
    for author in authors:
        author = str(author)
        if tex and author in hqp:
            author_list.append("\\HQP{%s}" % author)
        elif tex and author in students:
            author_list.append("\\student{%s}" % author)
        else:
            author_list.append(author)
    return ' and '.join(author_list)

def process_addendum(addendum):
    # input format is Acceptance Ratio: 12/30 = 40\%
    # this could also be an impact factor "Impact: 4.2"
    addendum = addendum.strip().replace("\\%","%")
    if addendum.endswith(")"):
        addendum = addendum[:-1]
    if addendum.startswith("("):
        addendum = addendum[1:]
    return addendum


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--bibfile')
    parser.add_argument('--outputfile')
    args = parser.parse_args()

    bib_data = parse_file(args.bibfile)

    jsondata = {}
    jsondata['journals'] = []
    jsondata['conferences'] = []

    for key in bib_data.entries.keys():
        paper = bib_data.entries[key]
        jsonentry = {}

        jsonentry["id"] = key
        
        jsonentry['authors_tex'] = process_authors(paper.persons['author'], tex=True)
        jsonentry['authors'] = process_authors(paper.persons['author'])

        #keys with same name in bib and json format
        for key in ['title', 'year', 'publisher', 'doi', 'city', 'country', 'volume', 'number']:
            if key in paper.fields:
                jsonentry[key] = paper.fields[key]
                
        if 'pages' in paper.fields:
            jsonentry['pagerange'] = paper.fields['pages']

        if 'addendum' in paper.fields:
            jsonentry['notes'] = process_addendum(paper.fields['addendum'])
        
        if 'status' in paper.fields:
            jsonentry['publishingstatus'] = paper.fields['status']
        else:
            # assumption is entries appearing in bib file are published, 
            # unless another explicit status is given
            jsonentry['publishingstatus'] = 'Published' 

        if paper.type == 'article': # journal specific values
            jsonentry['venue'] = paper.fields['journal']
            jsondata['journals'].append(jsonentry)

            if 'addendum' in paper.fields:
                jsonentry['impact'] = process_addendum(paper.fields['addendum'])
        elif paper.type == 'inproceedings': # conference specific values
            jsonentry['venue'] = paper.fields['booktitle']
            jsondata['conferences'].append(jsonentry)
            jsonentry['dateconf'] = paper.fields['dateconf']

            

    with open(args.outputfile, 'w') as outfile:
        json.dump(jsondata, outfile, indent=4)

if __name__ == "__main__":
    main()