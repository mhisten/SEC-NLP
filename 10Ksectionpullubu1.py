from bs4 import BeautifulSoup
import os, sys, csv, re, csv, codecs, requests, ssl, boto3, pickle
from urllib.request import urlopen

section = 'Item 1A'
next_section = 'Item 1B'
ssl._create_default_https_context = ssl._create_unverified_context

path1 = '/home/ubuntu/'

os.chdir(path1)
file1 = '2015.csv'
file2 = 'smallerreporting.csv'
exceptions = []

bucket1 = 'processed1'
#pull boto access

count = 0

f = codecs.open(file1, 'r', 'utf-8-sig')
reader = csv.reader(f, delimiter=',')

for row in reader:
    
    try:
        count = count + 1
        if (count % 50) == 0:
            print('Count: ' + str(count))

        adsh = str(row[0])
        print(adsh)
        url = str(row[1])

        page = urlopen(url).read()

        # Pre-processing the html content by removing extra white space and combining then into one line.
        page = page.strip()  
        page = page.replace(b'\n', b' ')  
        page = page.replace(b'\r', b'')  
        page = page.replace(b'&nbsp;', b' ')  
        page = page.replace(b'&#160;', b' ') 

        while b'  ' in page:
            page = page.replace(b'  ', b' ')  

        sub = "Item 1A"
        sub2 = "Item 1B"
        sub3 = "Item 2"
        page1 = str(page)
        soup = BeautifulSoup(page1, "html.parser") 
        rawText1 = soup.text.encode('utf8') 
        rawText1 = str(rawText1)
        outText1 = rawText1.strip()
        page2 = str(outText1)

        # Pre-processing of cleaned content by removing extra html phrases.
        page2 = page2.replace('\\xe2',' ')
        page2 = page2.replace('\\x80',' ')
        page2 = page2.replace('\\xa2',' ')
        page2 = page2.replace('\\x9d',' ')
        page2 = page2.replace('\\x96',' ')
        page2 = page2.replace('\\xaa',' ')
        page2 = page2.replace('\\x9c',' ')
        page2 = page2.replace('\\x94',' ')
        page2 = page2.replace('\\x99',' ')
        page2 = page2.replace('\\x93',' ')
        page2 = page2.replace('\\x8b',' ')
        page2 = page2.replace('\\xa0',' ')
        page2 = page2.replace('\\xc2',' ')
        page2 = page2.replace('\\x84',' ')
        page2 = page2.replace('\\xb7',' ')
        page2 = page2.replace('\\\\t',' ')
        page2 = page2.replace('\\x97',' ')
        page2 = page2.replace('\\x8f',' ')
        page2 = page2.replace('\\xae',' ')
        page2 = page2.replace('\\xef',' ')
        page2 = page2.replace('\\xbb',' ')
        page2 = page2.replace('\\xbf',' ')
        page2 = page2.replace('\\x83',' ')

        while '  ' in page2:
            page2 = page2.replace('  ', ' ')  

        #Begin
        length1 = []
        length1 = re.findall(sub,page2, flags=re.IGNORECASE)
        position1 = []
        for m in re.finditer(sub,page2, flags=re.IGNORECASE):
            position1.append(m.start())

        #End
        lenth2 = []
        length2 = re.findall(sub2,page2, flags=re.IGNORECASE)
        position2 = []
        for m in re.finditer(sub2,page2, flags=re.IGNORECASE):
            position2.append(m.start())

        begin = 'a' # Give error if no start
        for item in position1: #find start
            check0 = 0
            check1 = page2[item + 8:item + 2000] # Skip index
            check2 = page2[item:item + 25] # Check if it's a reference
            check3 = page2[item - 25:item] # Check if it's a reference

            if 'risk factors' not in str(check2).lower():
                pass
            else:
                if 'item 1.' in str(check1).lower():
                    pass
                else:
                    if 'mine safety disclosures' in str(check1).lower():
                        check0 = check0 + 1
                    if 'legal proceedings' in str(check1).lower():  
                        check0 = check0 + 1
                    if 'unresolved staff comments' in str(check1).lower():     
                        check0 = check0 + 1
                    if 'selected financial data' in str(check1).lower(): 
                        check0 = check0 + 1
                    if check0 >= 2:
                        pass
                    else: 
                        check0 = 0
                        if 'refer to' in str(check3).lower():
                            check0 = check0 + 1
                        if 'section entitled' in str(check3).lower():
                            check0 = check0 + 1
                        if ' see ' in str(check3).lower():
                            check0 = check0 + 1
                        if check0 >=1:
                            pass

                        else:
                            begin = item
                            break

        finish = 'a' # Give error if no finish
        for item2 in position2: #find end
            if begin > item2:
                pass
            else: 
                finish = item2

        if finish == 'a': #if no section 1B
            position3 = []
            for m in re.finditer(sub3,page2, flags=re.IGNORECASE):
                position3.append(m.start())
            
            for item4 in position3: #find end
                if begin > item4:
                    pass
                else: 
                    finish = item4

        for item3 in position1: #pull last occurence before finish
            if item3 < begin:
                pass
            else:
                if item3 < finish:
                    check0 = 0
                    check1 = page2[item3:item + 25] # Check reference again

                    if 'risk factors' not in str(check1).lower():
                        pass
                    else: begin = item3

                else:
                    break

        page0 = page2[begin:finish] #collect document

        if len(page0) > 1000:
            s3_resource = boto3.resource('s3', aws_access_key_id=ACCESS_ID, aws_secret_access_key= ACCESS_KEY)
            s3_resource.Object(bucket1,(adsh + '.txt')).put(Body=page0)


        else: # Check is smaller reporting company
            pass
            '''
            check0 = 0
            if 'smaller reporting company' in str(page0).lower():
                check0 = check0 + 1
            if 'not required' in str(page0).lower():
                check0 = check0 + 1
            if 'not applicable' in str(page0).lower():
                check0 = check0 + 1
            if check0 >=1:
                check0 = check0 + 1

            if check0 >=1:
                exceptions.append(adsh)
            '''
        # clear memory
        page0 = []
        page1 = []
        page2 = []

    except:
        pass

'''
pickle = pickle.dumps(exceptions) 
s3_resource = boto3.resource('s3', aws_access_key_id=ACCESS_ID, aws_secret_access_key= ACCESS_KEY)
s3_resource.Object(bucket1,file2).put(Body=pickle)
'''