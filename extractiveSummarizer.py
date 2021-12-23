import numpy as np
import pandas as pd
import spacy
import time
import re
import networkx as nx
from scipy import spatial
import spacy_universal_sentence_encoder
import tensorflow_text
import os
start = time.time()
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
text = '''RANCHO CUCAMONGA, Calif., March 29, 2021 (GLOBE NEWSWIRE) -- Amphastar Pharmaceuticals, Inc. (NASDAQ: AMPH) announced that the U.S. Food and Drug Administration (“FDA”) approved the Company’s Abbreviated New Drug Application (“ANDA”) for Dextrose injection 50% in the 50 mL Luer-Jet® Prefilled Syringe System. For the past 40 years, the company has sold and marketed the product under the “grandfather” exception to the FDA’s “Prescription Drug Wrap-Up” program. Net revenues for the Company’s Dextrose injection for the year ended December 31, 2020, were $7.6 million.

Amphastar’s CEO and President, Dr. Jack Zhang, commented: “The FDA’s approval of Dextrose, a product often on the Agency’s Drug Shortage list, offers an opportunity to ensure quality products are produced at the highest standard and highlights Amphastar’s manufacturing capabilities to fulfill such market needs.”

Pipeline Information

The Company currently has five ANDAs on file with the FDA targeting products with a market size of approximately $2.3 billion, three biosimilar products in development targeting products with a market size of approximately $13 billion, and seven generic products in development targeting products with a market size of approximately $10.5 billion. This market information is based on IQVIA data for the 12 months ended December 31, 2020. The Company is currently developing multiple proprietary products with injectable and intranasal dosage forms.

Amphastar’s Chinese subsidiary, ANP, currently has 14 Drug Master Files, or DMFs, on file with the FDA and is developing several additional DMFs.
'''

def summarize():
    os.environ['TF_XLA_FLAGS'] = '--tf_xla_enable_xla_devices'
    nlp = spacy_universal_sentence_encoder.load_model('xx_use_md')
    doc = nlp(text)
    # get the vector of the Doc, Span or Token

    sents = doc.sents
    sentList = list(doc.sents)
    preprocess = []
    for sentence in sents:
        #print(sentence)
        #print(type(sentence))
        sentence = list(sentence)

        #print(sentence)


        preprocess.append(sentence)
        processedWords = []
    #print(preprocess)
    for sentence in preprocess:
        #print(sentence)
         for word in sentence:
             if word.is_stop is False:
                 processedWords.append(word)
    #print(processedWords)
    doc2 = nlp(str(processedWords))
    count = 0
    vectorList = []
    for sent in doc2.sents:
        #print(sent)
        vector = sent.vector
        #print(vector)
        count +=1
        vectorList.append(vector)
    #print(vectorList)


    simMatrix = np.zeros([count,count])

    #print(simMatrix.shape)


    for i, row in enumerate(vectorList):
        for j, col in enumerate(vectorList):
            simMatrix[i][j] = 1-spatial.distance.cosine(row,col)

    graph = nx.from_numpy_array(simMatrix)
    rankAlgo = nx.pagerank(graph)

    #print(rankAlgo)

    #print(sorted(rankAlgo.values()))

    index = sorted(rankAlgo, key=rankAlgo.get, reverse=True)
    item = dict(sorted(rankAlgo.items(), key=lambda x: x[1], reverse=True)[:7])

    for x in item:
        print(sentList[x])









summarize()

print('It took', time.time()-start, 'seconds.')
