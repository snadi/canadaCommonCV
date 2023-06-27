from pybtex.database import parse_file
import argparse
import json
from hqp import hqp, students

# fill with your own HQP names
hqp = ["Amann, Sven", 
            "Proksch, Sebastian", 
            "Cergani, Ervina",
            "Masri, Samer Al", 
            "Mahmoudi, Mehran", 
            "de la Mora, Fernando Lopez", 
            "Radu, Aida", 
            "Kareshk, Moein Owhadi", 
            "Bhuiyan, Nazim Uddin", 
            "Jha, Ajay Kumar", 
            "El-Hajj, Rehab", 
            "Kamath, Ram", 
            "Tang, Henry", 
            "Nuryyev, Batyr", 
            "Galappaththi, Akalanka", 
            "Nguyen, Nhan", 
            "Gulami, Mansur", 
            "Ellis, Max", 
            "Islam, Mohayeminul"]

students = ["Lin, Changyuan",
            "Soni, Abhishek",
            "Soares, Larissa Rocha"]

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

def process_acceptance(addendum):
    # input format is Acceptance Ratio: 12/30 = 40\%
    # return "12/30 = 40%"
    return addendum.split(":")[1].strip().replace("\%","%")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--bibfile')
    args = parser.parse_args()

    bib_data = parse_file(args.bibfile)

    jsondata = {}
    jsondata['journals'] = []
    jsondata['conferences'] = []

    for entry in bib_data.entries.keys():
        paper = bib_data.entries[entry]
        jsonentry = {}
        
        jsonentry['authors_tex'] = process_authors(paper.persons['author'], tex=True)
        jsonentry['authors'] = process_authors(paper.persons['author'])

        #keys with same name in bib and json format
        for key in ['title', 'year', 'publisher', 'doi', 'city', 'country', 'volume']:
            if key in paper.fields:
                jsonentry[key] = paper.fields[key]
                
        if 'pages' in paper.fields:
            jsonentry['pagerange'] = paper.fields['pages']

        if 'addendum' in paper.fields:
            jsonentry['rate'] = process_acceptance(paper.fields['addendum'])

        jsonentry['PublishingStatus'] = 'Published' # assumption is entries appearing in bib file are published

        if paper.type == 'article': # journal specific values
            jsonentry['venue'] = paper.fields['journal']
            jsondata['journals'].append(jsonentry)
        elif paper.type == 'inproceedings': # conference specific values
            jsonentry['venue'] = paper.fields['booktitle']
            jsondata['conferences'].append(jsonentry)

    print(json.dumps(jsondata, indent=4))

if __name__ == "__main__":
    main()