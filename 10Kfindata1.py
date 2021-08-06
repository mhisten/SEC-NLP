import os

path1 = '/Users/mhisten/OneDrive - The College of Wooster/research/lda/manipulated1/'
path2 = '/Users/mhisten/OneDrive - The College of Wooster/research/lda/cleaned2'

os.chdir(path1)

lineitem0 = 'Assets'
lineitem0 = lineitem0.lower()

txtout_file = "assets2.txt"

for filename in os.listdir(path1):
    with open(filename, "rb") as f:
        if filename != '.DS_Store':
            print(filename)
            lines = [l.decode('utf8', 'ignore') for l in f.readlines()]
            for m in lines:
                    n = m.split()
                    if n[0] == 'adsh':
                        pass
                    else:

                        coreg = n[3]

                        if coreg.isnumeric(): # no coreg
                            adsh = n[0]
                            tag = n[1]
                            tag = tag.lower()
                            year = n[3]
                            qtr = n[4]
                            currency = n[5]
                            try:
                                value = n[6]
                            except:
                                value = 0
                        else:
                            pass

                        if tag == lineitem0:
                            if qtr == str(0): #for balance sheet, 0; for income statement, 4
                                outfile = open(path2 + '/' + txtout_file,'a')
                                outfile.write(str(adsh) + ',' + str(tag) + ',' + str(year) + ',' + str(qtr) + ',' + str(currency) + ',' + str(value) + '\n') 



