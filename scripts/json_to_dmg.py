import json
import hashlib
import re
import argparse
from bib_to_json import remove_umlauts

fields_to_remove = ["authors_tex"]
fields_to_rename = []
# 'type': 'article' for journal
# 'type': 'inproceedings for conference

types = ['conferences','journals']#,'workshop']
type_dict = {'conferences':'Paper', 'journals':'Paper'}
file_dict = {'conferences':'confs.txt','journals':'journals.txt'}

region_countries = set(['Canada','United States'])

def trim_all(strings):
    return [x.strip() for x in strings]

def bibtex_names(authors):
    if (" and " in authors):
        authors = authors.split(" and ")
    elif (", " in authors):
        authors = authors.split(",")
    else:
        authors = [authors]
    return trim_all(authors)

def get_short_venue(venue):
    if "(" in venue:
        m = re.match(r'^.*\((?P<short>[^\)]+)\).*$', venue)
        if m:
            short = m.group("short")
            return short.replace("-","").replace(" ","")
    return re.sub(r'[^A-Z0-9]','',venue).replace(" ","")

def title_code(title):
    return "".join([x[0] for x in title.split(" ") if len(x) > 0]).lower()

def generate_id(entry):
    if "id" in entry:
        return entry["id"]
    author = bibtex_names(entry['authors'])[0].lower().split(" ")[0]
    year   = str(entry['year'])
    venue  = get_short_venue(entry['venue'])
    #myhash = hashlib.sha224(entry['title'] + entry['venue']).hexdigest()[0:3]
    tcode = title_code(entry['title'])
    return author+year+venue+tcode

def record_id(idkey):
    return hashlib.sha224(idkey.encode('utf-8')).hexdigest()[0:32]

def conference_date(entry):
    check = ["DateConf","dateconf","date","published","year"]
    for key in check:
        if key in entry:
            if key == "date":
                if "/" in entry[key]:
                    parts = entry[key].split('/')
                    return ("%s-%s-1" % (parts[0], parts[1]))
            if key == "year":
                if 'month' in entry:
                    return "%s-%s-1" % (entry[key], entry['month'])
                else:
                    return "%s-01-01" % entry[key]
            return entry[key]
    raise Exception("No Conf date in entry")

def entry_date(entry):
    # Note sure why but there are two dates
    # one that is Date = month/year
    # and one that is Conference Date = year-month-year
    check = ["date","DateConf","dateconf","published","year"]
    for key in check:
        if key in entry:
            if key == "date" or key == "dateconf":
                if "-" in entry[key]:
                    parts = entry[key].split("-")
                    return "%s/%s" % (parts[0], parts[1])                    
            if key == "year":
                return str(entry[key])+"/1"
            if key == "published":
                parts = entry[key].split("-")
                return "%s/%s" % (parts[0], parts[1])
            return entry[key]
    raise Exception("No Dates in entry")

def conference_city_and_country(entry):
    l = entry['location'].split(", ")
    city = l[0]
    country = l[-1]
    return (city, country)
def conference_city(entry):
    city, country = conference_city_and_country(entry)
    return city

def conference_country(entry):
    city, country = conference_city_and_country(entry)    
    return country

def bold_authors(entry):
    if "Authors" in entry:
        return entry["Authors"]
    if "authors_tex" in entry:
        authors = entry["authors_tex"]
        authors = re.sub(r'\\\'{a}',r'a',authors)
        authors = re.sub(r'\\\'{e}',r'e',authors)
        authors = re.sub(r'\\"{u}', r'ue', authors)
        authors = re.sub(r'\\"{o}', r'oe', authors)
        authors = re.sub(r'\\"{a}',r'ae',authors)
        authors = re.sub(r'\\student{([^}]+)}',r'<b>\1</b>',authors)
        authors = re.sub(r'\\HQP{([^}]+)}',r'<b>\1*</b>',authors)
        return authors
    else:
        return entry["authors"]

def get_note(pub):
    if 'notes' in pub:
        return pub['notes']
    if 'rate' in pub:
        return pub['rate']
    
    return None

def process(pubs):
    seen_ids = set()
    pcount = 0
    for pub_type in types: #pubs.keys():
        ppubs = pubs[pub_type]
        allpubs = []
        for pub in ppubs:
            opub = dict()
            opub['Title'] = pub['title']
            opub['Date'] = entry_date(pub)
            if not pub_type == "journals":
                # conference
                opub['Type'] = type_dict[pub_type]
                opub['Conference'] = pub['venue']
                opub['DateConf'] = conference_date(pub)
                if 'location' in pub:
                    #opub['City'] = conference_city(pub)
                    opub['City'] = pub['location']
                    opub['Country'] = conference_country(pub)
                else:
                    opub['City'] = " "
                    opub['Country'] = " "
                #print(opub['Country'])
                opub['PublishedIn'] = " " # pub['venue'][0:99]
            note = get_note(pub)
            if note:
                opub['Note'] = note
            opub['PublishingStatus']=pub.get('publishingstatus',"Published")
            opub['Refereed'] = pub.get("refereed","Yes")
            opub['Authors'] = bold_authors(pub)
            opub['Publisher'] = pub.get("publisher"," ")
            opub['DOI'] = pub.get("doi"," ")
            #opub['Role'] = pub.get("role"," ")
            opub['URL'] = pub.get("url"," ")
            opub['dmgKey'] = pub.get('id',generate_id(pub))
            if 'region' in pub:
                opub['Region'] = pub['region']
            if 'Country' in opub and opub['Country'] in region_countries and 'Region' not in opub:
                raise Exception("We need a region (province/state) ! %s \n%s" % (opub['dmgKey'],pub))                        
            if opub['dmgKey'] in seen_ids:
                raise Exception("We've seen %s before!\n%s" % (opub['dmgKey'],pub))
            # else:
            #     print(opub['dmgKey'])
            seen_ids.add(opub['dmgKey'])
            opub['recordId'] = record_id(opub['dmgKey'])
            if pub_type == 'journals' and not 'journal' in pub:
                pub['journal'] = pub['venue']
                opub['Journal'] = pub['journal']
                opub['OpenAccess'] = pub.get('openaccess','No')
                if 'issue' in pub:
                    pub['issue'] = str(pub['issue'])
                    opub['Issue'] = pub['issue']
                if 'volume' in pub:
                    opub['Volume'] = pub['volume']
                if 'number' in pub:
                    opub['Issue'] = pub['number']
                
            if 'pages' in pub:
                pub['pages'] = str(pub['pages'])
                pub['Pages'] = pub['pages']            
            if 'pagerange' in pub:
                opub['PageRange'] = pub['pagerange']
            elif 'pages' in pub:
                opub['PageRange'] = "1--%s" % pub["Pages"]
            pub['year'] = str(pub['year'])
            for field in fields_to_remove:
                if field in pub:
                    del(pub[field])
            allpubs.append(opub)
            pcount += 1
        filename = file_dict[pub_type]
        with open(f"output/{filename}", 'w') as fd:
            fd.write("# dmg style file: %s\n" % filename)
            for pub in allpubs:
                key = "recordId"
                fd.write("%s=%s\n" % (key,pub[key]))
                for key in pub.keys():
                    if not "recordId" == key:
                        fd.write("%s=%s\n" % (key,pub[key]))
                fd.write("\n")

if __name__ == "__main__":
    # mypubs.init_logging()
    # get first command-line argument
    parser = argparse.ArgumentParser()
    parser.add_argument('--jsonfile')
    args = parser.parse_args()
    pubs = json.load(open(args.jsonfile))
    
    process(pubs)