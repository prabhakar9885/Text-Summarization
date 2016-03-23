"""
USAGE:
python  <Source-document-name> <output-file-name>
"""

import gensim, logging
import sys, os
import nltk
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords

sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
filename = sys.argv[1]	# /home/prabhakar/Desktop/IRE_project/
outfile = sys.argv[2]	

def preprocess(sentence):
	sentence = sentence.lower()
	tokenizer = RegexpTokenizer(r'[A-Za-z\.\,]+')
	tokens = tokenizer.tokenize(sentence)
	filtered_words = [w for w in tokens if not w in stopwords.words('english')]
	return " ".join(filtered_words)

class LabeledLineSentence(object):
    def __init__(self, doc, label):
        self.label = label
        self.doc = doc
        fileContent = preprocess( doc.read() );
        self.sentences = sent_detector.tokenize(fileContent.strip())
    def __iter__(self):
        for idx, sentence in enumerate(self.sentences):
        	yield gensim.models.doc2vec.LabeledSentence(words=sentence, tags=[self.label+str(idx)])

fileObj = open(filename, "r")
it = LabeledLineSentence(fileObj, filename)
model = gensim.models.Doc2Vec(size=300, window=10, min_count=1, workers=11,alpha=0.025, min_alpha=0.025)
model.build_vocab(it)

for epoch in range(10):
	model.train(it)
	model.alpha -= 0.002
	model.min_alpha = model.alpha
	model.train(it)

model.save(outfile + ".model")