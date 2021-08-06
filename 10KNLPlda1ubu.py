import sys, os, nltk, re, pickle, boto3
from nltk import word_tokenize, pos_tag
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.collocations import *
import gensim
from gensim import corpora, models

path1 = '/home/ubuntu/dataassets/'
os.chdir(path1)
bucket = 'processed1'
#pull boto access

true_bag = []
lemmatizer = WordNetLemmatizer()
bigram_measures = nltk.collocations.BigramAssocMeasures()
stop_words = set(stopwords.words('english'))
stop_words1 = {'company', 'business', 'financial', 'net', 'gross', 'due', 'year', 'end', 'annual', 
'increase', 'decrease', 'incline', 'decline', 'loss', 'gain', 'prior', 'fiscal', 'statement', 'accounting',
'first', 'second', 'third', 'fourth', 'fifth', 'hundred', 'thousand', 'million', 'billion',
'january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october','november', 'december',
'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten', 
'eleven', 'twelve', 'thirteen', 'fourteen', 'fifteen', 'sixteen', 'seventeen', 'eighteen', 'nineteen', 
'twenty', 'thirty', 'forty', 'fifty', 'sixty', 'seventy', 'eighty', 'ninety'}
#stop_words2 = {'risk', 'factor', 'item', 'operation', 'market', 'significant', 'result', 'product', 'condition', 'cost', 
#'adverse', 'certain', 'effect', 'additional', 'addition', 'change', 'subject', 'ability', 'common', 'stock', 'share', 'price', 
#'future', 'material', 'shareholder', 'stockholder', 'table', 'contents'}
stop_words2 = {'risk','significant', 'result', 'operation', 'condition', 'stock', 'common', 'product', 'cost', 
'operating', 'future', 'addition', 'additional', 'table', 'contents', 'subject', 'ability', 'change', 'market'}

#Read all documents in folder
count = 0
adsh_list = []
for filename in os.listdir(path1):
    with open(filename, "r") as f:
        if filename != '.DS_Store':

            count = count + 1
            if (count % 50) == 0:
                print('Count: ' + str(count))

            adsh = filename[:-4]
            print(adsh)
            f=open(filename, "r")
            f = f.read
            f = f()
            f = f.lower()
            f = str(f)

            word_sent = nltk.sent_tokenize(f) #take each sentence for observation
            sic_bag = []
            for s in word_sent:
                s1 = word_tokenize(s) #tokenize each sentence
                s2 = []
                for t in s1: #lemmatize each word in the sentence to avoid duplicates
                    if t.isalpha():
                        t1 = lemmatizer.lemmatize(t)
                        s2.append(t1)
                s3 = nltk.pos_tag(s2) #grab part of speech
                for u in s3: 
                    if (u[1] == 'NN' or u[1] == 'JJ') and (len(u[0])>2): #only take nouns and adjectives
                        if (u[0] not in stop_words1) and (u[0] not in stop_words2) and (u[0] not in stopwords.words('english')): #ignore stopwords
                            sic_bag.append(u[0]) 


            word_count = [str(adsh), len(sic_bag)]
            adsh_list.append(word_count)
            #true_bag.append(sic_bag[:])

            
            # Collect bigrams
            word_fd = nltk.FreqDist(sic_bag)
            bigram_fd = nltk.FreqDist(nltk.bigrams(sic_bag))
            finder = BigramCollocationFinder(word_fd, bigram_fd)
            finder.apply_freq_filter(3)
            bgrm = sorted(finder.above_score(bigram_measures.raw_freq,1.0 / len(tuple(nltk.bigrams(sic_bag)))))
            gram_bag = []
            for gram in bgrm:
                grammy = str(gram[0]) + str(gram[1])
                gram_bag.append(grammy)

            # form word list / avoid double count
            count1 = 0
            count2 = 0
            sic_bag2 = []
            for words in sic_bag:
                if count2 == 0:
                    if count1 == 0:
                        word1 = words
                        count1 = count1 + 1
                    else:
                        word2 = words
                        word0 = word1 + word2
                        if word0 in gram_bag:
                            sic_bag2.append(word0)
                            count2 = 1
                        else:
                            sic_bag2.append(word1)
                        word1 = words
                        count1 = 1
                else:
                    count2 = 0
                    count1 = 0

            # add word list to corpus
            true_bag.append(sic_bag2[:])
            
            
dct = corpora.Dictionary()
corpus = [dct.doc2bow(doc, allow_update=True) for doc in true_bag]

pickle1 = pickle.dumps(corpus) 
pickle2 = pickle.dumps(dct) 
pickle3 = pickle.dumps(adsh_list) 

s3_resource = boto3.resource('s3', aws_access_key_id=ACCESS_ID, aws_secret_access_key= ACCESS_KEY)
s3_resource.Object(bucket,'corpus.pkl').put(Body=pickle1)
s3_resource.Object(bucket,'dct.pkl').put(Body=pickle2)
s3_resource.Object(bucket,'adsh.pkl').put(Body=pickle3)


 