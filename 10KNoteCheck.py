import os, re, shutil

path1 = '/Users/mhisten/OneDrive - The College of Wooster/research/lda/Note/raw2015/'
path2 = '/Users/mhisten/OneDrive - The College of Wooster/research/lda/Note/processed/'

text = 'Item 1A'
text = text.lower()

os.chdir(path1)

for filename in os.listdir(path1):
    with open(filename, "r") as f:
        if filename != '.DS_Store':
            #print(filename)
            filename1 = f.read()
            length1 = []
            length1 = re.findall(text,filename1, flags=re.IGNORECASE)
            size = len(length1)
            if size == 1:
                shutil.move(path1 + '/' + filename, path2 + '/' + filename)
            else:
                x = 0
                y = 0
                for item in re.finditer(text,filename1, flags=re.IGNORECASE):
                    if str(item.group()) == "Item 1A":
                        x = x + 1
                    if str(item.group()) == "ITEM 1A":
                        y = y + 1
                        z = item.start()
                if y == 1 and x >= 1:
                    outfile = open(path2 + '/' + filename,'a')
                    outfile.write(filename1[z:])
                    os.remove(filename)



            


