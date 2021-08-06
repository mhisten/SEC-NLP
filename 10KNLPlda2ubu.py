
import sys, os, codecs, nltk, re, pickle, pandas, boto3
from gensim.models import LdaModel, LdaMulticore
#import logging
#logging.basicConfig(format='%(levelname)s : %(message)s')
#logging.root.setLevel(level=logging.INFO)

path1 = '/home/ubuntu/amonograms/'
path2 = '/home/ubuntu/'
os.chdir(path1)
bucket = 'processed1'
#pull boto access

os.chdir(path1)
corpus = pandas.read_pickle('corpus.pkl') 
dct = pandas.read_pickle('dct.pkl') 
#print(dct)

lda_model = LdaMulticore(corpus=corpus,
                         id2word=dct,
                         random_state=None,
                         num_topics=10,
                         passes=30,
                         chunksize=1000,
                         batch=False,
                         alpha='asymmetric',
                         decay=0.5,
                         offset=64,
                         eta=None,
                         eval_every=10,
                         iterations=50,
                         gamma_threshold=0.001,
                         per_word_topics=True,
                         dtype='float64')

topiclist = []
for i in lda_model.print_topics(num_topics=lda_model.num_topics, num_words=1000):
    topiclist.append(i)

documentlist = []
for j in lda_model.get_document_topics(bow=corpus, minimum_probability=None, minimum_phi_value=None, per_word_topics=False):
    documentlist.append(j)

pickle1 = pickle.dumps(topiclist) 
pickle2 = pickle.dumps(documentlist) 

s3_resource = boto3.resource('s3', aws_access_key_id=ACCESS_ID, aws_secret_access_key= ACCESS_KEY)
s3_resource.Object(bucket,'topics.pkl').put(Body=pickle1)
s3_resource.Object(bucket,'documents.pkl').put(Body=pickle2)

os.chdir(path2)
lda_model.save('lda_model.gensim')
