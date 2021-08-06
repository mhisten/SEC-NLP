
from bs4 import BeautifulSoup
import os, sys, csv, re, csv, codecs, requests, ssl, pickle, boto3
from urllib.request import urlopen
from time import sleep
from random import randint

ssl._create_default_https_context = ssl._create_unverified_context
bucket = 'lda10k'
#pull boto access

path1 = '/home/ubuntu/'
os.chdir(path1)


file1 = '2018.csv'
#file2 = '2018url.pkl'

url1 = 'https://www.sec.gov/cgi-bin/srch-edgar?text='
url2 = '&first=2000&last=2020'
url3 = 'https://www.sec.gov'

key1 = '2018url'
urldata = []

x = 0

f = codecs.open(file1, 'r', 'utf-8-sig')
reader = csv.reader(f, delimiter=',')

x = 0 # counter
z = 250 # save file every

for row in reader:

    sleep(randint(3, 7))

    x = x + 1
    if (x % 50) == 0:
        print('Count: ' + str(x))

    adsh = str(row[0])
    print(adsh)
    url = url1 + adsh + url2
    page = urlopen(url).read()

    soup = BeautifulSoup(page, "lxml")
    soup = soup.findAll('table')
    for table in soup:
        table1 = str(table)
        if '10-K' in table1:
            soup1 = table.findAll('tr')
            for line in soup1:
                line1 = str(line)
                if '10-K' in line1:
                    soup2 = line.findAll('a', {'href': re.compile('^/Archives/')})
                    for potato in soup2:
                        potato1 = str(potato)
                        if '[text]' in potato1:
                            potato1 = potato1.split('"')
                            potato1 = url3 + str(potato1[1])
                            urldata.append(str(adsh) + ',' + potato1)

    if (x % z) == 0:

        print('Pickling...')

        pickle1 = pickle.dumps(urldata) 

        y = x / z
        y = int(y)

        key11 = str(key1) + str(y) + '.pkl'

        s3_resource = boto3.resource('s3', aws_access_key_id=ACCESS_ID, aws_secret_access_key= ACCESS_KEY)
        s3_resource.Object(bucket,key11).put(Body=pickle1)

        urldata = []

pickle1 = pickle.dumps(urldata) 

key11 = str(key1) + str('Fin') + '.pkl'

s3_resource = boto3.resource('s3', aws_access_key_id=ACCESS_ID, aws_secret_access_key= ACCESS_KEY)
s3_resource.Object(bucket,key11).put(Body=pickle1)








