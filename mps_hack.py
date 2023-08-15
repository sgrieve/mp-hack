from mediawiki import MediaWiki
from bs4 import BeautifulSoup
import pandas as pd
import re
import json
import spacy
import requests

def clean_uni(uni):
    '''
    Fixing a bunch of issues when we scrape university names from wikipedia
    '''
    uni = re.sub(r'\([^)]*\)', '', uni)  # Remove information in brackets eg "(BSc)"
    uni = re.sub(r'\[[^)]*\]', '', uni)  # Remove footnote links in square brackets
    uni = uni.replace('  ', '')  # Strip extra whitespace due to the above steps
    uni = re.sub(r'([a-z](?=[A-ZÉ])|[A-Z](?=[A-Z][a-z]))', r'\1|', uni)  # Find word boundaries that are missing a space
    uni = uni.replace('Academyof', 'Academy of')  # Deidre Brock has a line break here so we need to force a space
    uni = uni.replace('Glasgow Harvard', 'Glasgow|Harvard')  # John Nicholson breaks the formatting so fixing here
    uni = uni.strip() # Strip out any leading or trailing whitespace

    uni_split = uni.split('|')
    return uni_split

def get_mp_list(cached=False):
    '''
    Set cached to true to not download the latest mp list

    The cached version has been edited to correct differences in names between
    theyworkforyou and wikipedia - eg jnr vs jr, chris vs christopher
    '''
    if not cached:
        r = requests.get('https://www.theyworkforyou.com/mps/?f=csv')
        with open('mps.csv', 'w') as w:
            w.write(r.text)


# Set up spacy and MediaWiki
nlp = spacy.load('en_core_web_sm')
wikipedia = MediaWiki()

get_mp_list(True)
mps = pd.read_csv('mps.csv')
names = mps['First name'] + ' ' +  mps['Last name']

uk = ['List of MPs for constituencies in England (2019–present)',
      'List of MPs for constituencies in Scotland (2019–present)',
      'List of MPs for constituencies in Northern Ireland (2019–present)',
      'List of MPs for constituencies in Wales (2019–present)']
outnames = ['english_mps.json','scottish_mps.json', 'ni_mps.json', 'welsh_mps.json']

for i, country in enumerate(uk):

    main_list = wikipedia.page(country)

    soup = BeautifulSoup(main_list.html, 'html.parser')

    mp_uni = {}

    for name in names:
        title = None

        try:
            mp_data = {}
            # There are multiple tables in the english data
            mp_tables = soup.find_all('table', {"class": "wikitable sortable"})

            # This checks all of the tables in the wiki page until it finds a match
            # in the case of non english MPs, there is only 1 table.
            # In cases where no matches are found 'title' will be undefined and
            # this exception is caught with the outer try/except
            for mp_table in mp_tables:
                if mp_table.find('a', {'title': re.compile(name+'*')}):
                    title = mp_table.find('a', {'title': re.compile(name+'*')}).attrs['title']
                    print(name, 'found', country)
                    break

            p = wikipedia.page(title, auto_suggest=False)

            mp_soup = BeautifulSoup(p.html, 'html.parser')

            table = mp_soup.find('table', {'class': 'infobox vcard'})

            df = pd.read_html(str(table), index_col=0)[0]

            try:
                mp_data['unis'] = '|'.join(clean_uni(df.T['Alma mater'][0]))
                mp_data['sentence'] = ''

                # grab the text from the wiki page
                content = nlp(p.content)

                # Need to format and split up these uni names for those that did multiple degrees
                for uni_name in clean_uni(mp_data['unis']):
                    for sent in content.sents:
                        if uni_name in sent.text:
                            mp_data['sentence'] += sent.text.strip()

                if len(mp_data['sentence']) == 0:

                    # Trying to catch situations where eg 'university of glasgow' is listed as 'glasgow university'
                    for sent in content.sents:
                        if 'niversity' in sent.text:
                            mp_data['sentence'] += sent.text.strip()

                if len(mp_data['sentence']) == 0:
                    mp_data['sentence'] = 'No Data'

            except:
                mp_data['unis'] = 'No Data'
                mp_data['sentence'] = 'No Data'

            # Changed her name after joining parliament
            if name == 'Kate Griffiths':
                name = 'Kate Kniveton'

            mp_uni[name] = mp_data

        except:

            # David Simmonds is the only MP to not have the MP template on wikipedia
            if name == 'David Simmonds':
                mp_data['unis'] = 'Durham University|Birkbeck, University of London'
                mp_data['sentence'] = 'No Data'
                mp_uni[name] = mp_data
            else:
                print(name, 'not found')

    with open(outnames[i], 'w') as f:
         f.write(json.dumps(mp_uni, indent=4, ensure_ascii=False))
