from bs4 import BeautifulSoup
import requests, sys, os, codecs, csv, ssl

ssl._create_default_https_context = ssl._create_unverified_context

path = '/Users/mhisten/OneDrive/research/lda/mergent/leftover/'
os.chdir(path)
f = codecs.open('revenue2.csv', 'r', 'utf-8-sig')
reader = csv.reader(f, delimiter=',')

x = 0

for row in reader:
    x = x + 1
    if (x % 100) == 0:
        print('Count: ' + str(x))

    adsh = row[0]
    adsh = adsh.strip()
    url = row[1]
    url = url.strip()
    print(adsh)

    # Obtain HTML for document page
    doc_resp = requests.get(url)
    doc_str = doc_resp.text

    # Find the doc link
    soup = BeautifulSoup(doc_str, 'html.parser')
    table_tag = soup.find('table', class_='tableFile', summary='Document Format Files')
    rows = table_tag.find_all('tr')
    for row in rows:
        cells = row.find_all('td')
        if len(cells) > 3:
            if '10-K' in cells[3].text:
                doc_link = 'https://www.sec.gov' + cells[2].a['href']
                filetype = doc_link[-3:]
                if filetype == 'htm':
                    outfile = open(path + 'rev2link.csv','a')
                    outfile.write(str(adsh) + ',' + doc_link + '\n')
                else:
                    pass


        



