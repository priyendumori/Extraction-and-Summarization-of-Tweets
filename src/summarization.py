from operator import add
from scipy import spatial
import glob
import sys
import numpy
from scipy.spatial import distance
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from nltk.tokenize import word_tokenize
import random
import heapq
from sklearn.metrics.pairwise import cosine_similarity


def get_sentences(tag):
    files = glob.glob("../data/tweets/"+tag+"/*")
    sentences = []
    for file in files:
        fd = open(file,"r")
        for line in fd:
            sentences.append(line)
        fd.close()
    return sentences


def get_vectors(sentences,model):
    sen_vectors = []
    for sentence in sentences:
        test_data = word_tokenize(sentence.lower())
        v1 = model.infer_vector(test_data)
        sen_vectors.append(v1)
    return sen_vectors


def ranking(sentence_vectors,sentences):
    l = len(sentences)
    if l == 0:
        return [],[]
    centroid_vector = [0 for i in range(len(sentence_vectors[0]))]
    for vector in sentence_vectors:
        centroid_vector = list(map(add, centroid_vector, vector))
    rank = []
    count = 0
    for vector in sentence_vectors:
        rank.append([cosine_similarity([vector,centroid_vector])[0][1],sentences[count]])
        count+=1
    return rank , list(numpy.array(centroid_vector)/l)


def beam_search(model,candidate_set,vectors,theta,k,dm_avg):
    l = len(candidate_set)
    if l == 0:
        return "No such hashtag"
    lk = []
    lold = []
    lnew = []
    for j in range(k):
        lold.append([candidate_set[random.randint(0, l)][1]])
    #print(lold)
    while len(lold):
        for sentence in candidate_set:
            for summary_set in lold:
                if sentence[1] not in summary_set:
                    summary_set_new = summary_set + [sentence[1]]
                    test_data = word_tokenize('.'.join(summary_set_new).lower())
                    v1 = model.infer_vector(test_data)
                    error = (distance.euclidean(v1, dm_avg))**2
                    if len(summary_set_new) < theta:
                        lnew.append([error,summary_set_new])
                        lnew = heapq.nsmallest(k,lnew)
                    elif len(summary_set_new) == theta:
                        lk.append([error,summary_set_new])
                        lk = heapq.nsmallest(k,lk)

        lold = [row[1] for row in lnew]
        lnew = []

    return '.'.join(lk[0][1])
