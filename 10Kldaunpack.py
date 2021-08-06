import os, pickle, pandas, csv

path1 = '/Users/mhisten/OneDrive/research/lda/regressions/take2/equity/emonograms/25/'
path2 = '/Users/mhisten/OneDrive/research/lda/regressions/take2/equity/emonograms/25/'

os.chdir(path1)


adshdata = []
reader1 = csv.reader(open(path2 + 'adsh.csv', 'r'))
for row in reader1:
    adshdata.append(row[0])

file2 = 'adsh1.csv'

'''
file1 = 'adsh.pkl'
file2 = 'adsh.csv'

file1 = pandas.read_pickle(file1) 


for line in file1:
    #print(line)
    outfile = open(file2,'a')
    outfile.write(str(line) + '\n')
'''


count = 0
vertical = []
for line in file1:
    horizontal = []
    adsh = adshdata[count]
    horizontal.append(adsh)

    for item in line:
        item = str(item)
        item = item.replace('(','')
        item = item.replace(')','')
        item = item.replace(' ','')
        item = item.replace(',',':')
        horizontal.append(item)
    vertical.append(horizontal)
    count = count + 1

    outfile = open(file2,'a')
    outfile.write(str(horizontal) + '\n')

'''
topics = 25
for item in vertical:
    adsh = item[0]
    tracker = 1

    #print(item[1])
    horizontal1 = []
    horizontal1.append(adsh)
    for topic in range(topics):
        if tracker > (len(item) - 1):
            tracker = 1

        item2 = str(item[tracker]).split(':')


        if int(item2[0]) == topic:
            item3 = str(item[tracker])
            item3 = item3.replace(':',',')
            horizontal1.append(item3)
            tracker = tracker + 1
        else: 
            horizontal1.append(str(topic) + ',0')

    outfile = open(file2,'a')
    outfile.write(str(horizontal1) + '\n')
'''




'''
for filename in os.listdir(path1):
    if filename != '.DS_Store':
        file1 = pandas.read_pickle(filename) 
        file2 = str(filename[:-4]) + '.csv'
        for line in file1:
            outfile = open(file2,'a')
            outfile.write(str(line) + '\n')

'''
'''
for filename in os.listdir(path1):
    with open(filename, "r") as f:
        if filename != '.DS_Store':
            print(filename[:-4])
'''







